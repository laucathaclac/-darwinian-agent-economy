# Darwinian Agent Economy (DAE)

A safety-first MVP for discovering candidate tasks, scoring opportunities, simulating outcomes, and deciding whether an agent should continue, pause, or qualify for a human-reviewed replication.

> **Stage:** local simulation and read-only research scaffold. No wallet, private-key, payment, or autonomous spending integration is included.

## Principles

- **Earn before expanding:** replication is only considered after repeated, verified positive net results.
- **Hard limits:** explicit per-task and daily budget caps.
- **Fail closed:** malformed or incomplete tasks are rejected rather than guessed.
- **Auditable decisions:** each candidate receives a transparent score and rejection reasons.
- **Human approval:** replication is a recommendation, never an automatic action.

## Requirements

- Python 3.11+
- No third-party runtime dependencies

## Run on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
dae demo
python -m unittest discover -s tests -v
```

Without installing the package:

```powershell
$env:PYTHONPATH = "src"
python -m dae.cli demo
```

## Modules

- `dae.models` — task, policy, score and agent history models
- `dae.scoring` — explainable opportunity scoring
- `dae.policy` — safety gates and budget checks
- `dae.evolution` — continue, pause, or replication-review decisions
- `dae.cli` — deterministic local demo

Scores prioritize candidates; they do not guarantee income. A passing test suite demonstrates code behavior, not market demand or profitability.

## Safety boundaries

- No trading, transfers, wallet signing, or autonomous payments.
- No automatic task execution or account creation.
- Third-party task listings are untrusted; verify terms and payout evidence independently.
- Never commit API keys, seed phrases, private keys, or passwords.

## Roadmap

- [x] Deterministic task scoring and safety policy
- [x] Simulated agent outcomes and replication review
- [x] Unit tests for core policy and evolution behavior
- [ ] Read-only task-source adapters
- [ ] Durable event log and CSV report export
- [ ] Sandboxed task execution after threat modelling and explicit approval


## Campaign readiness

See [Set and Earn readiness and evidence checklist](docs/SET_AND_EARN_READINESS.md) for the official requirements, current implementation status, and evidence log. Eligibility must be checked before participation; the official campaign requires participants to be 18 or over.


## v0.6 consolidation branch
This branch adds a simulation-only SQLite ledger (dae.store.Store), an economic snapshot validator, and a fail-closed policy gate for invalid inputs, excessive per-task cost, low confidence, excessive risk, low expected net, or negative risk-adjusted net. The ledger explicitly reports verified cash as zero and never processes payments.

The Task Hunter ZIP distributed with this branch is a self-contained read-only discovery package. Public-source adapter tests are mocked; live API behavior and any payout are not guaranteed. No task acceptance/submission, wallet/signing, spending, trading, or autonomous replication is enabled.
