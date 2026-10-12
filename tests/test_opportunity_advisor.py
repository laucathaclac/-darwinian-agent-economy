import json
import tempfile
import unittest
from pathlib import Path
import importlib.util

SPEC = importlib.util.spec_from_file_location("dae_opportunity_advisor", Path(__file__).parents[1] / "scripts" / "dae_opportunity_advisor.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class AdvisorTests(unittest.TestCase):
    def test_reward_is_not_funding(self):
        result = MODULE.assess({"title":"$500 bounty", "url":"https://example.com", "reward_amount_claimed_usd":500, "deadline_text":"Friday", "review_status":"REVIEW_LEAD", "reasons":[]})
        self.assertEqual(result["funding_status"], "UNVERIFIED")
        self.assertEqual(result["win_potential"], "UNRATED — insufficient competition and judging data")
        self.assertIn("not proof of funding", result["evidence_notes"][0])

    def test_unknown_reward_stays_unknown(self):
        result = MODULE.assess({"title":"Freelance issue", "url":"https://example.com", "reward_amount_claimed_usd":None, "deadline_text":None, "review_status":"NEEDS_MANUAL_CHECK", "reasons":["reward amount missing"]})
        self.assertIsNone(result["claimed_reward_usd"])
        self.assertEqual(result["funding_status"], "UNVERIFIED")
        self.assertIn("NOT ESTIMABLE", result["estimated_net_value_per_hour"])
        self.assertTrue(result["risks"])

if __name__ == "__main__":
    unittest.main()
