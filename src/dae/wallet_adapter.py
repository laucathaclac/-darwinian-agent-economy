"""Safe, read-only adapter for Binance Agentic Wallet (BAW) CLI.

This module intentionally exposes only status, addresses, chains and balance reads.
It does not provide a generic command runner and cannot submit or sign transactions.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from typing import Any, Sequence


class WalletCLIError(RuntimeError):
    """Raised when the BAW CLI is missing, times out, or returns invalid data."""


@dataclass(frozen=True)
class WalletAdapter:
    executable: str = "baw"
    timeout_seconds: int = 30

    def _read(self, args: Sequence[str]) -> dict[str, Any] | list[Any]:
        if shutil.which(self.executable) is None:
            raise WalletCLIError(
                f"'{self.executable}' was not found on PATH. Install Binance Agentic Wallet CLI first."
            )
        try:
            result = subprocess.run(
                [self.executable, *args, "--json"],
                shell=False,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise WalletCLIError("BAW CLI timed out while reading wallet data.") from exc
        except OSError as exc:
            raise WalletCLIError(f"Could not start BAW CLI: {exc}") from exc

        raw = result.stdout.strip()
        if not raw:
            detail = result.stderr.strip() or f"process exited with code {result.returncode}"
            raise WalletCLIError(f"BAW returned no JSON output: {detail}")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise WalletCLIError("BAW returned invalid JSON; output was not trusted.") from exc
        if result.returncode != 0 or not isinstance(payload, dict) or payload.get("success") is not True:
            error = payload.get("error", {}) if isinstance(payload, dict) else {}
            message = error.get("message") if isinstance(error, dict) else None
            raise WalletCLIError(str(message or "BAW read request failed."))
        return payload.get("data", payload)

    def status(self) -> dict[str, Any] | list[Any]:
        return self._read(["wallet", "status"])

    def addresses(self) -> dict[str, Any] | list[Any]:
        return self._read(["wallet", "address"])

    def chains(self) -> dict[str, Any] | list[Any]:
        return self._read(["wallet", "chains"])

    def balance(
        self,
        *,
        chain_id: str | int | None = None,
        symbol: str | None = None,
        token_address: str | None = None,
    ) -> dict[str, Any] | list[Any]:
        args = ["wallet", "balance"]
        if chain_id is not None:
            value = str(chain_id).strip()
            if not value.isdigit():
                raise ValueError("chain_id must contain digits only.")
            args.extend(["--binanceChainId", value])
        if symbol is not None:
            value = symbol.strip()
            if not value or any(ch.isspace() for ch in value):
                raise ValueError("symbol must be a non-empty token symbol without spaces.")
            args.extend(["--symbol", value])
        if token_address is not None:
            value = token_address.strip()
            if not value or any(ch.isspace() for ch in value):
                raise ValueError("token_address must be non-empty and contain no spaces.")
            args.extend(["--tokenAddress", value])
        return self._read(args)
