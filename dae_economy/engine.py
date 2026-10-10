"""Pure decision logic. No network, wallet, subprocess, or payment side effects."""
from .models import Evaluation, Opportunity


def evaluate(op: Opportunity, *, minimum_net_value: float = 0.25,
             minimum_margin: float = 0.20,
             risk_haircut: float = 0.15,
             reject_upfront_payment: bool = True) -> Evaluation:
    """Estimate expected value conservatively; this is a screen, not a guarantee."""
    from math import isfinite
    if not isfinite(minimum_net_value) or minimum_net_value < 0:
        raise ValueError("minimum_net_value must be finite and >= 0")
    if not isfinite(minimum_margin) or not 0 <= minimum_margin <= 1:
        raise ValueError("minimum_margin must be between 0 and 1")
    if not isfinite(risk_haircut) or not 0 <= risk_haircut <= 1:
        raise ValueError("risk_haircut must be between 0 and 1")
    if reject_upfront_payment and op.requires_upfront_payment:
        return Evaluation(op.opportunity_id, 0.0, 0.0, 0.0, 0.0, 0.0,
                          False, "Rejected: opportunity requires upfront payment")
    gross = op.reward * op.probability_success * op.probability_payment_if_success
    variable_cost = op.compute_cost + op.labor_cost + op.platform_fee
    expected_failure_cost = (1 - op.probability_success) * op.failure_cost
    expected_cost = variable_cost + expected_failure_cost
    net = gross - expected_cost
    margin = net / gross if gross > 0 else (-1.0 if expected_cost > 0 else 0.0)
    # Penalize uncertainty and thin margins rather than treating EV as certain.
    risk_adjusted = net * (1 - risk_haircut)
    eligible = net >= minimum_net_value and margin >= minimum_margin
    reason = "Passes economic screen" if eligible else "Rejected: expected value or margin below threshold"
    return Evaluation(op.opportunity_id, round(gross, 6), round(expected_cost, 6),
                      round(net, 6), round(margin, 6), round(risk_adjusted, 6),
                      eligible, reason)


def allocate_surplus(verified_cash: float, *, reserve_ratio: float = 0.50,
                     operations_ratio: float = 0.30,
                     growth_ratio: float = 0.20) -> dict[str, float]:
    """Allocate only verified positive cash. Ratios must sum to 1."""
    from math import isfinite
    if not isfinite(verified_cash) or verified_cash < 0:
        raise ValueError("verified_cash must be finite and >= 0")
    ratios = (reserve_ratio, operations_ratio, growth_ratio)
    if any(not isfinite(x) or x < 0 or x > 1 for x in ratios):
        raise ValueError("allocation ratios must be finite and between 0 and 1")
    if abs(sum(ratios) - 1.0) > 1e-9:
        raise ValueError("allocation ratios must sum to 1")
    return {
        "reserve": round(verified_cash * reserve_ratio, 2),
        "operations": round(verified_cash * operations_ratio, 2),
        "growth": round(verified_cash * growth_ratio, 2),
    }


def can_replicate(*, verified_paid_tasks: int, net_profit: float,
                  profit_margin: float, policy_violations: int,
                  minimum_tasks: int = 10, minimum_margin: float = 0.30) -> tuple[bool, str]:
    """Replication gate. Returns a decision only; never creates or funds a child."""
    if min(verified_paid_tasks, policy_violations, minimum_tasks) < 0:
        return False, "Invalid negative counter"
    if net_profit <= 0:
        return False, "No positive verified net profit"
    if profit_margin < minimum_margin:
        return False, "Profit margin below replication threshold"
    if verified_paid_tasks < minimum_tasks:
        return False, "Insufficient verified paid-task history"
    if policy_violations:
        return False, "Policy violations block replication"
    return True, "Eligible for human-reviewed replication proposal"
