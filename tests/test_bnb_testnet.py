"""Unit tests for the read-only BSC Testnet RPC adapter."""
from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from dae.bnb_testnet import (
    BNBTestnetRPCError, get_native_balance, get_network, quantity_to_int, rpc_call,
)


class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.payload


class BNBTestnetTests(unittest.TestCase):
    @patch("dae.bnb_testnet.urlopen")
    def test_network_check_reads_chain_and_block(self, mocked):
        mocked.side_effect = [FakeResponse({"result": "0x61"}), FakeResponse({"result": "0x123"})]
        self.assertEqual(get_network(), {
            "chain_id": 97, "network": "BSC Testnet", "latest_block": 0x123
        })
        self.assertEqual(mocked.call_count, 2)

    @patch("dae.bnb_testnet.urlopen")
    def test_wrong_chain_fails_closed_before_block_query(self, mocked):
        mocked.return_value = FakeResponse({"result": "0x38"})
        with self.assertRaisesRegex(BNBTestnetRPCError, "expected BSC Testnet"):
            get_network()
        mocked.assert_called_once()

    @patch("dae.bnb_testnet.urlopen")
    def test_balance_is_read_only(self, mocked):
        mocked.side_effect = [
            FakeResponse({"result": "0x61"}),
            FakeResponse({"result": "0x10"}),
            FakeResponse({"result": "0xDE0B6B3A7640000"}),
        ]
        result = get_native_balance("0x" + "1" * 40)
        self.assertEqual(result["balance_wei"], 10**18)
        self.assertEqual(result["balance_tbnb"], 1.0)
        self.assertNotIn("private_key", result)

    def test_broadcast_methods_are_not_allowlisted(self):
        for method in ("eth_sendRawTransaction", "eth_sendTransaction", "personal_sendTransaction", "debug_traceTransaction"):
            with self.subTest(method=method), self.assertRaises(ValueError):
                rpc_call(method)

    def test_non_https_endpoint_rejected(self):
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            rpc_call("eth_chainId", rpc_url="http://localhost:8545")

    def test_bad_addresses_rejected(self):
        for address in ("", "0x1234", "0x" + "g" * 40):
            with self.subTest(address=address), self.assertRaises(ValueError):
                get_native_balance(address)

    def test_quantity_parser(self):
        self.assertEqual(quantity_to_int("0x61"), 97)
        for value in ("97", "0x", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                quantity_to_int(value)

    def test_rpc_error_propagated(self):
        with patch("dae.bnb_testnet.urlopen", return_value=FakeResponse({"error": {"message": "nope"}})):
            with self.assertRaisesRegex(BNBTestnetRPCError, "RPC error"):
                rpc_call("eth_chainId")


if __name__ == "__main__":
    unittest.main()
