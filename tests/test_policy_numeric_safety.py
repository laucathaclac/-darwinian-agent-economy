import unittest
from math import inf, nan

from dae.models import SafetyPolicy, Task
from dae.policy import task_rejection_reasons


class NumericSafetyTests(unittest.TestCase):
    def setUp(self):
        self.task = Task("safe", "Bounded test task", 20, 2, 1, 0.9, 0.1)

    def test_nan_policy_limit_fails_closed(self):
        with self.assertRaises(ValueError):
            SafetyPolicy(max_daily_spend=nan).validate()

    def test_infinite_policy_limit_fails_closed(self):
        with self.assertRaises(ValueError):
            SafetyPolicy(max_cost_per_task=inf).validate()

    def test_nan_spend_fails_closed(self):
        with self.assertRaises(ValueError):
            task_rejection_reasons(self.task, SafetyPolicy(), spent_today=nan)

    def test_infinite_spend_fails_closed(self):
        with self.assertRaises(ValueError):
            task_rejection_reasons(self.task, SafetyPolicy(), spent_today=inf)


if __name__ == "__main__":
    unittest.main()
