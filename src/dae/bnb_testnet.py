"""Read-only BNB Smart Chain testnet JSON-RPC adapter for DAE.

Only a small allowlist of read methods is exposed. This module has no signing
or transaction-broadcasting capability and rejects endpoints that resolve to
a chain other than BSC Testnet (97) when strict testnet mode is requested.
"""
from __future__ import annotations

import json
import math
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BSC_TESTNET_CHAIN_ID = 97
DEFAULT_BSC_TESTNET_RPC = "https://bsc-testnet-dataseed.bnbchain.org"
_ALLOWED_METHODS = {"eth_chainId", "eth_blockNumber", "eth_getBalance"}


class BNBTestnetRPCError(RuntimeError):
    """Raised when the RPC request fails or returns an invalid response."""


def quantity_to_int(value: str) -> int:
    """Parse an EVM JSON-RPC quantity."""
    if not isinstance(value, str) or not value.startswith("0x") or len(value) < 3:
        raise ValueError("RPC quantity must be a non-empty 0x-prefixed hex string")
    try:
        return int(value, 16)
    except ValueError as exc:
        raise ValueError("RPC quantity contains invalid hexadecimal digits") from exc


def _validate_address(address: str) -> str:
    if not isinstance(address, str) or len(address) != 42 or not address.startswith("0x"):
        raise ValueError("Address must be a 42-character 0x-prefixed EVM address")
    if any(ch not in "0123456789abcdefABCDEF" for ch in address[2:]):
        raise ValueError("Address contains non-hexadecimal characters")
    return address


def rpc_call(method: str, params: list | None = None, *,
             rpc_url: str = DEFAULT_BSC_TESTNET_RPC, timeout: float = 10.0):
    """Call an explicitly allowlisted read-only JSON-RPC method."""
    if method not in _ALLOWED_METHODS:
        raise ValueError(f"RPC method is not allowlisted: {method}")
    if not isinstance(rpc_url, str) or not rpc_url.startswith("https://"):
        raise ValueError("RPC URL must use HTTPS")
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be a positive finite number")
    payload = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": method, "params": params or []
    }).encode("utf-8")
    request = Request(rpc_url, data=payload,
                      headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise BNBTestnetRPCError(f"BNB testnet RPC request failed: {exc}") from exc
    if not isinstance(result, dict):
        raise BNBTestnetRPCError("RPC response must be a JSON object")
    if result.get("error"):
        raise BNBTestnetRPCError(f"RPC error: {result['error']}")
    if "result" not in result:
        raise BNBTestnetRPCError("RPC response did not contain a result")
    return result["result"]


def get_network(*, rpc_url: str = DEFAULT_BSC_TESTNET_RPC, timeout: float = 10.0) -> dict:
    """Read chain ID and latest block, requiring BSC Testnet (97)."""
    chain_id = quantity_to_int(rpc_call("eth_chainId", rpc_url=rpc_url, timeout=timeout))
    if chain_id != BSC_TESTNET_CHAIN_ID:
        raise BNBTestnetRPCError(
            f"Wrong network: expected BSC Testnet chain ID 97, received {chain_id}"
        )
    block_number = quantity_to_int(
        rpc_call("eth_blockNumber", rpc_url=rpc_url, timeout=timeout)
    )
    return {"chain_id": chain_id, "network": "BSC Testnet", "latest_block": block_number}


def get_native_balance(address: str, *, rpc_url: str = DEFAULT_BSC_TESTNET_RPC,
                       timeout: float = 10.0) -> dict:
    """Read public native tBNB balance for an address; never accepts a private key."""
    address = _validate_address(address)
    network = get_network(rpc_url=rpc_url, timeout=timeout)
    balance_wei = quantity_to_int(
        rpc_call("eth_getBalance", [address, "latest"], rpc_url=rpc_url, timeout=timeout)
    )
    return {**network, "address": address, "balance_wei": balance_wei,
            "balance_tbnb": balance_wei / 10**18}
