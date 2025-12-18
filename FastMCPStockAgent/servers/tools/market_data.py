import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_ticker_from_name(company_name: str) -> str:
    """Simple mapping or search. For production, use a search API."""
    # Simplified for demo. In real app, use yf.Ticker search
    mapping = {
        "apple": "AAPL", "microsoft": "MSFT", "tesla": "TSLA",
        "google": "GOOGL", "nvidia": "NVDA", "amazon": "AMZN"
    }
    return mapping.get(company_name.lower(), company_name.upper())

def fetch_historical_data(ticker: str, period="2y") -> pd.DataFrame:
    """Fetches OHLCV data."""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    df.reset_index(inplace=True)
    # Ensure date is timezone naive for compatibility
    df['Date'] = df['Date'].dt.tz_localize(None)
    return df

def get_specific_historical_price(ticker: str, date_str: str) -> float:
    """Gets exact close price for a past date."""
    stock = yf.Ticker(ticker)
    # Fetch a small window around the date to ensure we catch it
    start_date = datetime.strptime(date_str, "%Y-%m-%d")
    end_date = start_date + timedelta(days=1)
    
    df = stock.history(start=start_date, end=end_date)
    if df.empty:
        return None
    return df['Close'].iloc[0]