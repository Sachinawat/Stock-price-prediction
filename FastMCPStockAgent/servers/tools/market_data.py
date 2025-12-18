import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

def search_indian_ticker(query: str) -> str:
    """
    Uses Yahoo Finance API to find the correct Indian Ticker (.NS or .BO).
    Handles names like 'Reliance' -> 'RELIANCE.NS', 'Infosys' -> 'INFY.NS'.
    """
    print(f"🔎 Searching database for '{query}'...")
    
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=10&newsCount=0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        
        if 'quotes' in data and len(data['quotes']) > 0:
            for quote in data['quotes']:
                symbol = quote.get('symbol', '')
                shortname = quote.get('shortname', '').lower()
                
                # Priority 1: National Stock Exchange (NSE)
                if symbol.endswith('.NS'):
                    return symbol
                
                # Priority 2: Bombay Stock Exchange (BSE)
                if symbol.endswith('.BO'):
                    return symbol
                    
    except Exception as e:
        print(f"Search API Warning: {e}")
        
    return None

def get_ticker_from_name(company_name: str) -> str:
    # 1. Manual Map for common tricky ones (Optional but faster)
    mapping = {
        "reliance": "RELIANCE.NS",
        "tcs": "TCS.NS",
        "infosys": "INFY.NS", # Note: Ticker is INFY, not INFOSYS
        "wipro": "WIPRO.NS",
        "hcl": "HCLTECH.NS",
        "sbi": "SBIN.NS",
        "zomato": "ZOMATO.NS"
    }
    
    clean_name = company_name.lower().strip()
    if clean_name in mapping:
        return mapping[clean_name]
        
    # 2. Run Smart Search
    found_ticker = search_indian_ticker(company_name)
    
    # 3. If found, return it. If not, try a blind guess (Upper + .NS)
    if found_ticker:
        return found_ticker
        
    print("⚠️ Search failed, attempting blind guess...")
    return f"{company_name.upper().replace(' ', '')}.NS"

def fetch_historical_data(ticker: str, period="5y") -> pd.DataFrame:
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if df.empty:
            return None
            
        df.reset_index(inplace=True)
        df['Date'] = df['Date'].dt.tz_localize(None) 
        return df
    except Exception:
        return None

def get_specific_historical_price(ticker: str, date_str: str) -> float:
    # (Same as before)
    stock = yf.Ticker(ticker)
    start_date = datetime.strptime(date_str, "%Y-%m-%d")
    end_date = datetime.strptime(date_str, "%Y-%m-%d") + pd.Timedelta(days=1)
    df = stock.history(start=start_date, end=end_date)
    if df.empty: return None
    return df['Close'].iloc[0]