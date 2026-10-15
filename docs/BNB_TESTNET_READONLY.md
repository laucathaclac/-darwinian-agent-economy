# BSC Testnet read-only adapter

## Purpose

Provide DAE with a first live network integration that can be tested without wallet credentials. The adapter uses the public BSC Testnet JSON-RPC endpoint and requires chain ID **97**.

## Commands (Windows CMD)

```bat
py -3 -m unittest discover -s tests -v
py -3 scripts\dae_bnb_testnet_check.py
py -3 scripts\dae_bnb_testnet_check.py --address 0xYOUR_PUBLIC_TESTNET_ADDRESS
```

The optional address is a public EVM address, not a private key. The command reports chain ID, latest block, and optionally the address's native tBNB balance. Use an address you control only if you want to inspect its public balance; no wallet connection is needed.

## Security properties

- HTTPS RPC only.
- Allowlisted methods: `eth_chainId`, `eth_blockNumber`, and `eth_getBalance`.
- Chain ID must be exactly 97 before returning a network status or balance.
- No signing library, private-key input, transaction submission, or arbitrary RPC method execution.
- Network/API errors fail closed and return a nonzero CLI exit code.

## Explicit limitations

This adapter does **not** read lending positions, prices, collateral factors, or protocol-specific liquidation thresholds. It is not wired into HealthGuard's position input and does not prove the agent is deployed or campaign-qualified. The next engineering step is a protocol-specific, read-only testnet data adapter with verified market addresses and unit tests against documented contract interfaces. Only after that should the HTTP agent card/API and TermiX marketplace workflow be connected.
