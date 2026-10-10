"""SQLite evidence ledger. Claimed revenue is separate from verified cash."""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class Ledger:
    def __init__(self, path: str | Path = "dae_ledger.sqlite3"):
        self.path = str(path)
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    opportunity_id TEXT NOT NULL,
                    amount REAL NOT NULL DEFAULT 0,
                    verified INTEGER NOT NULL DEFAULT 0,
                    evidence TEXT NOT NULL DEFAULT '',
                    payload_json TEXT NOT NULL DEFAULT '{}'
                )
            """)

    def record(self, event_type: str, opportunity_id: str, amount: float = 0,
               *, verified: bool = False, evidence: str = "",
               payload: dict[str, Any] | None = None) -> int:
        if not event_type.strip() or not opportunity_id.strip():
            raise ValueError("event_type and opportunity_id are required")
        if amount < 0 or amount != amount or amount == float("inf"):
            raise ValueError("amount must be finite and >= 0")
        if verified and (event_type != "revenue" or not evidence.strip()):
            raise ValueError("only evidenced revenue events can be verified")
        with self._connect() as db:
            cur = db.execute(
                "INSERT INTO events(timestamp,event_type,opportunity_id,amount,verified,evidence,payload_json) VALUES(?,?,?,?,?,?,?)",
                (datetime.now(timezone.utc).isoformat(), event_type, opportunity_id,
                 amount, int(verified), evidence, json.dumps(payload or {}, sort_keys=True)))
            return int(cur.lastrowid)

    def summary(self) -> dict[str, float | int]:
        with self._connect() as db:
            row = db.execute("""
                SELECT
                  COALESCE(SUM(CASE WHEN event_type='revenue' AND verified=1 THEN amount ELSE 0 END),0) AS verified_revenue,
                  COALESCE(SUM(CASE WHEN event_type='revenue' AND verified=0 THEN amount ELSE 0 END),0) AS claimed_revenue,
                  COALESCE(SUM(CASE WHEN event_type='cost' THEN amount ELSE 0 END),0) AS costs,
                  COUNT(*) AS event_count
                FROM events
            """).fetchone()
        revenue = float(row["verified_revenue"])
        costs = float(row["costs"])
        return {
            "verified_revenue": round(revenue, 2),
            "claimed_revenue": round(float(row["claimed_revenue"]), 2),
            "costs": round(costs, 2),
            "verified_net_cashflow": round(revenue - costs, 2),
            "event_count": int(row["event_count"]),
        }
