"""Simulation-only economic helpers."""
from dataclasses import dataclass
import math
from .store import Store
@dataclass(frozen=True)
class EconomicSnapshot:
    expected_net_usd: float
    risk_adjusted_net_usd: float
    realized_net_usd: float = 0.0
    verified_cash_usd: float = 0.0
    def __post_init__(self):
        values=(self.expected_net_usd,self.risk_adjusted_net_usd,self.realized_net_usd,self.verified_cash_usd)
        if not all(math.isfinite(x) for x in values): raise ValueError("Economic values must be finite")
        if self.verified_cash_usd < 0: raise ValueError("verified_cash_usd cannot be negative")
def summarize_store(path="data/dae.db"): return Store(path).summary()
