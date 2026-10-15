# DAE HealthGuard HTTP API

## Runtime choice

The runtime is currently unknown, so this MVP uses Python's standard-library HTTP server and has no web-framework dependency. It binds to localhost by default and can run from Windows CMD. This gives the project a testable service boundary without pretending it is already linked to TermiX.

## Start locally (Windows CMD)

```bat
py -3 -m unittest discover -s tests -v
py -3 scripts\dae_healthguard_server.py
```

Default base URL: `http://127.0.0.1:8788`.

- `GET /health` — process health.
- `GET /.well-known/agent-card.json` — public agent-card-shaped metadata.
- `POST /v1/assess` — assess a normalized JSON position snapshot.

Example request body:

```json
{
  "position": {
    "collateral_value": 1000,
    "debt_value": 500,
    "liquidation_threshold": 0.8,
    "observed_at": "2026-10-15T12:00:00+00:00",
    "source": "manual-test-fixture"
  }
}
```

Use a current timezone-aware `observed_at`; stale/future data returns `UNKNOWN`. The server accepts a maximum request body of 16 KiB. Errors fail closed. Responses explicitly state `transaction_executed: false`.

## Important limitation

The HTTP API currently evaluates caller-supplied normalized data. It does **not** fetch a user's lending positions from BNB Chain or a lending protocol. The read-only BSC Testnet RPC checker is a separate connectivity component, not a lending-market adapter. Do not expose this service to the public internet or list it as a live risk monitor until authentication/rate limits, a verified protocol adapter, deployment, and end-to-end tests are completed.
