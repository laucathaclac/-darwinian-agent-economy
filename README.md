# Darwinian Agent Economy (DAE)

**DAE is a safety-first, local-first opportunity research and agent-economics prototype.** It combines a deterministic simulation core with read-only public GitHub issue discovery, transparent triage, and search links for other public opportunity ecosystems.

> **Current status:** release candidate / research MVP, not a production SaaS. Reward claims are not independently verified. No guaranteed income, autonomous work acceptance, client contact, task execution, wallet signing, payment, or spending is performed.

## Quick start — Windows

1. Download the ZIP from the repository's Releases page (when a release is published) or download the repository source.
2. Extract to a normal writable folder, e.g. `C:\\DAE`.
3. Install Python 3.11 or newer from https://www.python.org/downloads/windows/ and enable **Add Python to PATH**.
4. Double-click `TEST_DAE.bat`; keep the window open and confirm the tests pass.
5. Double-click `RUN_DAE.bat` to run the read-only scanner, advisor, and external search-link generator.
6. Open `reports\\hourly_opportunity_brief.md` and `reports\\external_source_searches.md`.

If the batch files do not run, open CMD in the extracted folder and use:

```bat
py -3 --version
py -3 -m unittest discover -s tests -v
py -3 -m dae.cli demo
py -3 scripts\\dae_hourly_scan.py
py -3 scripts\\dae_opportunity_advisor.py
py -3 scripts\\dae_external_source_discovery.py
```

Install the local package only if you want the `dae` CLI command:

```bat
py -3 -m pip install -e .
dae demo
```

## What runs where

- `src/dae/`: deterministic task scoring, policy gates, economic simulation and human-reviewed evolution decisions.
- `scripts/dae_hourly_scan.py`: GET-only search of public GitHub Issues. It creates candidate leads and never accepts or submits a task.
- `scripts/dae_opportunity_advisor.py`: triage report based on scanner output. It does not independently verify funders, payout terms, or win probability.
- `scripts/dae_external_source_discovery.py`: generates search links for X, Binance Square via public web search, and broader bounty/grant/hackathon searches. These are **search links, not live crawlers or verified opportunities**.
- `reports/`: generated local reports; reports are not committed by default.

## Interpreting results

- `UNVERIFIED` means there is no independent proof that a reward is funded.
- Triage/evidence scores measure information completeness for review. They are **not** probability of winning or being paid.
- A reward pool paid in tokens is not automatically cash revenue.
- Check original terms, funder identity, actual funding, acceptance criteria, deadline/timezone, age and location eligibility, payout method, tax, and IP/license terms before investing time.
- Never pay an upfront fee, send crypto to unlock a reward, disclose a seed phrase/private key, or run untrusted task code.

## Safety boundaries

DAE is read-only by default. It does not trade, transfer assets, sign wallet transactions, spend money, create accounts, contact clients, accept tasks, submit work, or execute third-party code. Hourly scheduling is optional and must be enabled by the user; it is not enabled automatically.

## Quality and release status

See:
- [Commercial readiness assessment](docs/COMMERCIAL_READINESS.md)
- [Hourly scanner documentation](docs/HOURLY_SCAN.md)
- [Opportunity advisor documentation](docs/OPPORTUNITY_ADVISOR.md)
- [Multi-source discovery limitations](docs/MULTI_SOURCE_DISCOVERY.md)
- [Project submission draft](docs/PROJECT_SUBMISSION_DRAFT.md)
- [Marketplace listing draft](docs/MARKETPLACE_LISTING_DRAFT.md)
- [Release gate checklist](docs/RELEASE_GATE.md)
- [Set and Earn readiness checklist](docs/SET_AND_EARN_READINESS.md)

A green CI run confirms the tested code paths on the listed runners; it does not prove market demand, payout reliability, production security, marketplace acceptance, or eligibility for a hackathon. See the official rules before applying. The current Set and Earn readiness notes say participants must be at least 18; do not misrepresent eligibility.

## Development

```bat
py -3 -m pip install -e .
py -3 -m unittest discover -s tests -v
py -3 -m dae.cli demo
```

No paid APIs or third-party Python runtime packages are required by the current scanner scripts. Public endpoints may rate-limit or change; failures should be treated as incomplete discovery, not as proof that no opportunities exist.


## BNB Chain integration (testnet, read-only)

DAE now includes an initial **read-only BNB Smart Chain testnet adapter**. It can verify the RPC network/chain ID, read the latest block, and optionally inspect a public address's native BNB balance. It does not sign or broadcast transactions.

```bat
py -3 scripts\dae_bnb_testnet_check.py
py -3 scripts\dae_bnb_testnet_check.py --address 0xYourPublicAddress
py -3 -m unittest discover -s tests -v
```

The default endpoint is the public BSC testnet RPC (chain ID 97). To use another endpoint, set `DAE_BSC_TESTNET_RPC` or pass `--rpc`. Do not put private keys, seed phrases, or wallet credentials in command-line arguments, source files, or GitHub. Real transaction execution is deliberately not enabled: it requires a separately reviewed signing flow, explicit human approval, transaction simulation, recipient/contract allowlists, and strict spend limits.
