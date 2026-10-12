# Binance Agentic Wallet: DAE read-only adapter

## Current scope

DAE now has an optional Python adapter around the installed `baw` CLI. It can query:

- authentication/wallet status;
- addresses returned by BAW for supported chains;
- supported chains;
- token balances, optionally filtered by Binance chain ID, symbol, or token contract.

The adapter uses argument arrays with `shell=False`, a 30-second timeout, JSON validation, and a fixed allowlist of read-only operations. It deliberately exposes no generic command runner and no methods for sending, cancelling, speeding up, or signing transactions.

This is a local integration: the `baw` CLI and its authentication state must already be configured on the machine. Installing this adapter does not connect a wallet by itself.

## Windows usage

From the DAE project directory:

```bat
py -3 scripts\dae_wallet_readonly.py status
py -3 scripts\dae_wallet_readonly.py chains
py -3 scripts\dae_wallet_readonly.py addresses
py -3 scripts\dae_wallet_readonly.py balance --chain-id 56
py -3 scripts\dae_wallet_readonly.py balance --chain-id 56 --symbol BNB
```

Use `--baw PATH_TO_EXECUTABLE` only if the CLI is not named `baw` on PATH. The commands print JSON and return a non-zero exit code on failure.

## Balance interpretation

BAW's balance command documents that it only returns tokens with a non-zero balance. An empty array therefore means the query returned no matching non-zero token balances; it does not prove that every asset type or chain indexer has been exhaustively checked.

## Safety notes

- Keep this feature read-only; do not add transaction submission to the scanner.
- Never store or print seed phrases, private keys, pairing codes, QR IDs, or authentication tokens in DAE logs/reports.
- Never ask users to paste secrets into issues or chat.
- A connected wallet does not imply DAE has permission to sign or transact.
- Any future transaction feature must be a separate, explicit design with per-action consent, spending caps, and tests; it is outside this adapter's scope.

## Tests

Run the existing suite plus the adapter tests:

```bat
py -3 -m unittest discover -s tests -v
```

The adapter tests mock the CLI and do not need a funded wallet or network access.
