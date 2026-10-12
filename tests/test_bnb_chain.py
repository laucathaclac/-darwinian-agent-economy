import unittest
from unittest.mock import patch

from dae.bnb_chain import (
    BNBChainRPCError,
    BSC_TESTNET_CHAIN_ID,
    get_network,
    quantity_to_int,
    rpc_call,
)


class BNBChainAdapterTests(unittest.TestCase):
    def test_quantity_to_int(self):
        self.assertEqual(quantity_to_int("0x61"), 97)
        self.assertEqual(quantity_to_int("0x0"), 0)

    def test_quantity_rejects_non_rpc_quantity(self):
        with self.assertRaises(ValueError):
            quantity_to_int("97")

    @patch("dae.bnb_chain.rpc_call")
    def test_get_network_marks_testnet(self, rpc):
        rpc.side_effect = ["0x61", "0x123"]
        result = get_network("https://example.invalid")
        self.assertEqual(result["chain_id"], BSC_TESTNET_CHAIN_ID)
        self.assertTrue(result["is_testnet"])
        self.assertEqual(result["latest_block"], 0x123)

    def test_broadcast_methods_are_blocked(self):
        for method in ("eth_sendRawTransaction", "eth_sendTransaction", "personal_sendTransaction"):
            with self.subTest(method=method):
                with self.assertRaises(ValueError):
                    rpc_call(method, params=["0xdeadbeef"], rpc_url="https://example.invalid")


if __name__ == "__main__":
    unittest.main()
