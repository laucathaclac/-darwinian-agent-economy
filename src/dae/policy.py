import math
from .models import SafetyPolicy, Task
from .scoring import score_task

def task_rejection_reasons(task: Task, policy: SafetyPolicy) -> list[str]:
    reasons=[]
    if not task.task_id or not task.title: reasons.append("missing_task_identity")
    numeric=(task.reward_usd,task.estimated_cost_usd,task.estimated_hours,task.success_probability,task.risk_probability)
    if not all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in numeric):
        return reasons+["non_finite_or_non_numeric_input"]
    if task.reward_usd <= 0: reasons.append("reward_not_positive")
    if task.estimated_cost_usd < 0 or task.estimated_hours <= 0: reasons.append("invalid_cost_or_hours")
    if not 0 <= task.success_probability <= 1 or not 0 <= task.risk_probability <= 1: reasons.append("invalid_probability")
    if task.source not in {"github_issues","taskbounty","demo"}: reasons.append("unknown_source")
    if not reasons:
        score=score_task(task)
        if score.expected_net < policy.minimum_expected_value_usd: reasons.append("expected_net_below_policy_floor")
        if task.reward_usd > 0 and score.expected_net/task.reward_usd < policy.minimum_margin: reasons.append("margin_below_policy_floor")
        if task.reward_usd*task.success_probability*(1-task.risk_probability)-task.estimated_cost_usd < 0: reasons.append("negative_risk_adjusted_net")
    return reasons
