import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from config import BASE_URL, get_headers, USE_PRO_API

def date_to_unix(date_string: str) -> int:
    """Convert YYYY-MM-DD to UNIX timestamp."""
    dt = datetime.strptime(date_string, "%Y-%m-%d")
    return int(dt.timestamp())


def fetch_bitcoin_historical(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch Bitcoin price data for a specified date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        DataFrame with timestamp index and price column
    """
    endpoint = f"{BASE_URL}/coins/bitcoin/market_chart/range"
    
    params = {
        "vs_currency": "usd",
        "from": date_to_unix(start_date),
        "to": date_to_unix(end_date)
    }
    
    response = requests.get(endpoint, headers=get_headers(), params=params)
    response.raise_for_status()
    data = response.json()
    
    # Create DataFrame from prices
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    
    return df


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Add backtesting metrics to the DataFrame."""
    # Daily returns (percentage change)
    df["daily_return"] = df["price"].pct_change() * 100
    
    # 30-day rolling average
    df["sma_30"] = df["price"].rolling(window=30).mean()
    
    # 30-day rolling volatility (standard deviation of returns)
    df["volatility_30"] = df["daily_return"].rolling(window=30).std()
    
    # Cumulative return from start
    df["cumulative_return"] = ((df["price"] / df["price"].iloc[0]) - 1) * 100
    
    return df


def plot_price_with_sma(df: pd.DataFrame, output_file: str = "bitcoin_analysis.png"):
    """Create a visualization of price with moving average."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Price and SMA
    ax1.plot(df.index, df["price"], label="BTC Price", alpha=0.8)
    ax1.plot(df.index, df["sma_30"], label="30-Day SMA", color="orange", alpha=0.8)
    ax1.set_ylabel("Price (USD)")
    ax1.set_title("Bitcoin Price Analysis")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Cumulative return
    ax2.fill_between(df.index, df["cumulative_return"], alpha=0.3, color="green")
    ax2.plot(df.index, df["cumulative_return"], color="green")
    ax2.set_ylabel("Cumulative Return (%)")
    ax2.set_xlabel("Date")
    ax2.axhline(y=0, color="black", linestyle="--", alpha=0.5)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    print(f"Chart saved to {output_file}")
    plt.close()


if __name__ == "__main__":
    # ==========================================================================
    # Date Range Configuration
    # ==========================================================================
    # Demo API: Access to past 365 days of historical data
    # Pro API: Access to full historical data back to 2013
    # ==========================================================================
    
    # Calculate date range (past 365 days works for all plans)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Format dates
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    plan_type = "Pro" if USE_PRO_API else "Demo"
    print(f"Using {plan_type} API plan")
    print(f"Fetching Bitcoin data from {start_str} to {end_str}...")
    
    btc_data = fetch_bitcoin_historical(start_str, end_str)
    print(f"Retrieved {len(btc_data)} data points")
    
    print("Calculating metrics...")
    btc_data = calculate_metrics(btc_data)
    
    print("\nSample of processed data:")
    print(btc_data.tail(10))
    
    print("\nSummary statistics:")
    print(f"  Start price: ${btc_data['price'].iloc[0]:,.2f}")
    print(f"  End price: ${btc_data['price'].iloc[-1]:,.2f}")
    print(f"  Total return: {btc_data['cumulative_return'].iloc[-1]:.1f}%")
    print(f"  Average daily return: {btc_data['daily_return'].mean():.3f}%")
    print(f"  Max single-day loss: {btc_data['daily_return'].min():.1f}%")
    
    print("\nGenerating visualization...")
    plot_price_with_sma(btc_data)
    
    # Export to CSV for further analysis
    btc_data.to_csv("bitcoin_backtesting.csv")
    print("Data exported to bitcoin_backtesting.csv")
