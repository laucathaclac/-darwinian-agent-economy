# DAE release gate checklist

This checklist is the single release gate. A release is not considered complete until every required item is evidenced.

## Automated gates
- [ ] GitHub Actions pass on Windows and Ubuntu for Python 3.11 and 3.12.
- [ ] All unit tests pass from a clean checkout.
- [ ] Python modules compile.
- [ ] CLI demo exits successfully.
- [ ] Windows launchers preserve output and pause on completion/failure.
- [ ] Scanner/advisor can fail safely on rate limit, timeout, malformed response, missing report, and empty results.
- [ ] Generated Markdown, JSON, and CSV are valid UTF-8 and contain honest source/status metadata.

## Product/data gates
- [ ] Each candidate links to its primary source and records the retrieval/update timestamp where available.
- [ ] Duplicate links are removed.
- [ ] Reward amount is labelled as claimed, never independently verified unless evidence supports it.
- [ ] No win probability is fabricated from a completeness score.
- [ ] Expired or stale opportunities are flagged where the source exposes reliable dates.
- [ ] X and Binance Square search-link mode is not described as a live crawler.
- [ ] No paid API calls are made by default.
- [ ] No tasks are accepted, submitted, executed, or paid for automatically.

## Release/marketplace gates
- [ ] Version, changelog, README, CLI behavior, and ZIP all refer to the same commit.
- [ ] License and third-party/source terms are reviewed.
- [ ] No secrets, personal data, generated reports, or local state are packaged.
- [ ] Clean Windows extraction test succeeds without manual file editing.
- [ ] Release ZIP hash is recorded.
- [ ] Marketplace listing clearly states limitations and does not promise income.
- [ ] Target program eligibility and submission rules are checked before submitting.

## Current status
This repository is a local-first MVP/release candidate, not an audited production SaaS. Funding verification, robust direct X/Square integrations, hosted service operations, customer validation, SLA, and security audit remain out of scope until implemented and evidenced. Do not mark these boxes complete without proof.
