import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from config import BASE_URL, get_headers

def date_to_unix(date_string: str) -> int:
    """Convert YYYY-MM-DD to UNIX timestamp."""
    dt = datetime.strptime(date_string, "%Y-%m-%d")
    return int(dt.timestamp())


def fetch_bitcoin_5_years() -> pd.DataFrame:
    """Fetch 5 years of Bitcoin price data."""
    endpoint = f"{BASE_URL}/coins/bitcoin/market_chart/range"
    
    params = {
        "vs_currency": "usd",
        "from": date_to_unix("2019-01-01"),
        "to": date_to_unix("2024-01-01")
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


def plot_price_with_sma(df: pd.DataFrame, output_file: str = "bitcoin_5yr_analysis.png"):
    """Create a visualization of price with moving average."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Price and SMA
    ax1.plot(df.index, df["price"], label="BTC Price", alpha=0.8)
    ax1.plot(df.index, df["sma_30"], label="30-Day SMA", color="orange", alpha=0.8)
    ax1.set_ylabel("Price (USD)")
    ax1.set_title("Bitcoin Price: 2019-2024")
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
    print("Fetching 5 years of Bitcoin data...")
    btc_data = fetch_bitcoin_5_years()
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
    print(f"  Max drawdown day: {btc_data['daily_return'].min():.1f}%")
    
    print("\nGenerating visualization...")
    plot_price_with_sma(btc_data)
    
    # Export to CSV for further analysis
    btc_data.to_csv("bitcoin_5yr_backtesting.csv")
    print("Data exported to bitcoin_5yr_backtesting.csv")