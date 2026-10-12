"""Fail-closed economic policy for the existing DAE core models."""
import math

from .models import SafetyPolicy, Task
from .scoring import score_task


def task_rejection_reasons(
    task: Task,
    policy: SafetyPolicy,
    *,
    spent_today: float = 0.0,
) -> list[str]:
    """Return all reasons a task is disallowed.

    spent_today is the amount already spent under the same daily budget.
    Invalid or non-finite inputs fail closed rather than being treated as safe.
    """
    if not isinstance(spent_today, (int, float)) or not math.isfinite(spent_today):
        raise ValueError("spent_today must be finite")
    if spent_today < 0:
        raise ValueError("spent_today cannot be negative")

    try:
        task.validate()
        policy.validate()
        score = score_task(task)
    except (ValueError, TypeError, OverflowError) as exc:
        return [f"invalid_input:{str(exc)}"]

    reasons: list[str] = []
    if task.estimated_cost > policy.max_cost_per_task:
        reasons.append("cost exceeds per-task limit")
    if spent_today + task.estimated_cost > policy.max_daily_spend:
        reasons.append("cost exceeds daily budget")
    if task.confidence < policy.min_confidence:
        reasons.append("confidence below policy floor")
    if task.risk > policy.max_risk:
        reasons.append("risk exceeds policy limit")
    if score.expected_net < policy.min_net_profit:
        reasons.append("expected net below policy floor")

    risk_adjusted_net = (
        task.expected_revenue * task.confidence * (1 - task.risk)
        - task.estimated_cost
    )
    if risk_adjusted_net < 0:
        reasons.append("negative risk-adjusted net")
    return reasons


def task_is_allowed(
    task: Task,
    policy: SafetyPolicy,
    *,
    spent_today: float = 0.0,
) -> bool:
    """Return True only when no policy rejection reasons exist."""
    return not task_rejection_reasons(task, policy, spent_today=spent_today)
