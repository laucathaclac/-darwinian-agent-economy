"""Read-only Binance Agentic Wallet inspection commands for DAE."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dae.wallet_adapter import WalletAdapter, WalletCLIError  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only Binance Agentic Wallet status, addresses, chains, or balances."
    )
    parser.add_argument("command", choices=("status", "addresses", "chains", "balance"))
    parser.add_argument("--chain-id", help="Optional Binance chain ID, e.g. 56 for BSC.")
    parser.add_argument("--symbol", help="Optional token symbol filter, e.g. BNB.")
    parser.add_argument("--token-address", help="Optional token contract address filter.")
    parser.add_argument("--baw", default="baw", help="Path/name of the baw executable.")
    args = parser.parse_args()

    adapter = WalletAdapter(executable=args.baw)
    try:
        if args.command == "status":
            data = adapter.status()
        elif args.command == "addresses":
            data = adapter.addresses()
        elif args.command == "chains":
            data = adapter.chains()
        else:
            data = adapter.balance(
                chain_id=args.chain_id,
                symbol=args.symbol,
                token_address=args.token_address,
            )
    except (WalletCLIError, ValueError) as exc:
        print(json.dumps({"success": False, "error": str(exc)}, indent=2))
        return 1

    print(json.dumps({"success": True, "data": data}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
