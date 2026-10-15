"""HTTP contract tests for the local HealthGuard service."""
from __future__ import annotations

import json
import sys
import threading
import unittest
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import dae_healthguard_server as service  # noqa: E402


class HealthGuardServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), service.Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request_json(self, path, payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        req = Request(self.base + path, data=data,
                      headers={"Content-Type": "application/json"} if data else {},
                      method="POST" if data else "GET")
        try:
            with urlopen(req, timeout=3) as response:
                return response.status, json.loads(response.read())
        except HTTPError as exc:
            return exc.code, json.loads(exc.read())

    def test_health_and_agent_card(self):
        status, health = self.request_json("/health")
        self.assertEqual(status, 200)
        self.assertTrue(health["read_only"])
        status, card = self.request_json("/.well-known/agent-card.json")
        self.assertEqual(status, 200)
        self.assertEqual(card["name"], "DAE HealthGuard")
        self.assertFalse(card["safety"]["signs_transactions"])

    def test_assess_endpoint_returns_machine_readable_result(self):
        now = datetime.now(timezone.utc).isoformat()
        status, result = self.request_json("/v1/assess", {"position": {
            "collateral_value": 1000, "debt_value": 500,
            "liquidation_threshold": 0.8, "observed_at": now,
            "source": "unit-test"
        }})
        self.assertEqual(status, 200)
        self.assertEqual(result["status"], "HEALTHY")
        self.assertFalse(result["transaction_executed"])

    def test_invalid_payload_fails_closed(self):
        status, result = self.request_json("/v1/assess", {"position": {}})
        self.assertEqual(status, 400)
        self.assertFalse(result["transaction_executed"])

    def test_unknown_route_is_not_found(self):
        status, result = self.request_json("/missing")
        self.assertEqual(status, 404)
        self.assertEqual(result["error"], "not_found")


if __name__ == "__main__":
    unittest.main()
