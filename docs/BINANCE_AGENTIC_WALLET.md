# Binance Agentic Wallet integration (DAE)

## Goal

Connect DAE to Binance Agentic Wallet through Binance's official Wallet Skills rather than importing a seed phrase or private key into DAE.

Official references:
- Overview: https://developers.binance.com/en/docs/products/agentic-wallet/welcome
- Install guide: https://developers.binance.com/en/docs/products/agentic-wallet/quickstart/install-agentic-wallet
- Binance Wallet Skills: https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3

## Important scope

This is an integration plan, not a claim that DAE already has wallet execution wired in. The current DAE scanner is read-only. Installing Skills into a compatible local agent gives that agent access to wallet tools; it does not automatically make DAE's Python code able to call those tools.

Binance Agentic Wallet currently documents support for BSC mainnet (chain ID 56), Ethereum (1), Base (8453), and Solana. Do not use the existing BSC testnet RPC adapter as if it were the same wallet integration.

## Install on the Windows laptop

Run in a terminal on the machine where the compatible agent/CLI will run:

```bat
npx skills add binance/binance-skills-hub/skills/binance-web3/binance-agentic-wallet
```

If Node/npm is not installed, install the current supported Node.js LTS first, then reopen CMD and verify:

```bat
node --version
npm --version
npx --version
```

Follow the official installation guide for the specific agent framework. The terminal must belong to the agent environment that will use the Skill. Running the command in an unrelated terminal or only on GitHub does not connect DAE.

## Pairing flow

1. Start the compatible local agent and ask it to create/sign in to Binance Agentic Wallet according to the official guide.
2. The agent terminal generates a pairing QR/code.
3. Scan it in the Binance App and verify the pairing code matches before approving.
4. Enable Secure Auto Sign only after reviewing the terms and configuring the wallet's limits.
5. Verify the agent can read the Agentic Wallet address and balance before enabling any transaction workflow.

Do not send a seed phrase, private key, Binance password, or API secret to DAE, a chat, an issue, or a repository.

## Required guardrails before DAE can execute

- Start with a dedicated Agentic Wallet balance, separate from the main wallet.
- Set the smallest practical daily spending limit and narrow token scope.
- Keep transfers restricted to known address-book entries.
- Require explicit review for new transaction types, unfamiliar tokens/contracts, and large or irreversible operations.
- Add a DAE-side policy gate, dry-run/quote preview, transaction audit log, and daily budget check before connecting any autonomous strategy.
- Default to read-only and fail closed if wallet status, chain, amount, token, quote, or policy cannot be verified.
- Never execute from an opportunity score alone. DAE's current scores are triage signals, not proof of profit or payout.

## Acceptance checklist

- [ ] Official Skill installed in the correct local agent environment.
- [ ] Wallet pairing completed by the user in the Binance App.
- [ ] Wallet address and chain support verified.
- [ ] Read-only balance/status check works.
- [ ] Daily limit and token scope confirmed in the Binance App.
- [ ] Dry-run / quote and policy checks pass.
- [ ] One user-approved, low-value test transaction completed and audited.
- [ ] Automated execution remains disabled until separate tests and risk limits are reviewed.

## Costs and availability

Binance's FAQ says creating the wallet and installing Wallet Skills are free, while on-chain transactions may incur service fees. Availability and applicable terms may vary by region/account. Confirm in the Binance App before funding or authorizing the agent.

## Why the existing browser console is not the selected path

The prototype in PR #11 uses an injected browser provider and BSC testnet. Agentic Wallet is a separate, skill-based agent integration and currently lists BSC mainnet rather than BSC testnet. Keep the prototype separate; do not assume it can authenticate to or control Agentic Wallet.
