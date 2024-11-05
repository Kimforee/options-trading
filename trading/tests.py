from django.test import TestCase
from unittest.mock import patch
import pandas as pd
from .utils import get_option_chain_data, calculate_margin_and_premium

class OptionChainDataTests(TestCase):
    @patch("trading.utils.requests.get")
    def test_get_option_chain_data_call_option(self, mock_get):
        # Sample mock response for Alpha Vantage API
        mock_response = {
            "Time Series (Daily)": {
                "2024-11-01": {
                    "1. open": "2300.00",
                    "2. high": "2350.00",
                    "3. low": "2290.00",
                    "4. close": "2330.00",
                    "5. volume": "2000000",
                },
                "2024-11-02": {
                    "1. open": "2350.00",
                    "2. high": "2400.00",
                    "3. low": "2330.00",
                    "4. close": "2380.00",
                    "5. volume": "2500000",
                },
            }
        }
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Call the function
        instrument_name = "NIFTY"
        side = "CE"
        df = get_option_chain_data(instrument_name, side)

        # Validate results
        self.assertEqual(df.shape[0], 2)
        self.assertEqual(df.loc[0, 'side'], "CE")
        self.assertEqual(df.loc[0, 'strike_price'], 2350.00)
        self.assertEqual(df.loc[0, 'bid/ask'], 2400.00)

class MarginAndPremiumTests(TestCase):
    @patch("trading.utils.requests.post")
    def test_calculate_margin_and_premium(self, mock_post):
        # Ensure mock response returns the correct margin as expected
        mock_margin_response = {"margin": 1950}
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_margin_response

        # Sample DataFrame input
        data = pd.DataFrame({
            "instrument_name": ["NIFTY", "NIFTY"],
            "strike_price": [19500, 20000],
            "side": ["PE", "CE"],
            "bid/ask": [0.65, 2302.25]
        })

        # Call the function
        result_df = calculate_margin_and_premium(data)

        # Validate results
        self.assertEqual(result_df.shape[0], 2)
        self.assertEqual(result_df.loc[0, 'margin_required'], 1950)  # Should match the mocked margin response
        self.assertEqual(result_df.loc[1, 'premium_earned'], 2302.25 * 75)  # assuming lot size is 75
