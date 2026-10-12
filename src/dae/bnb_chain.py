"""Read-only BNB Smart Chain JSON-RPC helpers.

This module intentionally does not sign or broadcast transactions. It is the
first integration step for DAE: verify the configured network and inspect
public chain state before any transaction executor is considered.
"""
from __future__ import annotations

import json
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

BSC_MAINNET_CHAIN_ID = 56
BSC_TESTNET_CHAIN_ID = 97
DEFAULT_BSC_TESTNET_RPC = "https://bsc-testnet-dataseed.bnbchain.org"


class BNBChainRPCError(RuntimeError):
    """Raised when an RPC endpoint returns an error or invalid response."""


def quantity_to_int(value: str) -> int:
    """Convert an Ethereum JSON-RPC quantity (hex string) to an integer."""
    if not isinstance(value, str) or not value.startswith("0x"):
        raise ValueError("RPC quantity must be a 0x-prefixed hex string")
    return int(value, 16)


def rpc_call(method: str, params: list | None = None, rpc_url: str = DEFAULT_BSC_TESTNET_RPC,
             timeout: float = 10.0):
    """Perform a single JSON-RPC request without signing or sending a transaction."""
    if method in {"eth_sendRawTransaction", "eth_sendTransaction", "personal_sendTransaction"}:
        raise ValueError("Transaction broadcasting is disabled in the read-only adapter")
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or [],
    }).encode("utf-8")
    request = Request(rpc_url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise BNBChainRPCError(f"BNB Chain RPC request failed: {exc}") from exc
    if result.get("error"):
        raise BNBChainRPCError(f"RPC error: {result['error']}")
    if "result" not in result:
        raise BNBChainRPCError("RPC response did not contain a result")
    return result["result"]


def get_network(rpc_url: str = DEFAULT_BSC_TESTNET_RPC) -> dict:
    """Return chain ID and latest block; reject unexpected network IDs."""
    chain_id = quantity_to_int(rpc_call("eth_chainId", rpc_url=rpc_url))
    block_number = quantity_to_int(rpc_call("eth_blockNumber", rpc_url=rpc_url))
    return {
        "chain_id": chain_id,
        "network": "BSC Testnet" if chain_id == BSC_TESTNET_CHAIN_ID else
                   "BSC Mainnet" if chain_id == BSC_MAINNET_CHAIN_ID else "Unknown network",
        "latest_block": block_number,
        "is_testnet": chain_id == BSC_TESTNET_CHAIN_ID,
    }


def get_native_balance(address: str, rpc_url: str = DEFAULT_BSC_TESTNET_RPC) -> dict:
    """Read a native BNB balance; caller must supply an address, never a private key."""
    if not isinstance(address, str) or len(address) != 42 or not address.startswith("0x"):
        raise ValueError("Address must be a 42-character 0x-prefixed EVM address")
    if any(ch not in "0123456789abcdefABCDEF" for ch in address[2:]):
        raise ValueError("Address contains non-hexadecimal characters")
    network = get_network(rpc_url)
    balance_wei = quantity_to_int(rpc_call("eth_getBalance", [address, "latest"], rpc_url))
    return {
        **network,
        "address": address,
        "balance_wei": balance_wei,
        "balance_bnb": balance_wei / 10**18,
    }
