import requests
import pandas as pd
from datetime import datetime
from config import BASE_URL, get_headers

def date_to_unix(date_string: str) -> int:
    """
    Convert a date string (YYYY-MM-DD) to UNIX timestamp.
    
    Args:
        date_string: Date in YYYY-MM-DD format
    
    Returns:
        UNIX timestamp in seconds
    """
    dt = datetime.strptime(date_string, "%Y-%m-%d")
    return int(dt.timestamp())


def get_historical_prices_range(
    coin_id: str, 
    start_date: str, 
    end_date: str, 
    vs_currency: str = "usd"
) -> pd.DataFrame:
    """
    Fetch historical price data for a specific date range.
    
    Args:
        coin_id: CoinGecko coin ID (e.g., 'bitcoin', 'ethereum')
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        vs_currency: Target currency for prices
    
    Returns:
        DataFrame with timestamp index and price, market_cap, volume columns
    """
    endpoint = f"{BASE_URL}/coins/{coin_id}/market_chart/range"
    
    params = {
        "vs_currency": vs_currency,
        "from": date_to_unix(start_date),
        "to": date_to_unix(end_date)
    }
    
    response = requests.get(endpoint, headers=get_headers(), params=params)
    response.raise_for_status()
    data = response.json()
    
    # Create DataFrames for each metric
    prices_df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    market_caps_df = pd.DataFrame(data["market_caps"], columns=["timestamp", "market_cap"])
    volumes_df = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume"])
    
    # Merge all metrics on timestamp
    df = prices_df.merge(market_caps_df, on="timestamp").merge(volumes_df, on="timestamp")
    
    # Convert UNIX timestamp (milliseconds) to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    
    return df


if __name__ == "__main__":
    # Fetch Bitcoin data for all of 2023
    btc_2023 = get_historical_prices_range(
        coin_id="bitcoin",
        start_date="2023-01-01",
        end_date="2023-12-31"
    )
    print(f"Fetched {len(btc_2023)} data points for 2023")
    print(btc_2023.head())