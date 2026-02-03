import pandas as pd
from fetch_market_chart import get_historical_prices

def export_coin_data_to_csv(coin_id: str, days: int, filename: str = None) -> str:
    """
    Fetch historical data and export to CSV.
    
    Args:
        coin_id: CoinGecko coin ID
        days: Number of days of data
        filename: Output filename (defaults to {coin_id}_history.csv)
    
    Returns:
        Path to the saved CSV file
    """
    if filename is None:
        filename = f"{coin_id}_history.csv"
    
    # Fetch the data
    df = get_historical_prices(coin_id, days=days)
    
    # Export to CSV with the datetime index
    df.to_csv(filename, index=True)
    print(f"Saved {len(df)} rows to {filename}")
    
    return filename


def export_multiple_coins(coin_ids: list, days: int, filename: str = "multi_coin_history.csv") -> str:
    """
    Fetch data for multiple coins and combine into a single CSV.
    
    Args:
        coin_ids: List of CoinGecko coin IDs
        days: Number of days of data
        filename: Output filename
    
    Returns:
        Path to the saved CSV file
    """
    all_data = []
    
    for coin_id in coin_ids:
        print(f"Fetching {coin_id}...")
        df = get_historical_prices(coin_id, days=days)
        df["coin"] = coin_id
        all_data.append(df)
    
    # Combine all DataFrames
    combined_df = pd.concat(all_data)
    combined_df.to_csv(filename, index=True)
    print(f"Saved {len(combined_df)} total rows to {filename}")
    
    return filename


if __name__ == "__main__":
    # Export single coin (90 days)
    export_coin_data_to_csv("bitcoin", days=90, filename="bitcoin_90d.csv")
    
    # Export multiple coins
    coins = ["bitcoin", "ethereum", "solana"]
    export_multiple_coins(coins, days=90, filename="top_coins_90d.csv")
