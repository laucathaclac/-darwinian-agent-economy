import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("dae_hourly_scan", Path(__file__).parents[1] / "scripts" / "dae_hourly_scan.py")
SCANNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCANNER)

class HourlyScannerSafetyTests(unittest.TestCase):
    def test_reward_text_is_never_treated_as_verified_funding(self):
        lead = SCANNER.evaluate({
            "id": 1,
            "title": "Paid bounty $250",
            "body": "Implementation task.\nDeadline: 2026-12-01\n" + ("Acceptance criteria. " * 20),
            "html_url": "https://github.com/example/project/issues/1",
            "repository_url": "https://api.github.com/repos/example/project",
            "user": {"login": "owner"},
            "updated_at": "2026-10-12T00:00:00Z",
        })
        self.assertEqual(lead["reward_amount_claimed_usd"], 250.0)
        self.assertIn("UNVERIFIED", lead["reward_status"])

    def test_wallet_secret_and_deposit_phrases_require_manual_check(self):
        for phrase in ("send your seed phrase", "provide private key", "connect your wallet", "deposit first", "send crypto first"):
            with self.subTest(phrase=phrase):
                lead = SCANNER.evaluate({
                    "id": 2, "title": "Reward $50", "body": phrase + "\nDeadline: Friday",
                    "html_url": "https://github.com/example/project/issues/2",
                    "repository_url": "https://api.github.com/repos/example/project",
                    "user": {"login": "owner"}, "updated_at": "",
                })
                self.assertEqual(lead["review_status"], "NEEDS_MANUAL_CHECK")
                self.assertTrue(any("unsafe fee language" in reason for reason in lead["reasons"]))

    def test_missing_reward_and_deadline_stay_unqualified(self):
        lead = SCANNER.evaluate({"id": 3, "title": "Help wanted", "body": "No details", "html_url": "https://github.com/example/project/issues/3"})
        self.assertIsNone(lead["reward_amount_claimed_usd"])
        self.assertEqual(lead["review_status"], "NEEDS_MANUAL_CHECK")

if __name__ == "__main__":
    unittest.main()
