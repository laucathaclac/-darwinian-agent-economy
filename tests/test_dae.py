import unittest

from dae.evolution import evaluate_agent
from dae.models import AgentHistory, AgentResult, EvolutionAction, SafetyPolicy, Task
from dae.policy import task_is_allowed, task_rejection_reasons
from dae.scoring import score_task


class ScoringTests(unittest.TestCase):
    def test_score_is_bounded(self):
        task = Task("a", "Good task", 20, 2, 1, 0.9, 0.1)
        result = score_task(task)
        self.assertGreaterEqual(result.score, 0)
        self.assertLessEqual(result.score, 100)

    def test_invalid_confidence_rejected(self):
        with self.assertRaises(ValueError):
            score_task(Task("a", "Bad", 20, 2, 1, 1.5, 0.1))


class PolicyTests(unittest.TestCase):
    def test_safe_task_allowed(self):
        self.assertTrue(task_is_allowed(
            Task("a", "Good", 20, 2, 1, 0.9, 0.1), SafetyPolicy()))

    def test_task_cost_limit(self):
        reasons = task_rejection_reasons(
            Task("a", "Expensive", 30, 12, 1, 0.9, 0.1), SafetyPolicy())
        self.assertTrue(any("per-task limit" in reason for reason in reasons))

    def test_daily_limit(self):
        reasons = task_rejection_reasons(
            Task("a", "Over budget", 20, 8, 1, 0.9, 0.1),
            SafetyPolicy(), spent_today=20)
        self.assertTrue(any("daily budget" in reason for reason in reasons))


class EvolutionTests(unittest.TestCase):
    def test_insufficient_history_does_not_replicate(self):
        action, _ = evaluate_agent(AgentHistory("a", [AgentResult(10, 1)]))
        self.assertEqual(action, EvolutionAction.CONTINUE)

    def test_consecutive_losses_pause(self):
        history = AgentHistory("a", [
            AgentResult(5, 1), AgentResult(2, 5),
            AgentResult(1, 4), AgentResult(0, 2)])
        action, _ = evaluate_agent(history)
        self.assertEqual(action, EvolutionAction.PAUSE)

    def test_profit_only_qualifies_for_human_review(self):
        history = AgentHistory("a", [AgentResult(10, 2) for _ in range(5)])
        action, reason = evaluate_agent(history)
        self.assertEqual(action, EvolutionAction.REVIEW_REPLICATION)
        self.assertIn("No agent was created", reason)

    def test_agent_cap_blocks_review(self):
        history = AgentHistory("a", [AgentResult(10, 2) for _ in range(5)])
        action, _ = evaluate_agent(history, active_agents=3, max_active_agents=3)
        self.assertEqual(action, EvolutionAction.CONTINUE)


if __name__ == "__main__":
    unittest.main()
