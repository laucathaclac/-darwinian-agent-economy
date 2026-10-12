# Marketplace Listing — DAE Health Sentinel

**Status: copy prepared; not yet published to a marketplace.**

## Name
DAE Health Sentinel — Venus Liquidation-Risk Monitor

## Category
Health Factor Monitoring

## Short description
A read-only BNB Smart Chain agent that checks a Venus Core Pool account's liquidation-threshold liquidity and shortfall, then returns a timestamped risk status with transparent limitations. It does not custody funds or sign transactions.

## Full description
DAE Health Sentinel helps Venus users check a lending position's liquidation-risk buffer without handing over wallet access. Submit a public EVM account address and the agent queries Venus Core Pool's account-liquidity view on BNB Smart Chain.

### What it returns
- Current Venus account liquidity buffer and shortfall.
- Explainable status: OK, WARNING, HIGH_RISK, or CRITICAL.
- Timestamp, network and method used.
- Clear limits and a reminder that the result is an RPC snapshot, not a guarantee.

### Safety
- Read-only; no private keys, signing, transaction broadcasts, or custody.
- Never asks for a seed phrase or private key.
- Does not automatically repay debt or supply collateral.
- The Venus method returns liquidity/shortfall, not an exact health-factor ratio.
- A successful query does not guarantee a position cannot be liquidated.

## Endpoints
- GET /health
- GET /.well-known/agent-card.json
- POST /v1/monitor with JSON {"account":"0x..."}

## Pricing
To be set by the marketplace. Do not promise free hosted availability until a stable deployment and operating cost are confirmed.

## Repository
https://github.com/laucathaclac/-darwinian-agent-economy

## Publication blockers
- Verify and configure the official Venus Core Pool Comptroller/Unitroller address.
- Deploy to a stable public HTTPS endpoint and test from outside the host.
- Register ERC-8004 and publish verified registry ID and chain.
- Confirm the marketplace accepts the card/API format and publish the listing.
- Meet independent-hire and category-consistent on-chain-action requirements before claiming Set and Earn qualification.
