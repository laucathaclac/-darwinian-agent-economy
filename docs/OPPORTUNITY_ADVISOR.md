# DAE Opportunity Advisor v0.8

After the read-only hourly scanner, run `python scripts/dae_opportunity_advisor.py`. It reads `reports/hourly_latest.json` and writes:

- `reports/hourly_advice.json`: structured assessment per lead
- `reports/hourly_opportunity_brief.md`: human-readable brief with participation checklist, risks, evidence notes and recommendation

The advisor uses only Python's standard library. It does not browse additional sources and therefore does not independently verify funding, eligibility, competition, judging rules or payment. All funding remains `UNVERIFIED`; numeric win probability is deliberately withheld where competition/judging evidence is missing. Its payment evidence score (0–20) is an evidence-completeness heuristic, not a probability of payment. Net value/hour is not estimated unless reward, work hours, fees and payout likelihood can be supported by evidence.

No tasks are claimed, accepted, submitted, executed, or sent to clients. The user decides whether to participate.
