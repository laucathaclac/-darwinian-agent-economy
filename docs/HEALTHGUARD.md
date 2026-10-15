# DAE HealthGuard — MVP handover

## Purpose
A deterministic health-factor assessment core for a BNB Chain lending-monitoring agent. It validates normalized position inputs, rejects stale/future observations, calculates health factor, classifies risk, and emits a JSON report.

## Implemented
- Input validation for finite, non-negative collateral/debt values and liquidation threshold.
- Configurable warning/critical/urgent thresholds.
- Health factor calculation: collateral value × liquidation threshold ÷ debt value.
- Fail-closed UNKNOWN status for stale or future observations.
- NO_DEBT state when debt value is zero.
- Machine-readable recommendations and explicit transaction_executed=false.
- Offline CLI and deterministic unit tests.

## Not implemented
- No live BNB RPC/indexer or protocol adapter.
- No live lending protocol integration.
- No wallet, private key, transaction signing, or transaction submission.
- No hosted endpoint, ERC-8004 registration, public agent card, TermiX order adapter, or verified campaign evidence.
- Example JSON is a fixture, not live data.

Do not represent this MVP as a live autonomous financial agent until those integrations have been implemented and tested. The monitoring core cannot guarantee avoidance of liquidation.

## Run on Windows
From the repository root:

```bat
py -3 -m unittest discover -s tests -v
py -3 scripts\dae_healthguard.py examples\healthguard_position.json
py -3 scripts\dae_healthguard.py examples\healthguard_position.json --output reports\healthguard_demo.json
```

The sample is intentionally dated and will eventually be rejected as stale. Replace observed_at with a current ISO-8601 timestamp including timezone before expecting a fresh assessment.

## Output semantics
- HEALTHY: above configured warning threshold.
- WARNING, CRITICAL, URGENT: increasing levels of attention.
- LIQUIDATION_THRESHOLD_REACHED: computed health factor ≤ 1.0; verify protocol-specific liquidation rules.
- NO_DEBT: debt value is zero.
- UNKNOWN: data is stale or future-dated; refresh before acting.

Recommendations are advisory. This module never executes a transaction.
