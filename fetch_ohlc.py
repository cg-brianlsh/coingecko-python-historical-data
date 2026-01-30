import requests
import pandas as pd
from config import BASE_URL, get_headers

def get_ohlc_data(coin_id: str, vs_currency: str = "usd", days: int = 30) -> pd.DataFrame:
    """
    Fetch OHLC candlestick data for a cryptocurrency.
    
    Args:
        coin_id: CoinGecko coin ID
        vs_currency: Target currency
        days: Number of days (1, 7, 14, 30, 90, 180, 365)
    
    Returns:
        DataFrame with timestamp, open, high, low, close columns
    """
    endpoint = f"{BASE_URL}/coins/{coin_id}/ohlc"
    
    params = {
        "vs_currency": vs_currency,
        "days": days
    }
    
    response = requests.get(endpoint, headers=get_headers(), params=params)
    response.raise_for_status()
    data = response.json()
    
    # API returns list of [timestamp, open, high, low, close]
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
    
    # Convert UNIX timestamp (milliseconds) to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    
    return df


if __name__ == "__main__":
    # Fetch 30 days of Bitcoin OHLC data
    btc_ohlc = get_ohlc_data("bitcoin", days=30)
    print(f"Fetched {len(btc_ohlc)} candles")
    print(btc_ohlc.head())