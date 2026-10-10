# Set and Earn: DAE readiness and evidence checklist

Last reviewed: 2026-10-10. Official campaign: [BNB Chain Set and Earn](https://www.bnbchain.org/en/hackathons/smart-money-era-set-and-earn).

## Important eligibility gate

The official rules state participants must be **18 or over**. Check eligibility and all location/other restrictions before registering, deploying, paying for hires, or submitting. Do not misstate age or eligibility.

## Official qualifying requirements

Campaign window: **1 October 2026 through 5 November 2026 at 12:00 UTC**. The campaign requires both a hire track and a build track.

### Hire track
- Register the campaign wallet before completing campaign tasks.
- Hire at least three different agents across at least two shortlisted marketplaces.
- Each hire must emit a qualifying on-chain hire event; token approvals alone do not count.
- Mainnet and testnet hires count under the published rules.

### Build track
- Register an original agent on the ERC-8004 Identity Registry on BNB Smart Chain mainnet (chain ID 56) or testnet (chain ID 97).
- The registered campaign wallet must own the agent.
- List it on a shortlisted marketplace.
- Publish a resolvable agent card at its registered domain that describes its purpose and category: yield, grid, rebalancing, or health-factor monitoring.
- Keep the agent live and responsive to calls.
- Obtain at least three completed hires from three distinct independent wallets that are not yours and not funded by yours.
- Perform at least five on-chain actions across at least three separate days; actions must match the agent's stated category.
- Keep this repository public and show the registry ID and chain once actually verified.

## Current repository status (honest snapshot)

| Requirement | Status | Evidence |
|---|---|---|
| Public GitHub repository | Implemented | This repository is public |
| Core scoring and budget policy | Implemented in code | `src/dae/` |
| Unit tests and GitHub Actions workflow | Configured | `tests/test_dae.py`, `.github/workflows/tests.yml` |
| Task-source integration | Not implemented | Roadmap |
| Live hosted agent endpoint/card | Not implemented | No public endpoint registered yet |
| ERC-8004 registry ID and ownership proof | Not implemented / not verified | No ID claimed |
| Marketplace listing | Not implemented / not verified | No listing claimed |
| Three qualifying independent completed hires | Not implemented / not verified | No hire evidence claimed |
| Five category-consistent on-chain actions across three days | Not implemented / not verified | No transaction evidence claimed |
| Real revenue | Not established | Current demo is simulation only |

## Evidence log template

When a requirement is genuinely completed, add evidence here with:
- UTC timestamp
- Network and chain ID
- Registry ID / marketplace listing URL
- Transaction hash and explorer URL (where relevant)
- A short description of what the evidence proves
- Whether it is testnet or mainnet

Never publish private keys, seed phrases, API secrets, or personal data. Never create circular or self-funded hires to imitate independent usage; the campaign rules explicitly exclude such behavior.

## References

- [Official Set and Earn campaign and rules](https://www.bnbchain.org/en/hackathons/smart-money-era-set-and-earn)
- [Official BNB Chain announcement](https://www.bnbchain.org/en/blog/set-and-earn-hire-and-build-ai-agents-on-bnb-chain-win)
