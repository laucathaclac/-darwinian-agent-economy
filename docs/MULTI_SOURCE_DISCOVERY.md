# DAE v0.9 — Multi-source discovery

## Why this change
GitHub Issues is only one source and often has few real paid opportunities. v0.9 adds a zero-cost discovery layer for:
- X posts advertising paid coding work, bounties, freelance tasks, and creator campaigns.
- Public web-indexed Binance Square campaign/contest posts.
- Broader open-source/Web3 bounty, grant, and hackathon searches.

## Cost and safety
- Uses ordinary browser search links; no X API reads, paid API calls, undocumented Binance endpoints, or scraping.
- This is a discovery index, not a live crawler. It does **not** claim to have found or verified any active reward until a human opens a result and checks the official terms.
- Do not count a headline reward pool as funded money. Check funder identity, actual funding, terms, deadline, acceptance criteria, age/location eligibility, and payout method.
- Never pay an application fee, reveal seed phrases/private keys, or connect a wallet merely to claim a prize.
- The tool never accepts tasks, submits work, contacts clients, executes untrusted code, or spends funds.

## Run on Windows
From the repository root:
```bat
python scripts\dae_external_source_discovery.py
```
It creates:
- `reports\external_source_searches.md`
- `reports\external_source_searches.json`

Then open the search links manually and only add opportunities to the shortlist after checking the original official terms. X API reading is intentionally not enabled because it can incur usage charges. Binance Square is searched via a public web search instead of an undocumented API.

## Honest limitation
This version increases source coverage, not verified opportunity count. Funding remains unverified until evidence is collected from the original program and independently reviewed.
