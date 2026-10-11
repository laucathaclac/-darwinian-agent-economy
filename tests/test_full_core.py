import math, tempfile, unittest
from pathlib import Path
from dae.models import SafetyPolicy, Task
from dae.policy import task_rejection_reasons
from dae.store import Store
from dae.economy import EconomicSnapshot

class FullCoreTests(unittest.TestCase):
    def test_low_ev_task_rejected(self):
        t=Task("low","tiny reward",4,1,1,.75,.2,"demo")
        self.assertIn("expected_net_below_policy_floor", task_rejection_reasons(t,SafetyPolicy()))
    def test_non_finite_task_rejected(self):
        t=Task("nan","bad number",10,float("nan"),1,.8,.1,"demo")
        self.assertIn("non_finite_or_non_numeric_input", task_rejection_reasons(t,SafetyPolicy()))
    def test_store_labels_cash_unverified(self):
        with tempfile.TemporaryDirectory() as d:
            s=Store(str(Path(d)/"dae.db")); s.add_agent("a1","demo")
            s.record_simulation("a1","SIMULATED_REVENUE",20,"mock")
            s.record_simulation("a1","SIMULATED_COST",5,"mock")
            summary=s.summary()
            self.assertEqual(summary["simulated_net_usd"],15)
            self.assertEqual(summary["verified_cash_usd"],0.0)
    def test_store_rejects_infinite_amount(self):
        with tempfile.TemporaryDirectory() as d:
            s=Store(str(Path(d)/"dae.db")); s.add_agent("a1","demo")
            with self.assertRaises(ValueError): s.record_simulation("a1","SIMULATED_COST",math.inf)
    def test_snapshot_rejects_nan(self):
        with self.assertRaises(ValueError): EconomicSnapshot(math.nan,0)

if __name__=="__main__": unittest.main()
