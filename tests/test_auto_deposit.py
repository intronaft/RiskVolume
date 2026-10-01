import unittest
from unittest.mock import Mock, patch

from auto_deposit import build_ccxt_balance_request_variants
from main import RiskVolumeApp, _extract_cross_margin_equity, _fetch_balance_with_ccxt


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


class CrossMarginEquityTests(unittest.TestCase):
    def test_bybit_endpoint_returns_wallet_balance_not_total_equity(self):
        response = Mock()
        response.json.return_value = {
            "retCode": 0,
            "result": {
                "list": [
                    {
                        "totalEquity": "102",
                        "totalWalletBalance": "100",
                    }
                ]
            },
        }
        with patch("main.requests.get", return_value=response):
            balance = RiskVolumeApp._fetch_bybit_unified_balance(
                None, "key", "secret", "USDT"
            )
        self.assertEqual(balance, 100.0)

    def test_binance_futures_endpoint_returns_cross_wallet_balance(self):
        response = Mock()
        response.json.return_value = {
            "totalMarginBalance": "102",
            "totalCrossWalletBalance": "100",
            "totalUnrealizedProfit": "2",
        }
        with patch("main.requests.get", return_value=response):
            balance = RiskVolumeApp._fetch_binance_balance_light(
                None, "key", "secret", "futures", "USDT"
            )
        self.assertEqual(balance, 100.0)

    def test_bybit_uses_wallet_balance_without_unrealized_pnl(self):
        balance = {
            "info": {
                "result": {
                    "list": [
                        {
                            "totalEquity": "1252.50",
                            "totalWalletBalance": "1250.50",
                            "totalAvailableBalance": "400",
                        }
                    ]
                }
            }
        }
        self.assertEqual(
            _extract_cross_margin_equity("bybit", balance, "USDT"),
            1250.5,
        )

    def test_binance_uses_cross_wallet_balance_not_margin_balance(self):
        balance = {
            "info": {
                "totalMarginBalance": "102",
                "totalCrossWalletBalance": "100",
                "totalUnrealizedProfit": "2",
            }
        }
        self.assertEqual(
            _extract_cross_margin_equity("binance", balance, "USDT"),
            100.0,
        )

    def test_falls_back_to_realized_balance_by_subtracting_unrealized_pnl(self):
        balance = {
            "info": {
                "accountEquity": "102",
                "unrealizedPL": "2",
            }
        }
        self.assertEqual(
            _extract_cross_margin_equity("bitget", balance, "USDT"),
            100.0,
        )

    def test_negative_unrealized_pnl_is_removed_without_inverting_sign(self):
        balance = {
            "info": {
                "accountEquity": "98",
                "unrealisedPNL": "-2",
            }
        }
        self.assertEqual(
            _extract_cross_margin_equity("kucoin", balance, "USDT"),
            100.0,
        )

    def test_known_exchange_does_not_fall_back_to_unsafe_ccxt_total(self):
        class FakeExchange:
            def __init__(self, params):
                self.auth_params = params

            def fetch_balance(self, request_params):
                self.request_params = request_params
                return {
                    "total": {"USDT": 102},
                    "info": {"equity": "102"},
                }

            def close(self):
                pass

        fake_ccxt = type("FakeCcxt", (), {"bitget": FakeExchange})
        payload = {
            "exchange_id": "bitget",
            "api_key": "key",
            "api_secret": "secret",
            "market_type": "futures",
            "asset": "USDT",
        }
        with patch("main.importlib.import_module", return_value=fake_ccxt):
            with self.assertRaisesRegex(
                RuntimeError, "may include unrealized PnL"
            ):
                _fetch_balance_with_ccxt(payload)

    def test_falls_back_to_ccxt_total_not_free_balance(self):
        balance = {
            "free": {"USDT": 400},
            "total": {"USDT": 1250.5},
        }
        self.assertEqual(
            _extract_cross_margin_equity("unknown", balance, "USDT"),
            1250.5,
        )


if __name__ == "__main__":
    unittest.main()
