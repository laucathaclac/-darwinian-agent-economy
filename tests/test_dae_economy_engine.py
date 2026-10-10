import math
import pytest
from dae_economy.engine import allocate_surplus, can_replicate, evaluate
from dae_economy.ledger import Ledger
from dae_economy.models import Opportunity


def op(**overrides):
    data = dict(opportunity_id="t1", title="Test task", reward=20.0,
                probability_success=0.9, probability_payment_if_success=0.9,
                compute_cost=0.5, labor_cost=2.0, platform_fee=1.0,
                failure_cost=1.0, hours_required=1.0)
    data.update(overrides)
    return Opportunity(**data)


def test_expected_value_calculation():
    result = evaluate(op())
    assert result.expected_gross_revenue == pytest.approx(16.2)
    assert result.expected_cost == pytest.approx(3.6)
    assert result.expected_net_value == pytest.approx(12.6)
    assert result.eligible


def test_upfront_payment_is_rejected_by_default():
    result = evaluate(op(requires_upfront_payment=True))
    assert not result.eligible
    assert "upfront" in result.reason.lower()


@pytest.mark.parametrize("value", [-1, math.inf, math.nan])
def test_rejects_invalid_reward(value):
    with pytest.raises(ValueError):
        op(reward=value)


def test_probabilities_are_bounded():
    with pytest.raises(ValueError):
        op(probability_success=1.1)


def test_unprofitable_opportunity_is_rejected():
    result = evaluate(op(reward=1, compute_cost=4, labor_cost=5, platform_fee=0))
    assert not result.eligible


def test_allocation_sums_to_verified_cash():
    parts = allocate_surplus(100)
    assert parts == {"reserve": 50.0, "operations": 30.0, "growth": 20.0}


def test_allocation_rejects_bad_ratios():
    with pytest.raises(ValueError):
        allocate_surplus(100, reserve_ratio=0.9, operations_ratio=0.2, growth_ratio=0.1)


def test_replication_requires_evidence_of_sustained_profit():
    assert not can_replicate(verified_paid_tasks=20, net_profit=100, profit_margin=.4, policy_violations=1)[0]
    assert not can_replicate(verified_paid_tasks=3, net_profit=100, profit_margin=.4, policy_violations=0)[0]
    assert can_replicate(verified_paid_tasks=10, net_profit=100, profit_margin=.4, policy_violations=0)[0]


def test_ledger_never_counts_claimed_revenue_as_cash(tmp_path):
    ledger = Ledger(tmp_path / "ledger.sqlite")
    ledger.record("revenue", "task1", 50, verified=False)
    ledger.record("revenue", "task2", 12, verified=True, evidence="payment receipt id")
    ledger.record("cost", "task2", 2)
    summary = ledger.summary()
    assert summary["claimed_revenue"] == 50
    assert summary["verified_revenue"] == 12
    assert summary["verified_net_cashflow"] == 10


def test_ledger_rejects_verified_revenue_without_evidence(tmp_path):
    ledger = Ledger(tmp_path / "ledger.sqlite")
    with pytest.raises(ValueError):
        ledger.record("revenue", "task1", 10, verified=True)
