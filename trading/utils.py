# trading/utils.py

import requests
import pandas as pd
from django.conf import settings

def get_option_chain_data(instrument_name: str, side: str) -> pd.DataFrame:
    """
    Fetches option chain data for a specified instrument and side (Put or Call).

    Parameters:
    instrument_name (str): Name of the instrument (e.g., 'NIFTY').
    side (str): Type of option to retrieve ('PE' for Put, 'CE' for Call).

    Returns:
    pd.DataFrame: DataFrame containing instrument name, strike price, side, and bid/ask price.

    Raises:
    RuntimeError: If the API request fails.
    ValueError: If the response structure is unexpected.
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={instrument_name}&apikey=300DDTCL7F7V0CAB"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Check if data contains the expected structure
        if "Time Series (Daily)" not in data:
            raise ValueError("Unexpected response structure from API.")
        
        # Parse data and filter for 'PE' or 'CE' based on the side argument
        time_series_data = data["Time Series (Daily)"]
        parsed_data = []
        
        for date, values in time_series_data.items():
            strike_price = float(values["4. close"])
            bid_ask = float(values["2. high"] if side == "CE" else values["3. low"])
            parsed_data.append({
                "instrument_name": instrument_name,
                "strike_price": strike_price,
                "side": side,
                "bid/ask": bid_ask
            })
        
        # Create and return DataFrame
        return pd.DataFrame(parsed_data)
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {e}")
    except ValueError as ve:
        raise ValueError(f"Data validation error: {ve}")
    except KeyError as ke:
        raise ValueError(f"Missing expected key in response: {ke}")

# Assuming a lot size of 75 (typical for Indian stock options)
LOT_SIZE = 75

def calculate_margin_and_premium(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates margin required and premium earned for each option in the DataFrame.

    Parameters:
    data (pd.DataFrame): DataFrame containing option chain data.

    Returns:
    pd.DataFrame: Updated DataFrame with margin_required and premium_earned columns.

    Raises:
    ValueError: If required columns are missing from the input DataFrame.
    """
    # Ensure required columns exist
    required_columns = {"instrument_name", "strike_price", "side", "bid/ask"}
    if not required_columns.issubset(data.columns):
        raise ValueError("Input DataFrame is missing required columns.")

    # Calculate margin and premium
    data["margin_required"] = data.apply(
        lambda row: row["strike_price"] * (0.05 if row["side"] == "PE" else 0.07), axis=1
    )
    data["premium_earned"] = data["bid/ask"] * LOT_SIZE
    
    return data