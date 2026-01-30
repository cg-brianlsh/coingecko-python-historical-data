import requests
import pandas as pd
from config import BASE_URL, get_headers

def get_token_history_by_contract(
    platform: str, 
    contract_address: str, 
    vs_currency: str = "usd", 
    days: int = 30
) -> pd.DataFrame:
    """
    Fetch historical data for a token using its contract address.
    
    Args:
        platform: Blockchain platform ID (e.g., 'ethereum', 'solana', 'base')
        contract_address: Token contract address
        vs_currency: Target currency
        days: Number of days of data
    
    Returns:
        DataFrame with timestamp index and price, market_cap, volume columns
    """
    endpoint = f"{BASE_URL}/coins/{platform}/contract/{contract_address}/market_chart"
    
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
    
    # Merge all metrics
    df = prices_df.merge(market_caps_df, on="timestamp").merge(volumes_df, on="timestamp")
    
    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    
    return df


if __name__ == "__main__":
    # Fetch Chainlink (LINK) data using its Ethereum contract address
    link_contract = "0x514910771af9ca656af840dff83e8264ecf986ca"
    link_data = get_token_history_by_contract(
        platform="ethereum",
        contract_address=link_contract,
        days=30
    )
    print(f"Fetched {len(link_data)} data points for LINK")
    print(link_data.head())