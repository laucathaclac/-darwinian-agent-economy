"""Typed domain models and conservative economics for DAE."""
from dataclasses import dataclass
from math import isfinite


def _finite_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and >= 0")


@dataclass(frozen=True)
class Opportunity:
    opportunity_id: str
    title: str
    reward: float
    probability_success: float
    probability_payment_if_success: float
    compute_cost: float = 0.0
    labor_cost: float = 0.0
    platform_fee: float = 0.0
    failure_cost: float = 0.0
    hours_required: float = 0.0
    evidence_url: str = ""
    requires_upfront_payment: bool = False

    def __post_init__(self) -> None:
        if not self.opportunity_id.strip():
            raise ValueError("opportunity_id is required")
        if not self.title.strip():
            raise ValueError("title is required")
        for name in ("reward", "compute_cost", "labor_cost", "platform_fee",
                     "failure_cost", "hours_required"):
            _finite_nonnegative(name, getattr(self, name))
        for name in ("probability_success", "probability_payment_if_success"):
            value = getattr(self, name)
            if not isfinite(value) or not 0 <= value <= 1:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.platform_fee > self.reward:
            raise ValueError("platform_fee cannot exceed reward")


@dataclass(frozen=True)
class Evaluation:
    opportunity_id: str
    expected_gross_revenue: float
    expected_cost: float
    expected_net_value: float
    expected_margin: float
    risk_adjusted_value: float
    eligible: bool
    reason: str


@dataclass(frozen=True)
class Receipt:
    opportunity_id: str
    amount: float
    evidence: str
    verified: bool = False

    def __post_init__(self) -> None:
        _finite_nonnegative("amount", self.amount)
        if not self.opportunity_id.strip():
            raise ValueError("opportunity_id is required")
        if self.verified and not self.evidence.strip():
            raise ValueError("verified receipts require evidence")
