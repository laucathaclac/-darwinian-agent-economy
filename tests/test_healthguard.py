import unittest
from datetime import datetime, timezone
from dae.healthguard import HealthGuardPolicy, PositionSnapshot, assess_position, assess_json
NOW = datetime(2026, 10, 15, 12, 0, tzinfo=timezone.utc)
FRESH = "2026-10-15T11:59:00+00:00"
def snapshot(collateral=1000, debt=500, threshold=0.8, observed=FRESH):
    return PositionSnapshot(collateral, debt, threshold, observed, "unit-test-fixture")
class HealthGuardTests(unittest.TestCase):
    def test_healthy_position(self):
        result = assess_position(snapshot(), now=NOW)
        self.assertEqual(result["status"], "HEALTHY")
        self.assertEqual(result["health_factor"], 1.6)
        self.assertFalse(result["transaction_executed"])
    def test_warning_position(self):
        result = assess_position(snapshot(collateral=800, debt=500), now=NOW)
        self.assertEqual(result["status"], "WARNING")
        self.assertEqual(result["recommendation"], "REVIEW_POSITION")
    def test_critical_position(self):
        self.assertEqual(assess_position(snapshot(collateral=700, debt=500), now=NOW)["status"], "CRITICAL")
    def test_urgent_position(self):
        self.assertEqual(assess_position(snapshot(collateral=650, debt=500), now=NOW)["status"], "URGENT")
    def test_at_liquidation_threshold(self):
        self.assertEqual(assess_position(snapshot(collateral=625, debt=500), now=NOW)["status"], "LIQUIDATION_THRESHOLD_REACHED")
    def test_stale_snapshot_fails_closed(self):
        result = assess_position(snapshot(observed="2026-10-15T11:00:00+00:00"), now=NOW)
        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["recommendation"], "REFRESH_DATA")
    def test_future_snapshot_fails_closed(self):
        self.assertEqual(assess_position(snapshot(observed="2026-10-15T12:01:00+00:00"), now=NOW)["status"], "UNKNOWN")
    def test_zero_debt(self):
        result = assess_position(snapshot(debt=0), now=NOW)
        self.assertEqual(result["status"], "NO_DEBT")
        self.assertIsNone(result["health_factor"])
    def test_invalid_threshold_rejected(self):
        with self.assertRaises(ValueError):
            assess_position(snapshot(threshold=0), now=NOW)
    def test_policy_threshold_order_validated(self):
        with self.assertRaises(ValueError):
            assess_position(snapshot(), HealthGuardPolicy(urgent_below=1.2, critical_below=1.1), now=NOW)
    def test_json_wrapper(self):
        result = assess_json({"position": {"collateral_value": 1000, "debt_value": 500, "liquidation_threshold": 0.8, "observed_at": FRESH, "source": "fixture"}}, now=NOW)
        self.assertEqual(result["health_factor"], 1.6)
    def test_transaction_never_claimed(self):
        result = assess_position(snapshot(), now=NOW)
        self.assertEqual(result["execution_status"], "NOT_IMPLEMENTED")
        self.assertFalse(result["transaction_executed"])
if __name__ == "__main__":
    unittest.main()
