import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# CoinGecko API Configuration
# =============================================================================
# Set USE_PRO_API to True if you have a paid plan (Analyst, Lite, Pro, Enterprise)
# Set to False for the free Demo plan
# =============================================================================
USE_PRO_API = os.getenv("USE_PRO_API", "false").lower() == "true"

# API Key
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

# Base URL and header key depend on your plan
if USE_PRO_API:
    BASE_URL = "https://pro-api.coingecko.com/api/v3"
    API_HEADER_KEY = "x-cg-pro-api-key"
else:
    BASE_URL = "https://api.coingecko.com/api/v3"
    API_HEADER_KEY = "x-cg-demo-api-key"


def get_headers():
    """Return headers with API key for CoinGecko requests."""
    return {
        "accept": "application/json",
        API_HEADER_KEY: COINGECKO_API_KEY
    }


# Print configuration status (useful for debugging)
if __name__ == "__main__":
    plan_type = "Pro/Paid" if USE_PRO_API else "Demo (Free)"
    print(f"CoinGecko API Configuration:")
    print(f"  Plan: {plan_type}")
    print(f"  Base URL: {BASE_URL}")
    print(f"  Header Key: {API_HEADER_KEY}")
    print(f"  API Key: {COINGECKO_API_KEY[:10]}..." if COINGECKO_API_KEY else "  API Key: Not set")
