"""Deterministic, fail-closed health-factor assessment for DAE HealthGuard.
Decision-support core only: no RPC client, wallet, signing, or transaction execution.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import math
from typing import Any

@dataclass(frozen=True)
class PositionSnapshot:
    """Normalized lending position, denominated in one consistent quote asset."""
    collateral_value: float
    debt_value: float
    liquidation_threshold: float
    observed_at: str
    source: str

    def validate(self) -> None:
        for name, value in (("collateral_value", self.collateral_value), ("debt_value", self.debt_value), ("liquidation_threshold", self.liquidation_threshold)):
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{name} must be a finite number")
        if self.collateral_value < 0 or self.debt_value < 0:
            raise ValueError("collateral_value and debt_value cannot be negative")
        if not 0 < self.liquidation_threshold <= 1:
            raise ValueError("liquidation_threshold must be in (0, 1]")
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("source is required")
        try:
            parsed = datetime.fromisoformat(self.observed_at.replace("Z", "+00:00"))
        except (AttributeError, ValueError) as exc:
            raise ValueError("observed_at must be an ISO-8601 timestamp") from exc
        if parsed.tzinfo is None:
            raise ValueError("observed_at must include a timezone")

@dataclass(frozen=True)
class HealthGuardPolicy:
    """Thresholds for alerts; these are not financial guarantees."""
    urgent_below: float = 1.05
    critical_below: float = 1.15
    warning_below: float = 1.35
    max_snapshot_age_seconds: int = 300

    def validate(self) -> None:
        values = (self.urgent_below, self.critical_below, self.warning_below)
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in values):
            raise ValueError("health-factor thresholds must be finite numbers")
        if not 0 < self.urgent_below < self.critical_below < self.warning_below:
            raise ValueError("thresholds must satisfy 0 < urgent < critical < warning")
        if isinstance(self.max_snapshot_age_seconds, bool) or not isinstance(self.max_snapshot_age_seconds, int) or self.max_snapshot_age_seconds < 0:
            raise ValueError("max_snapshot_age_seconds must be a non-negative integer")

def assess_position(snapshot: PositionSnapshot, policy: HealthGuardPolicy | None = None, *, now: datetime | None = None) -> dict[str, Any]:
    """Assess a position; stale/future data fails closed and no transaction is executed."""
    policy = policy or HealthGuardPolicy()
    snapshot.validate()
    policy.validate()
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must include a timezone")
    observed = datetime.fromisoformat(snapshot.observed_at.replace("Z", "+00:00"))
    age = (now.astimezone(timezone.utc) - observed.astimezone(timezone.utc)).total_seconds()
    common = {
        "source": snapshot.source, "observed_at": snapshot.observed_at,
        "snapshot_age_seconds": round(age, 3), "collateral_value": float(snapshot.collateral_value),
        "debt_value": float(snapshot.debt_value), "liquidation_threshold": float(snapshot.liquidation_threshold),
        "transaction_executed": False, "execution_status": "NOT_IMPLEMENTED",
    }
    if age < 0 or age > policy.max_snapshot_age_seconds:
        return {**common, "status": "UNKNOWN", "health_factor": None, "recommendation": "REFRESH_DATA",
                "reason": "Snapshot is future-dated or exceeds the configured freshness limit."}
    if snapshot.debt_value == 0:
        return {**common, "status": "NO_DEBT", "health_factor": None, "recommendation": "MONITOR",
                "reason": "Debt is zero; health factor is not defined for this position."}
    hf = snapshot.collateral_value * snapshot.liquidation_threshold / snapshot.debt_value
    if not math.isfinite(hf):
        raise ValueError("computed health factor is not finite")
    if hf <= 1.0:
        status, recommendation = "LIQUIDATION_THRESHOLD_REACHED", "URGENT_HUMAN_REVIEW"
        reason = "Computed health factor is at or below 1.0; verify protocol-specific liquidation rules immediately."
    elif hf < policy.urgent_below:
        status, recommendation, reason = "URGENT", "URGENT_HUMAN_REVIEW", "Health factor is below the urgent threshold."
    elif hf < policy.critical_below:
        status, recommendation, reason = "CRITICAL", "REVIEW_REPAY_OR_ADD_COLLATERAL", "Health factor is below the critical threshold."
    elif hf < policy.warning_below:
        status, recommendation, reason = "WARNING", "REVIEW_POSITION", "Health factor is below the warning threshold."
    else:
        status, recommendation, reason = "HEALTHY", "MONITOR", "Health factor is above the configured warning threshold."
    return {**common, "status": status, "health_factor": round(hf, 8), "recommendation": recommendation, "reason": reason}

def assess_json(payload: dict[str, Any], *, now: datetime | None = None) -> dict[str, Any]:
    """Convenience wrapper for a decoded JSON object."""
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")
    position, policy_payload = payload.get("position", payload), payload.get("policy", {})
    if not isinstance(position, dict) or not isinstance(policy_payload, dict):
        raise ValueError("position and policy must be JSON objects")
    snapshot = PositionSnapshot(
        collateral_value=position.get("collateral_value"), debt_value=position.get("debt_value"),
        liquidation_threshold=position.get("liquidation_threshold"), observed_at=position.get("observed_at"),
        source=position.get("source"),
    )
    return assess_position(snapshot, HealthGuardPolicy(**policy_payload), now=now)
