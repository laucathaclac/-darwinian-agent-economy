"""Read-only Venus Core Pool liquidation-risk monitor for BNB Smart Chain."""
from __future__ import annotations
import json, os, re, urllib.request
from datetime import datetime, timezone
from typing import Any

BSC_CHAIN_ID = 56
DEFAULT_RPC_URL = "https://bsc-dataseed.binance.org"
GET_ACCOUNT_LIQUIDITY_SELECTOR = "5ec88c79"
_ADDRESS_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")

class SentinelError(RuntimeError):
    """A risk check could not be completed reliably."""

def validate_address(address: str) -> str:
    if not isinstance(address, str) or not _ADDRESS_RE.fullmatch(address):
        raise ValueError("account must be a 20-byte EVM address")
    return address

def encode_get_account_liquidity(account: str) -> str:
    return "0x" + GET_ACCOUNT_LIQUIDITY_SELECTOR + validate_address(account)[2:].lower().rjust(64, "0")

def decode_account_liquidity(result: str) -> dict[str, int]:
    if not isinstance(result, str) or not result.startswith("0x"):
        raise SentinelError("RPC returned invalid eth_call data")
    payload = result[2:]
    if len(payload) < 192:
        raise SentinelError("RPC returned malformed account-liquidity data")
    try:
        words = [int(payload[i:i + 64], 16) for i in range(0, 192, 64)]
    except ValueError as exc:
        raise SentinelError("RPC returned non-hex account-liquidity data") from exc
    error_code, liquidity_wei, shortfall_wei = words
    if error_code != 0:
        raise SentinelError(f"Venus getAccountLiquidity error code: {error_code}")
    return {"liquidity_wei": liquidity_wei, "shortfall_wei": shortfall_wei}

def _rpc_call(method: str, params: list[Any], rpc_url: str, timeout: float) -> Any:
    body = json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode()
    request = urllib.request.Request(rpc_url, data=body, headers={"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode())
    except Exception as exc:
        raise SentinelError(f"RPC request failed: {type(exc).__name__}") from exc
    if not isinstance(data, dict) or data.get("error") or "result" not in data:
        raise SentinelError("RPC returned an error or malformed response")
    return data["result"]

def monitor_account(account: str, *, rpc_url: str | None = None,
                    comptroller_address: str | None = None,
                    warning_liquidity_usd: float = 1000.0,
                    critical_liquidity_usd: float = 250.0,
                    timeout: float = 8.0) -> dict[str, Any]:
    """Return Venus liquidity buffer/shortfall; this is not an exact HF ratio."""
    account = validate_address(account)
    rpc_url = rpc_url or os.getenv("BSC_RPC_URL", DEFAULT_RPC_URL)
    comptroller_address = comptroller_address or os.getenv("VENUS_COMPTROLLER_ADDRESS", "")
    if not _ADDRESS_RE.fullmatch(comptroller_address):
        raise SentinelError("Set VENUS_COMPTROLLER_ADDRESS to a verified Venus Core Pool Comptroller/Unitroller address.")
    if critical_liquidity_usd < 0 or warning_liquidity_usd < critical_liquidity_usd:
        raise ValueError("thresholds must satisfy warning >= critical >= 0")
    chain_id = _rpc_call("eth_chainId", [], rpc_url, timeout)
    try:
        chain_id_int = int(chain_id, 16)
    except (TypeError, ValueError) as exc:
        raise SentinelError("RPC returned invalid chain ID") from exc
    if chain_id_int != BSC_CHAIN_ID:
        raise SentinelError(f"Wrong network: expected BSC chain 56, got {chain_id_int}")
    call_data = encode_get_account_liquidity(account)
    raw = _rpc_call("eth_call", [{"to":comptroller_address,"data":call_data},"latest"], rpc_url, timeout)
    values = decode_account_liquidity(raw)
    liquidity = values["liquidity_wei"] / 10**18
    shortfall = values["shortfall_wei"] / 10**18
    if shortfall > 0:
        status, message = "CRITICAL", "Venus reports an account shortfall; review the position immediately."
    elif liquidity <= critical_liquidity_usd:
        status, message = "HIGH_RISK", "The remaining Venus liquidation-liquidity buffer is very low."
    elif liquidity <= warning_liquidity_usd:
        status, message = "WARNING", "The Venus liquidation-liquidity buffer is low; review collateral and debt."
    else:
        status, message = "OK", "No shortfall reported and the configured liquidity buffer is above thresholds."
    return {
        "agent":"DAE Health Sentinel","category":"health-factor monitoring",
        "network":"BNB Smart Chain","chain_id":chain_id_int,"protocol":"Venus Core Pool",
        "account":account,"status":status,"liquidity_buffer_usd":round(liquidity,8),
        "shortfall_usd":round(shortfall,8),"message":message,
        "as_of":datetime.now(timezone.utc).isoformat(),
        "method":"Venus Comptroller getAccountLiquidity(address)",
        "limitations":[
            "This reports Venus liquidity buffer/shortfall, not an exact health-factor ratio.",
            "An RPC response is a snapshot, not a guarantee against liquidation.",
            "No transaction is signed or sent; suggested actions require independent review."
        ]
    }
