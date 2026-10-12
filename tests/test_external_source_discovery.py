import unittest
from scripts.dae_external_source_discovery import build_report

class ExternalSourceDiscoveryTests(unittest.TestCase):
    def test_report_is_transparent_about_not_fetching_live_results(self):
        report = build_report()
        self.assertEqual(report["mode"], "manual_review_links_only")
        self.assertEqual(report["paid_api_calls"], 0)
        self.assertEqual(report["live_results_fetched"], 0)
        self.assertIn("not verified", report["warning"].lower())

    def test_has_x_and_binance_square_discovery(self):
        results = build_report()["results"]
        sources = {item["source"] for item in results}
        self.assertIn("X", sources)
        self.assertIn("Web search → Binance Square", sources)
        self.assertGreaterEqual(len(results), 5)

    def test_all_searches_have_valid_urls_and_queries(self):
        for item in build_report()["results"]:
            self.assertTrue(item["url"].startswith("https://"))
            self.assertTrue(item["query"])
            self.assertTrue(item["category"])

if __name__ == "__main__":
    unittest.main()
