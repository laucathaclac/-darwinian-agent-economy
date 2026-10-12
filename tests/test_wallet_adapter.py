"""Unit tests for the read-only BAW adapter; no wallet or network required."""
import json
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from unittest.mock import patch, Mock

from dae.wallet_adapter import WalletAdapter, WalletCLIError


class WalletAdapterTests(unittest.TestCase):
    @patch("dae.wallet_adapter.shutil.which", return_value="C:/npm/baw.cmd")
    @patch("dae.wallet_adapter.subprocess.run")
    def test_status_calls_only_read_command(self, run, _which):
        run.return_value = Mock(
            returncode=0,
            stdout=json.dumps({"success": True, "data": {"status": "CONNECTED"}}),
            stderr="",
        )
        result = WalletAdapter().status()
        self.assertEqual(result, {"status": "CONNECTED"})
        command = run.call_args.args[0]
        self.assertEqual(command, ["baw", "wallet", "status", "--json"])
        self.assertFalse(run.call_args.kwargs["shell"])

    @patch("dae.wallet_adapter.shutil.which", return_value="C:/npm/baw.cmd")
    @patch("dae.wallet_adapter.subprocess.run")
    def test_balance_can_filter_bsc(self, run, _which):
        run.return_value = Mock(
            returncode=0, stdout='{"success": true, "data": []}', stderr=""
        )
        self.assertEqual(WalletAdapter().balance(chain_id=56), [])
        self.assertEqual(
            run.call_args.args[0],
            ["baw", "wallet", "balance", "--binanceChainId", "56", "--json"],
        )

    def test_rejects_non_numeric_chain_id_before_process(self):
        with patch("dae.wallet_adapter.subprocess.run") as run:
            with self.assertRaises(ValueError):
                WalletAdapter().balance(chain_id="56 --send")
            run.assert_not_called()

    @patch("dae.wallet_adapter.shutil.which", return_value=None)
    def test_missing_cli_is_reported(self, _which):
        with self.assertRaisesRegex(WalletCLIError, "not found on PATH"):
            WalletAdapter().status()

    @patch("dae.wallet_adapter.shutil.which", return_value="C:/npm/baw.cmd")
    @patch("dae.wallet_adapter.subprocess.run")
    def test_rejects_cli_failure(self, run, _which):
        run.return_value = Mock(
            returncode=1,
            stdout='{"success": false, "error": {"message": "not connected"}}',
            stderr="",
        )
        with self.assertRaisesRegex(WalletCLIError, "not connected"):
            WalletAdapter().status()


if __name__ == "__main__":
    unittest.main()
