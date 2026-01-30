import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# CoinGecko API Configuration
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
BASE_URL = "https://api.coingecko.com/api/v3"

def get_headers():
    """Return headers with API key for CoinGecko requests."""
    return {
        "accept": "application/json",
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }