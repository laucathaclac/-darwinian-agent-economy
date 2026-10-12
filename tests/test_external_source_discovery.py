import unittest
from scripts.dae_external_source_discovery import build_report

class ExternalSourceDiscoveryTests(unittest.TestCase):
    def test_discloses_manual_mode_and_zero_paid_calls(self):
        report = build_report()
        self.assertEqual(report["mode"], "manual_review_links_only")
        self.assertEqual(report["paid_api_calls"], 0)
        self.assertEqual(report["live_results_fetched"], 0)
        self.assertIn("not verified", report["warning"].lower())

    def test_covers_x_and_binance_square(self):
        report = build_report()
        sources = {item["source"] for item in report["results"]}
        self.assertIn("X", sources)
        self.assertIn("Web search → Binance Square", sources)
        self.assertGreaterEqual(len(report["results"]), 6)

    def test_each_entry_has_search_url(self):
        for item in build_report()["results"]:
            self.assertTrue(item["url"].startswith("https://"))
            self.assertTrue(item["query"])
            self.assertTrue(item["category"])

if __name__ == "__main__":
    unittest.main()
