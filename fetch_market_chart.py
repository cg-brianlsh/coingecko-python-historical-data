import requests
import pandas as pd
from datetime import datetime
from config import BASE_URL, get_headers

def get_historical_prices(coin_id: str, vs_currency: str = "usd", days: int = 30) -> pd.DataFrame:
    """
    Fetch historical price data for a cryptocurrency.
    
    Args:
        coin_id: CoinGecko coin ID (e.g., 'bitcoin', 'ethereum')
        vs_currency: Target currency for prices (e.g., 'usd', 'eur')
        days: Number of days of historical data (1, 7, 14, 30, 90, 180, 365, or 'max')
    
    Returns:
        DataFrame with timestamp index and price, market_cap, volume columns
    """
    endpoint = f"{BASE_URL}/coins/{coin_id}/market_chart"
    
    params = {
        "vs_currency": vs_currency,
        "days": days
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
    # Fetch 30 days of Bitcoin price data
    btc_data = get_historical_prices("bitcoin", days=30)
    print(f"Fetched {len(btc_data)} data points")
    print(btc_data.head())