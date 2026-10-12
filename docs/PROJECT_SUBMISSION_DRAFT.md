# DAE — Project Submission Package (Draft)

**Status: prepared draft only; not submitted.**

## Project
Darwinian Agent Economy (DAE) — a safety-first opportunity intelligence and economic decision layer for AI-agent work.

## Problem
Public bounty and freelance opportunities are fragmented. Reward headlines can be ambiguous, deadlines and eligibility can be missed, and proposed reward pools are often mistaken for guaranteed cash.

## Solution
DAE gathers candidate paid-task leads from public GitHub issue search, adds discovery links for other platforms, ranks evidence completeness transparently, flags common scam language, and exports an auditable shortlist. It does not autonomously accept tasks or move funds.

## Differentiation
- Explainable score with explicit disclaimer that it is not win probability.
- Every reward claim remains UNVERIFIED until manually checked.
- Human approval and read-only boundaries by default.
- Local-first operation and CSV/JSON/Markdown exports.

## Current implementation
- Public GitHub Issues GET-only scanner.
- Simple deterministic amount/deadline/payment-term extraction.
- Deduplication by URL and triage labels.
- Markdown, JSON, CSV outputs.
- Search-link generator for X, Binance Square, and wider bounty searches.
- Unit tests and Windows CMD launchers.

## Evidence and limitations
- Local tests included in the ZIP; must also pass on the user's target Windows system and in CI.
- Public-source data is not independently verified funding.
- No hosted endpoint, ERC-8004 identity, marketplace listing, independent customer hires, or real revenue is claimed.
- Not production audited; no SLA or hosted service.

## Next proof points
1. Publish CI status and versioned release.
2. Collect real user feedback and measure false-positive rate.
3. Add source snapshots and reviewer-confirmed payout evidence.
4. Deploy a monitored read-only hosted demo only after security and privacy review.
5. Submit only after checking the specific program's eligibility and requirements.

## Eligibility gate
Check the target program's official rules before submission. The BNB Chain Set and Earn campaign rules in the repository state participants must be 18 or older; do not misstate age or eligibility. This draft is not a campaign submission and makes no claim that requirements have been fulfilled.
