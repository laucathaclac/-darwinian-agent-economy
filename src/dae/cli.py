"""Local deterministic demo for DAE."""
import argparse
from .evolution import evaluate_agent
from .models import AgentHistory, AgentResult, SafetyPolicy, Task
from .policy import task_rejection_reasons
from .scoring import score_task


def run_demo() -> int:
    policy = SafetyPolicy()
    tasks = [
        Task("demo-001", "Prepare a public-data report", 18, 3, 2, 0.85, 0.15, "demo"),
        Task("demo-002", "Unverified high-cost opportunity", 40, 18, 3, 0.70, 0.65, "demo"),
        Task("demo-003", "Low-value repetitive task", 4, 1, 1, 0.75, 0.20, "demo"),
    ]
    print("DAE demo — simulation only; no external tasks are executed.\n")
    for task in tasks:
        score = score_task(task)
        rejected = task_rejection_reasons(task, policy)
        status = "ELIGIBLE FOR REVIEW" if not rejected else "REJECTED BY POLICY"
        print(f"{task.task_id}: {task.title}")
        print(f"  score={score.score:.2f}/100 | expected_net={score.expected_net:.2f} | {status}")
        for reason in rejected:
            print(f"  - {reason}")
    history = AgentHistory("demo-agent", [
        AgentResult(8, 2), AgentResult(9, 2), AgentResult(7, 1),
        AgentResult(10, 2), AgentResult(8, 1),
    ])
    action, reason = evaluate_agent(history)
    print(f"\nEvolution decision: {action.value}\nReason: {reason}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="dae", description="Darwinian Agent Economy MVP")
    parser.add_argument("command", choices=["demo"])
    args = parser.parse_args()
    if args.command == "demo":
        raise SystemExit(run_demo())


if __name__ == "__main__":
    main()
