# DAE v0.6.0 — consolidated rebuild

- Standalone Task Hunter retained.
- Added SQLite simulation ledger and economic snapshot helper.
- Tightened policy: finite values, minimum expected net, minimum margin, and risk-adjusted net gate.
- Verified cash remains zero; simulation cannot mark cash verified.
- Read-only discovery only. No acceptance/submission, wallet, signing, spending, trading, or autonomous replication.
