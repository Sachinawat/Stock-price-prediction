import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_ticker_from_name(company_name: str) -> str:
    """
    Maps company names to NSE tickers (Indian Market).
    """
    # 1. Common Mapping for Indian Giants
    mapping = {
        "reliance": "RELIANCE.NS", "tcs": "TCS.NS", "infosys": "INFY.NS",
        "hdfc": "HDFCBANK.NS", "icici": "ICICIBANK.NS", "sbi": "SBIN.NS",
        "tata motors": "TATAMOTORS.NS", "zomato": "ZOMATO.NS",
        "paytm": "PAYTM.NS", "adani": "ADANIENT.NS"
    }
    
    clean_name = company_name.lower().replace(" bank", "").strip()
    
    if clean_name in mapping:
        return mapping[clean_name]
    
    # 2. If not found, assume user input is the symbol and append .NS
    return f"{company_name.upper()}.NS"

def fetch_historical_data(ticker: str, period="5y") -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    
    if df.empty:
        return None
        
    df.reset_index(inplace=True)
    # Remove Timezone info for compatibility
    df['Date'] = df['Date'].dt.tz_localize(None) 
    return df

def get_current_price(ticker: str) -> float:
    stock = yf.Ticker(ticker)
    # Fast fetch of today's data
    df = stock.history(period="1d")
    if not df.empty:
        return df['Close'].iloc[-1]
    return 0.0