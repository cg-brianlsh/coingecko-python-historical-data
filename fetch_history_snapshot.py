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
    # Get Ethereum's price on the day of The Merge (September 15, 2022)
    eth_merge_day = get_price_on_date("ethereum", "15-09-2022")
    print("Ethereum on The Merge day:")
    print(f"  Price: ${eth_merge_day['price_usd']:,.2f}")
    print(f"  Market Cap: ${eth_merge_day['market_cap_usd']:,.0f}")