"""Fail-closed economic policy for the existing DAE core models."""
import math
from .models import SafetyPolicy, Task
from .scoring import score_task

def task_rejection_reasons(task: Task, policy: SafetyPolicy) -> list[str]:
    reasons=[]
    try:
        task.validate()
        policy.validate()
        score=score_task(task)
    except (ValueError, TypeError, OverflowError) as exc:
        return [f"invalid_input:{str(exc)}"]
    if task.estimated_cost > policy.max_cost_per_task: reasons.append("cost_exceeds_per_task_limit")
    if task.confidence < policy.min_confidence: reasons.append("confidence_below_policy_floor")
    if task.risk > policy.max_risk: reasons.append("risk_exceeds_policy_limit")
    if score.expected_net < policy.min_net_profit: reasons.append("expected_net_below_policy_floor")
    risk_adjusted_net=task.expected_revenue*task.confidence*(1-task.risk)-task.estimated_cost
    if risk_adjusted_net < 0: reasons.append("negative_risk_adjusted_net")
    return reasons
