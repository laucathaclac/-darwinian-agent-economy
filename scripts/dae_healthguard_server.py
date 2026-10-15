"""Small standard-library HTTP API for DAE HealthGuard.

Local-first by default. This API assesses caller-supplied normalized snapshots;
it does not fetch live lending positions or execute transactions.
"""
from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dae.healthguard import assess_json  # noqa: E402

PUBLIC_URL = os.getenv("DAE_PUBLIC_URL", "http://127.0.0.1:8788").rstrip("/")
MAX_BODY_BYTES = 16_384
AGENT_CARD = {
    "name": "DAE HealthGuard",
    "description": "Read-only lending-position health-factor assessment from a supplied, timestamped snapshot. No custody, signing, or transaction execution.",
    "url": PUBLIC_URL,
    "version": "0.2.0",
    "provider": {
        "organization": "BlueTokenCapital",
        "url": "https://github.com/laucathaclac/-darwinian-agent-economy",
    },
    "capabilities": {"streaming": False, "pushNotifications": False},
    "skills": [{
        "id": "lending-health-factor-assessment",
        "name": "Lending health-factor assessment",
        "description": "Classify a normalized collateral/debt snapshot and reject stale or future data.",
        "tags": ["BNB Chain", "DeFi", "health-factor-monitoring", "risk-monitoring"],
        "examples": [{
            "input": {"position": {
                "collateral_value": 1000, "debt_value": 500,
                "liquidation_threshold": 0.8,
                "observed_at": "2026-10-15T12:00:00+00:00",
                "source": "example-only"
            }},
            "output": {"status": "UNKNOWN", "transaction_executed": False}
        }]
    }],
    "safety": {
        "read_only": True, "signs_transactions": False,
        "broadcasts_transactions": False, "custodies_funds": False,
    },
    "limitations": [
        "Input snapshot is supplied by the caller and is not verified against a live protocol.",
        "This service is decision support, not a liquidation guarantee or financial advice.",
    ],
}


class Handler(BaseHTTPRequestHandler):
    server_version = "DAEHealthGuard/0.2"

    def _send(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self._send(200, {"ok": True, "service": "DAE HealthGuard", "read_only": True})
        elif path in ("/", "/.well-known/agent-card.json"):
            self._send(200, AGENT_CARD)
        else:
            self._send(404, {"error": "not_found"})

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/v1/assess":
            self._send(404, {"error": "not_found"})
            return
        try:
            raw_length = self.headers.get("Content-Length", "")
            if not raw_length.isdigit():
                self._send(400, {"error": "content_length_required"})
                return
            length = int(raw_length)
            if length <= 0 or length > MAX_BODY_BYTES:
                self._send(413 if length > MAX_BODY_BYTES else 400,
                           {"error": "body_size_invalid"})
                return
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            result = assess_json(payload)
            self._send(200, result)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
            self._send(400, {"error": "invalid_request", "message": str(exc),
                             "transaction_executed": False})
        except Exception:
            self._send(500, {"error": "internal_error", "transaction_executed": False})

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.log_date_time_string(), fmt % args))


def main() -> None:
    host = os.getenv("DAE_HOST", "127.0.0.1")
    port = int(os.getenv("DAE_PORT", "8788"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"DAE HealthGuard API listening on http://{host}:{port}")
    print("Endpoints: GET /health, GET /.well-known/agent-card.json, POST /v1/assess")
    print("Local-only default; do not expose publicly until deployment security is reviewed.")
    server.serve_forever()


if __name__ == "__main__":
    main()
