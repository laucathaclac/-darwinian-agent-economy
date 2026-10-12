"""Check BNB Smart Chain testnet connectivity and optionally read an address balance."""
from __future__ import annotations

import argparse
import json
import os
import sys

from dae.bnb_chain import DEFAULT_BSC_TESTNET_RPC, get_native_balance, get_network


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rpc", default=os.getenv("DAE_BSC_TESTNET_RPC", DEFAULT_BSC_TESTNET_RPC),
                        help="BSC testnet JSON-RPC URL (default: public BNB Chain testnet endpoint)")
    parser.add_argument("--address", help="Optional public EVM address to inspect; no private key needed")
    args = parser.parse_args()
    try:
        result = get_native_balance(args.address, args.rpc) if args.address else get_network(args.rpc)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    if result["chain_id"] != 97:
        print("WARNING: configured endpoint is not BSC Testnet (chain ID 97). No transactions were sent.")
        return 2
    print("OK: connected to BSC Testnet. This check is read-only; no transaction was sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
