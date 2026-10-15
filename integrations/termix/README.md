# TermiX integration for DAE (BlueTokenCapital)

This integration connects DAE's opportunity research and bounded task-workflow to the TermiX marketplace on BNB Chain. It does **not** claim that the TermiX profile is already linked to a running DAE process.

## What is and is not integrated

- TermiX's official Agent Skill is the marketplace control plane for listing services, handling orders, and delivery.
- DAE remains the decision/work layer: discover opportunities, assess expected value and risk, create deliverables, run checks, and keep evidence.
- The TermiX skill must be installed inside the environment that actually runs the BlueTokenCapital agent. A repository change alone cannot install software into that remote runtime or approve wallet ownership.
- Do not paste wallet private keys, seed phrases, runtime tokens, or API secrets into chat, issues, logs, or GitHub.
- Do not enable unattended signing, staking, or value-bearing transactions as part of initial integration. Start with read-only marketplace inspection and dry-run workflows; allow order delivery only after verifying the task terms, acceptance criteria, and allowed tool scope.

## One-time setup in the TermiX agent runtime

Open the chat/console for the existing **BlueTokenCapital** agent and send:

```text
help me install http://termix.ai/skills?v=1.9.0
```

After the skill's own install verification, send:

```text
Link this terminal to my TermiX account on BSC. Show me the official approval page and wait for me to approve it. Do not request, print, or store my private key or seed phrase in chat.
```

Account linking and any wallet approval must happen in the official TermiX flow. This repository cannot perform that user-authorized step on your behalf.

## Configure the local DAE checkout

1. Use Python 3.11+ and Node.js 18+ in the machine where the agent runtime can reach both the DAE checkout and the TermiX skill.
2. Keep secrets in the runtime's local secret manager/environment, never in tracked files.
3. Set `AACP_CHAIN=bsc` using the official skill's configuration method. Do not independently override the API and RPC URLs unless following the official docs for the same chain.
4. Run DAE's existing scanner/advisor first. Current scanner findings are leads, not proof that a reward is funded.
5. Keep the first live test to one low-risk, no-upfront-fee task with explicit deliverables and a clear acceptance/payout condition.

## Target execution loop

1. **Hunt:** DAE scans permitted marketplace and public sources, deduplicates leads, and records source URLs/timestamps.
2. **Evaluate:** reject unclear eligibility, unfunded/ambiguous rewards, upfront fees, wallet-draining requests, and work outside configured risk/budget caps.
3. **Work:** generate a task plan and deliverables in an isolated workspace; run tests and secret/path checks; preserve hashes and logs.
4. **Deliver:** use the official TermiX skill workflow for the specific order. Never claim delivery succeeded until TermiX reports the corresponding order state.
5. **Collect:** reconcile the order and actual on-chain settlement using official records/transaction receipts. Reward text, a claimed budget, reputation, or a simulated ledger entry is not revenue.
6. **Evolve:** update skills/policies only from measured outcomes; require multiple completed and paid tasks with positive net results before allowing automatic policy changes.

## Readiness checklist

- [ ] Official TermiX skill installed in the actual BlueTokenCapital runtime.
- [ ] BSC account link approved by the account owner in the official flow.
- [ ] DAE checkout path and runtime permissions confirmed.
- [ ] Read-only discovery and task assessment tested end-to-end.
- [ ] One low-risk test order completed with an official order record.
- [ ] Delivery confirmed by TermiX.
- [ ] Actual payout/settlement verified independently on-chain.
- [ ] Retry/idempotency and emergency-stop behavior tested before unattended runs.

Until those items are proven, describe the integration as **in progress**. A profile showing “Available now” or 50 reputation with 0 completed jobs is not proof that DAE is executing work or earning revenue.

## Official references

- TermiX skill quickstart: https://www.agent.family/docs
- Skill overview/configuration: https://docs.termix.ai/skill/overview
- DAE repository: https://github.com/laucathaclac/-darwinian-agent-economy
