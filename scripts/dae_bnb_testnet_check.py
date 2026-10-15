"""Read-only BSC Testnet connectivity check for DAE."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dae.bnb_testnet import (  # noqa: E402
    BNBTestnetRPCError, DEFAULT_BSC_TESTNET_RPC, get_native_balance, get_network,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check BSC Testnet RPC (read-only; no wallet signing).")
    parser.add_argument("--rpc-url", default=DEFAULT_BSC_TESTNET_RPC,
                        help="HTTPS BSC Testnet RPC endpoint")
    parser.add_argument("--address", help="Optional public EVM address to inspect native tBNB balance")
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-request timeout in seconds")
    args = parser.parse_args()
    try:
        result = (get_native_balance(args.address, rpc_url=args.rpc_url, timeout=args.timeout)
                  if args.address else get_network(rpc_url=args.rpc_url, timeout=args.timeout))
    except (BNBTestnetRPCError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc), "transaction_executed": False}, indent=2))
        return 1
    print(json.dumps({"ok": True, **result, "read_only": True,
                      "transaction_executed": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
