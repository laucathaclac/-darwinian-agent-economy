"""Local-only demo CLI: python -m dae_economy.cli"""
import argparse
import json
from .engine import allocate_surplus, can_replicate, evaluate
from .ledger import Ledger
from .models import Opportunity


def main() -> int:
    parser = argparse.ArgumentParser(description="DAE economic engine (safe local demo)")
    parser.add_argument("command", choices=("demo", "ledger-summary"))
    parser.add_argument("--ledger", default="dae_ledger.sqlite3")
    args = parser.parse_args()

    if args.command == "ledger-summary":
        print(json.dumps(Ledger(args.ledger).summary(), indent=2))
        return 0

    example = Opportunity(
        opportunity_id="demo-task-001",
        title="Example paid data-cleaning task",
        reward=20.0,
        probability_success=0.80,
        probability_payment_if_success=0.90,
        compute_cost=0.50,
        labor_cost=5.0,
        platform_fee=1.0,
        failure_cost=1.0,
        hours_required=1.0,
        evidence_url="https://example.invalid/demo",
    )
    result = evaluate(example)
    print("DEMO ONLY — no task is accepted and no money moves.")
    print(json.dumps(result.__dict__, indent=2))
    print("Illustrative allocation of $10 verified surplus:")
    print(json.dumps(allocate_surplus(10.0), indent=2))
    print("Replication gate:", can_replicate(
        verified_paid_tasks=10, net_profit=12.0, profit_margin=0.35,
        policy_violations=0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
