import requests
from config import BASE_URL, get_headers

def get_price_on_date(coin_id: str, date: str) -> dict:
    """
    Get the price and market data for a coin on a specific date.
    
    Args:
        coin_id: CoinGecko coin ID (e.g., 'bitcoin', 'ethereum')
        date: Date in DD-MM-YYYY format (European format required by API)
    
    Returns:
        Dictionary containing price, market_cap, and volume data
    """
    endpoint = f"{BASE_URL}/coins/{coin_id}/history"
    
    params = {
        "date": date,
        "localization": "false"
    }
    
    response = requests.get(endpoint, headers=get_headers(), params=params)
    response.raise_for_status()
    data = response.json()
    
    # Extract market data
    market_data = data.get("market_data", {})
    
    return {
        "name": data.get("name"),
        "symbol": data.get("symbol"),
        "date": date,
        "price_usd": market_data.get("current_price", {}).get("usd"),
        "market_cap_usd": market_data.get("market_cap", {}).get("usd"),
        "volume_usd": market_data.get("total_volume", {}).get("usd")
    }


if __name__ == "__main__":
    # Get Bitcoin's price on a specific date (August 1, 2025)
    # Note: Demo API users have access to past 365 days of data
    # Date format is DD-MM-YYYY (European format)
    btc_snapshot = get_price_on_date("bitcoin", "01-08-2025")
    print(f"Bitcoin on {btc_snapshot['date']}:")
    print(f"  Price: ${btc_snapshot['price_usd']:,.2f}")
    print(f"  Market Cap: ${btc_snapshot['market_cap_usd']:,.0f}")
