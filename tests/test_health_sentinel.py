import unittest
from unittest.mock import patch
from dae.health_sentinel import SentinelError, decode_account_liquidity, encode_get_account_liquidity, monitor_account, validate_address

ACCOUNT = "0x" + "12"*20
COMPTROLLER = "0x" + "34"*20
def word(value): return f"{value:064x}"

class HealthSentinelTests(unittest.TestCase):
    def test_address_validation(self):
        self.assertEqual(validate_address(ACCOUNT), ACCOUNT)
        with self.assertRaises(ValueError): validate_address("0x123")
    def test_encodes_call(self):
        data = encode_get_account_liquidity(ACCOUNT)
        self.assertTrue(data.startswith("0x5ec88c79"))
        self.assertEqual(len(data), 74)
    def test_decode(self):
        result = "0x" + word(0) + word(125*10**18) + word(0)
        self.assertEqual(decode_account_liquidity(result), {"liquidity_wei":125*10**18,"shortfall_wei":0})
    def test_protocol_error_fails(self):
        with self.assertRaises(SentinelError): decode_account_liquidity("0x"+word(2)+word(0)+word(0))
    def test_wrong_chain_fails(self):
        with patch("dae.health_sentinel._rpc_call", return_value="0x1"):
            with self.assertRaisesRegex(SentinelError,"expected BSC chain 56"):
                monitor_account(ACCOUNT, comptroller_address=COMPTROLLER)
    def test_shortfall_is_critical(self):
        def rpc(method,params,url,timeout):
            if method=="eth_chainId": return "0x38"
            return "0x"+word(0)+word(0)+word(2*10**18)
        with patch("dae.health_sentinel._rpc_call",side_effect=rpc):
            result=monitor_account(ACCOUNT,comptroller_address=COMPTROLLER)
        self.assertEqual(result["status"],"CRITICAL")
        self.assertEqual(result["shortfall_usd"],2.0)
    def test_low_buffer_warning(self):
        def rpc(method,params,url,timeout):
            if method=="eth_chainId": return "0x38"
            return "0x"+word(0)+word(500*10**18)+word(0)
        with patch("dae.health_sentinel._rpc_call",side_effect=rpc):
            result=monitor_account(ACCOUNT,comptroller_address=COMPTROLLER)
        self.assertEqual(result["status"],"WARNING")
    def test_missing_comptroller_fails_closed(self):
        with patch.dict("os.environ",{"VENUS_COMPTROLLER_ADDRESS":""}):
            with self.assertRaisesRegex(SentinelError,"Set VENUS_COMPTROLLER_ADDRESS"):
                monitor_account(ACCOUNT)

if __name__ == "__main__": unittest.main()
