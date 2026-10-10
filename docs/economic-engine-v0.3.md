# DAE Economic Engine v0.3

## Objective

Optimize for **verified net cash flow and survival**, not task count, model output volume, or speculative token balances.

## Economic decision rule

For an opportunity:

- Expected gross revenue = reward × probability of successful completion × probability of payment conditional on success.
- Expected cost = compute + labor/time opportunity cost + platform fees + probability-weighted failure cost.
- Expected net value = expected gross revenue − expected cost.
- Margin = expected net value / expected gross revenue.
- Risk-adjusted value applies a haircut to expected net value.

The probabilities are estimates, not facts. The engine is a screening tool, not a guarantee of payment. Unknown or unverified rewards should be assigned a low payment probability or rejected.

## Capital allocation

Default allocation of **verified positive surplus**:
- 50% reserve/runway
- 30% operations
- 20% growth experiments

These are starting parameters for simulation and should be recalibrated against observed cash flows. No allocation causes a transfer or authorizes spending.

## Survival and reproduction

A replication proposal is eligible only after:
- at least 10 verified paid tasks,
- positive verified net profit,
- at least 30% profit margin,
- zero policy violations.

Eligibility does not create or fund another agent. Human review remains required. The thresholds are conservative initial hypotheses, not empirically validated universal constants.

## Evidence ledger

Claimed revenue and verified revenue are recorded separately. Only evidenced, verified revenue counts toward verified cash flow. Costs are logged independently, including failed attempts. Do not count a bounty listing, an accepted submission, a token allocation, or an unpaid invoice as cash.

## Safety boundary in this release

This module is local and deterministic. It does not:
- browse or accept tasks automatically,
- submit work to third-party services,
- hold or transfer funds,
- spend on APIs,
- trade assets,
- create child agents,
- modify its own code.

Those capabilities require separate adapters, explicit authorization, sandboxing, and test evidence before activation.

## First revenue experiment

Pick one service that can be delivered and independently verified (for example, repository QA, data cleanup, or structured research). Start with read-only opportunity discovery. Record every cost. Require payment evidence before revenue is marked verified. Stop if the cumulative experiment budget is exhausted or after a predeclared number of attempts without positive net results.
