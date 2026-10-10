"""Fail-closed policy checks. This module never executes tasks."""
from math import isfinite
from .models import SafetyPolicy, Task


def task_rejection_reasons(task: Task, policy: SafetyPolicy,
                           spent_today: float = 0.0) -> list[str]:
    policy.validate()
    task.validate()
    if not isfinite(spent_today) or spent_today < 0:
        raise ValueError("spent_today must be finite and non-negative")
    reasons: list[str] = []
    if task.estimated_cost > policy.max_cost_per_task:
        reasons.append("estimated cost exceeds per-task limit")
    if spent_today + task.estimated_cost > policy.max_daily_spend:
        reasons.append("estimated cost exceeds remaining daily budget")
    if task.confidence < policy.min_confidence:
        reasons.append("confidence is below policy minimum")
    if task.risk > policy.max_risk:
        reasons.append("risk exceeds policy maximum")
    if task.expected_revenue * task.confidence - task.estimated_cost < policy.min_net_profit:
        reasons.append("confidence-adjusted expected net is below minimum")
    return reasons


def task_is_allowed(task: Task, policy: SafetyPolicy,
                    spent_today: float = 0.0) -> bool:
    return not task_rejection_reasons(task, policy, spent_today)
