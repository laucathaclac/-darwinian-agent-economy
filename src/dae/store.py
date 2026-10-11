"""SQLite persistence for the DAE simulation ledger; never handles payments."""
from __future__ import annotations
import json, math, sqlite3
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS agents (
 agent_id TEXT PRIMARY KEY, name TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'SIMULATED',
 created_at TEXT NOT NULL, metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS ledger (
 entry_id INTEGER PRIMARY KEY AUTOINCREMENT, agent_id TEXT NOT NULL,
 kind TEXT NOT NULL CHECK(kind IN ('SIMULATED_REVENUE','SIMULATED_COST','NOTE')),
 amount_usd REAL NOT NULL, verified INTEGER NOT NULL DEFAULT 0 CHECK(verified IN (0,1)),
 memo TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL,
 FOREIGN KEY(agent_id) REFERENCES agents(agent_id)
);
CREATE TABLE IF NOT EXISTS opportunities (
 task_id TEXT PRIMARY KEY, source TEXT NOT NULL, title TEXT NOT NULL,
 expected_net REAL, risk_adjusted_net REAL, status TEXT NOT NULL DEFAULT 'DISCOVERED',
 evidence_json TEXT NOT NULL DEFAULT '{}', updated_at TEXT NOT NULL
);
"""
class Store:
    def __init__(self, path="data/dae.db"):
        self.path = Path(path); self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db: db.executescript(SCHEMA)
    def connect(self):
        db = sqlite3.connect(self.path); db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON"); return db
    @staticmethod
    def now(): return datetime.now(timezone.utc).isoformat()
    def add_agent(self, agent_id, name, metadata=None):
        with self.connect() as db:
            db.execute("INSERT OR IGNORE INTO agents(agent_id,name,created_at,metadata_json) VALUES(?,?,?,?)",(agent_id,name,self.now(),json.dumps(metadata or {})))
    def record_simulation(self, agent_id, kind, amount_usd, memo=""):
        if kind not in {"SIMULATED_REVENUE","SIMULATED_COST","NOTE"}: raise ValueError("Only simulated ledger entries and notes are allowed")
        if not isinstance(amount_usd,(int,float)) or isinstance(amount_usd,bool) or not math.isfinite(amount_usd) or amount_usd < 0: raise ValueError("amount_usd must be finite and non-negative")
        with self.connect() as db:
            db.execute("INSERT INTO ledger(agent_id,kind,amount_usd,verified,memo,created_at) VALUES(?,?,?,?,?,?)",(agent_id,kind,float(amount_usd),0,memo,self.now()))
    def summary(self):
        with self.connect() as db:
            agents=db.execute("SELECT COUNT(*) n FROM agents").fetchone()["n"]
            rows=db.execute("SELECT kind, COALESCE(SUM(amount_usd),0) amount FROM ledger GROUP BY kind").fetchall()
        totals={r["kind"]:round(r["amount"],2) for r in rows}
        rev,cost=totals.get("SIMULATED_REVENUE",0.0),totals.get("SIMULATED_COST",0.0)
        return {"agents":agents,"simulated_revenue_usd":rev,"simulated_cost_usd":cost,"simulated_net_usd":round(rev-cost,2),"verified_cash_usd":0.0,"warning":"Simulation ledger only; no real payment is processed or verified."}
