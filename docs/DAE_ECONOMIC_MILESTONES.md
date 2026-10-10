# Darwinian Agent Economy — Economic Milestones

## Milestone 1 — Measurement (this release)
- [x] Expected-value screening
- [x] Upfront-payment rejection by default
- [x] Separate claimed revenue from verified revenue
- [x] Cost ledger and net cash-flow summary
- [x] Capital allocation simulation
- [x] Replication eligibility gate
- [x] Tests for invalid numbers and evidence rules

## Milestone 2 — Read-only opportunity hunter
- Connect one public task source at a time.
- Respect robots, API terms, rate limits, and authentication rules.
- Store source URL, retrieval time, deadline, eligibility, reward currency, and proof of payment terms.
- Deduplicate by stable source ID.
- Never treat listing text as evidence of payment.

## Milestone 3 — One human-approved service
- Choose one deliverable with clear acceptance criteria.
- Generate a draft or patch in a restricted workspace.
- Run deterministic tests before human review.
- Require approval before submission or any external communication.
- Reconcile payout evidence against ledger.

## Milestone 4 — Verified unit economics
- At least 10 completed paid tasks.
- Positive net cash flow after compute, fees, and labor opportunity cost.
- Track success rate, median time-to-payment, refund/dispute rate, and profit margin.
- Stop or change strategy if the predefined loss limit is hit.

## Milestone 5 — Controlled evolution
- Compare strategy cohorts on verified net profit, not self-reported confidence.
- Keep an immutable audit trail and a rollback path.
- Propose strategy changes; test in simulation first.
- Replication is a reviewed proposal only; never auto-fund offspring.

## Release acceptance criteria
- Tests pass in CI.
- No secrets in repository.
- No live payment or wallet credentials.
- No autonomous external submissions, spending, trading, or replication.
