import unittest

from auto_deposit import build_ccxt_balance_request_variants


class AutoDepositVariantsTests(unittest.TestCase):
    def test_bybit_futures_uses_unified_account_fallbacks(self):
        variants = build_ccxt_balance_request_variants(
            exchange_id="bybit",
            market_type="futures",
            api_key="key",
            api_secret="secret",
            asset="USDT",
            passphrase="",
        )

        self.assertGreaterEqual(len(variants), 3)
        labels = [variant["label"] for variant in variants]
        self.assertIn("bybit-unified-swap", labels)
        self.assertIn("bybit-unified-linear", labels)

    def test_bybit_spot_keeps_spot_defaults(self):
        variants = build_ccxt_balance_request_variants(
            exchange_id="bybit",
            market_type="spot",
            api_key="key",
            api_secret="secret",
            asset="USDT",
            passphrase="",
        )

        self.assertTrue(any(variant["label"] == "bybit-spot" for variant in variants))
        spot_variant = next(variant for variant in variants if variant["label"] == "bybit-spot")
        self.assertEqual(spot_variant["auth"]["options"].get("defaultType"), "spot")


if __name__ == "__main__":
    unittest.main()
