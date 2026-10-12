"""Minimal standard-library HTTP service for DAE Health Sentinel."""
from __future__ import annotations
import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from dae.health_sentinel import SentinelError, monitor_account

AGENT_URL = os.getenv("AGENT_PUBLIC_URL", "http://127.0.0.1:8787")
AGENT_CARD = {
    "name":"DAE Health Sentinel",
    "description":"Read-only Venus Core Pool liquidation-risk monitoring on BNB Smart Chain. Reports account liquidity and shortfall; it does not custody funds or transact.",
    "url":AGENT_URL,"version":"0.1.0",
    "provider":{"organization":"BlueTokenCapital","url":"https://github.com/laucathaclac/-darwinian-agent-economy"},
    "capabilities":{"streaming":False,"pushNotifications":False},
    "skills":[{"id":"venus-liquidation-risk-monitor","name":"Venus liquidation-risk monitor",
      "description":"Read Venus Core Pool account liquidity and shortfall for a public EVM address.",
      "tags":["BNB Chain","Venus","health-factor-monitoring","risk-monitoring"],
      "examples":[{"input":{"account":"0x..."},"output":{"status":"OK","liquidity_buffer_usd":1000}}]}],
    "safety":{"read_only":True,"signs_transactions":False,"broadcasts_transactions":False,"custodies_funds":False}
}

class Handler(BaseHTTPRequestHandler):
    server_version = "DAEHealthSentinel/0.1"
    def _send(self, status, payload):
        body = json.dumps(payload, separators=(",",":"), ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(body)))
        self.send_header("Cache-Control","no-store")
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            self._send(200,{"ok":True,"service":"DAE Health Sentinel","read_only":True})
        elif path in ("/","/.well-known/agent-card.json"):
            self._send(200,AGENT_CARD)
        else:
            self._send(404,{"error":"not_found"})
    def do_POST(self):
        if urlparse(self.path).path != "/v1/monitor":
            self._send(404,{"error":"not_found"}); return
        try:
            length = int(self.headers.get("Content-Length","0"))
            if length <= 0 or length > 16384:
                self._send(400,{"error":"body_size_invalid"}); return
            payload = json.loads(self.rfile.read(length).decode())
            if not isinstance(payload,dict):
                self._send(400,{"error":"json_object_required"}); return
            self._send(200,monitor_account(payload.get("account","")))
        except (ValueError,json.JSONDecodeError) as exc:
            self._send(400,{"error":"invalid_request","message":str(exc)})
        except SentinelError as exc:
            self._send(503,{"error":"monitor_unavailable","message":str(exc)})
        except Exception:
            self._send(500,{"error":"internal_error"})
    def log_message(self, format, *args):
        print("%s - %s" % (self.log_date_time_string(),format % args))

if __name__ == "__main__":
    host, port = os.getenv("DAE_HOST","127.0.0.1"), int(os.getenv("PORT", os.getenv("DAE_PORT","8787")) )
    print(f"DAE Health Sentinel listening on http://{host}:{port} (read-only)")
    ThreadingHTTPServer((host,port),Handler).serve_forever()
