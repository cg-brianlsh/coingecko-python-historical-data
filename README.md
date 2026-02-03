# CoinGecko Python Historical Data Toolkit

A Python toolkit for fetching historical cryptocurrency data using the CoinGecko API. This repository accompanies the tutorial article "How to Fetch Crypto Historical Data with Python" on CoinGecko Learn.

## Features

- Fetch historical price, market cap, and volume data
- Query custom date ranges with UNIX timestamps
- Get price snapshots for specific dates
- Retrieve OHLC candlestick data
- Fetch token data by contract address
- Export data to CSV for analysis
- Complete backtesting example with visualization
- **Supports both Demo (Free) and Pro (Paid) API plans**

## Quick Start

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your CoinGecko API key
4. Configure your plan type in `.env` (see below)
5. Run any script: `python fetch_market_chart.py`

## Configuration

The toolkit supports both Demo and Pro API plans. Edit your `.env` file:

```ini
# Your CoinGecko API key
COINGECKO_API_KEY=CG-your_api_key_here

# Set to "true" if using a paid plan (Analyst, Lite, Pro, Enterprise)
# Set to "false" for the free Demo plan
USE_PRO_API=false
```

### Plan Differences

| Feature | Demo (Free) | Pro (Paid) |
|---------|-------------|------------|
| Base URL | api.coingecko.com | pro-api.coingecko.com |
| Header Key | x-cg-demo-api-key | x-cg-pro-api-key |
| Historical Data | Past 365 days | Full history (2013+) |

## Get Your API Key

Sign up for a free Demo API key at the [CoinGecko Developer Portal](https://www.coingecko.com/en/api).

## Files

| File | Description |
|------|-------------|
| `config.py` | API configuration with Demo/Pro plan support |
| `fetch_market_chart.py` | Fetch historical data with `/market_chart` |
| `fetch_market_chart_range.py` | Query custom date ranges |
| `fetch_history_snapshot.py` | Get price on a specific date |
| `fetch_ohlc.py` | Fetch OHLC candlestick data |
| `fetch_by_contract.py` | Fetch data by token contract address |
| `export_to_csv.py` | Export historical data to CSV |
| `backtesting_example.py` | Complete backtesting workflow |

## License

MIT
