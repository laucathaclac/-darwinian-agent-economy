"""Deterministic opportunity scoring; scores are not income guarantees."""
from .models import Task, TaskScore


def score_task(task: Task) -> TaskScore:
    task.validate()
    expected_net = task.expected_revenue * task.confidence - task.estimated_cost
    roi = ((task.expected_revenue - task.estimated_cost) / task.expected_revenue
           if task.expected_revenue > 0 else 0.0)
    roi_factor = max(0.0, min(1.0, roi))
    score = 100 * (
        0.40 * task.confidence
        + 0.25 * (1.0 - task.risk)
        + 0.20 * roi_factor
        + 0.15 * (1.0 / (1.0 + task.estimated_hours))
    )
    reasons = (
        f"confidence={task.confidence:.0%}",
        f"risk={task.risk:.0%}",
        f"confidence_adjusted_expected_net={expected_net:.2f}",
        f"estimated_hours={task.estimated_hours:g}",
    )
    return TaskScore(task.task_id, round(score, 2), round(expected_net, 2), reasons)
