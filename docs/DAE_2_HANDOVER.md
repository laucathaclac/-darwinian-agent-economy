# DAE 2.0 — build status and handover plan

## Product direction
DAE HealthGuard: a health-factor monitoring agent for supported lending positions on BNB Smart Chain. This direction maps to the health-factor monitoring category named in the Set and Earn program materials.

## Implemented in this change
- src/dae/healthguard.py: deterministic health-factor calculation, validation, risk classification, and freshness checks.
- scripts/dae_healthguard.py: Windows-compatible offline CLI.
- tests/test_healthguard.py: unit tests for healthy, warning, critical, urgent, liquidation-threshold, stale, future, zero-debt, invalid-input, and no-transaction cases.
- examples/healthguard_position.json: labelled demo fixture.
- docs/HEALTHGUARD.md: operating instructions and limitations.

## Acceptance gates for a real hackathon-ready product
1. Connect a maintained BNB Chain data source and a named lending protocol; document supported markets and oracle/decimals handling.
2. Add integration tests against known protocol fixtures and, where possible, a testnet deployment.
3. Build a reachable agent API with health checks, authentication/rate limits, and uptime monitoring.
4. Register the original agent in ERC-8004 and publish a resolvable agent card with accurate category and endpoint.
5. Integrate an approved marketplace and verify orders, deliveries, and qualifying on-chain hire events.
6. Verify at least three independent completed hires and at least five category-consistent on-chain actions across three separate days using explorer receipts and campaign records.
7. Add a safety-reviewed execution adapter only if required; default to alerts/advice and never hold user keys. Any transaction feature must use explicit delegated permissions, spend caps, simulation, and emergency stop.
8. Run CI on Windows and Linux, package a reproducible release, and create a demo/video plus submission narrative.

## Honest status
This branch implements a local assessment core, not a live deployed agent. It does not yet meet the complete campaign build/hire requirements. Do not claim live chain integration, registry identity, marketplace listing, independent hires, transactions, or revenue without evidence.

## Campaign evidence log
Append only verified evidence:
- Date/time UTC:
- Network / chain ID:
- ERC-8004 registry ID:
- Agent card URL:
- Marketplace listing:
- Hire order IDs and independent-wallet proof:
- Transaction hashes and explorer URLs:
- Category-consistent action descriptions:
- Verification status:
