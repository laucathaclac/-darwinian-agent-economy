# DAE Health Sentinel — Set and Earn build track

Product direction: read-only Venus Core Pool liquidation-risk monitoring on BNB Smart Chain (chain ID 56), in the campaign's health-factor-monitoring category.

## MVP features
- GET /health availability endpoint.
- GET /.well-known/agent-card.json public capability card.
- POST /v1/monitor with JSON body {"account":"0x..."}.
- Reads Venus getAccountLiquidity(address), reports liquidity buffer, shortfall, UTC timestamp and an explainable risk status.
- Fails closed on invalid addresses, wrong RPC chain, malformed RPC responses or missing Comptroller configuration.
- No private keys, wallet connection, transaction signing, broadcasting or custody.

## Accuracy boundary
Venus getAccountLiquidity reports liquidation-threshold liquidity and shortfall; it does not directly return an exact health-factor ratio. The service must not present this output as an exact HF number. A nonzero shortfall is critical. A successful RPC response is only a snapshot, not a guarantee against liquidation.

References:
- https://docs-v4.venus.io/technical-reference/reference-isolated-pools/comptroller/comptroller
- https://docs-v4.venus.io/guides/liquidation

## Windows CMD local run
From the repository root:
    py -3 -m pip install -e .
    set VENUS_COMPTROLLER_ADDRESS=<verified Venus Core Pool Comptroller/Unitroller address>
    set AGENT_PUBLIC_URL=http://127.0.0.1:8787
    py -3 scripts\dae_health_sentinel_server.py

Check:
    curl http://127.0.0.1:8787/health
    curl http://127.0.0.1:8787/.well-known/agent-card.json

Monitor a public address you are authorized to inspect:
    curl -X POST http://127.0.0.1:8787/v1/monitor -H "Content-Type: application/json" -d "{\"account\":\"0x0000000000000000000000000000000000000000\"}"

## Configuration
- BSC_RPC_URL: optional BSC mainnet JSON-RPC URL; defaults to the public BSC dataseed.
- VENUS_COMPTROLLER_ADDRESS: required and must be verified against current official deployment docs.
- AGENT_PUBLIC_URL: set to deployed HTTPS origin before listing.
- DAE_HOST and DAE_PORT: defaults to 127.0.0.1:8787. Only bind publicly behind a properly configured HTTPS reverse proxy.

## Campaign checklist — no completion claims without evidence
- [ ] Verify current Venus Core Pool Comptroller address from official deployment docs.
- [ ] Pass Windows and Linux CI tests.
- [ ] Deploy a stable public HTTPS endpoint and test card/health/monitor.
- [ ] Register ERC-8004 on chain 56 or 97 from the registered campaign wallet.
- [ ] Publish actual registry ID and chain in the public repository.
- [ ] List on a shortlisted marketplace after the official Phase 2 announcement.
- [ ] Receive 3 completed hires from 3 independent wallets.
- [ ] Demonstrate at least 5 real category-consistent on-chain actions across 3 separate days. This read-only MVP alone does not satisfy that requirement.
- [ ] Complete hire track: 3 different agents across at least 2 shortlisted marketplaces.

Never self-hire, use wallets you fund to simulate independent demand, or fabricate activity. Do not deploy an unattended transaction executor without separate threat modeling, simulation, contract allowlists, hard spend caps and explicit approvals.
