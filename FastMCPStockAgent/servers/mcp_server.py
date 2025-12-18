# import sys
# import os

# # PATH FIX
# current_dir = os.path.dirname(os.path.abspath(__file__))
# root_dir = os.path.dirname(current_dir)
# sys.path.append(root_dir)

# from fastmcp import FastMCP
# from servers.tools import market_data, advanced_ml, scraper # <--- Added Scraper
# from datetime import datetime

# mcp = FastMCP("StockQuantAgent")

# def stock_logic(company_name: str, date_str: str) -> str:
#     # 1. Indian Ticker Lookup
#     ticker = market_data.get_ticker_from_name(company_name)
#     print(f"🇮🇳 Analyzing {ticker} (NSE/BSE)...")

#     # 2. Date Check
#     try:
#         target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#     except ValueError: return "❌ Date format error."
#     today = datetime.now().date()
#     days_ahead = (target_date - today).days

#     # 3. GET DATA
#     df = market_data.fetch_historical_data(ticker, period="2y") # 2y is faster/enough
#     if df is None or len(df) < 50:
#         return f"❌ Could not fetch data for {ticker}. Check spelling."

#     current_price = df['Close'].iloc[-1]

#     # --- SCENARIO A: PAST/TODAY ---
#     if days_ahead <= 0:
#         return f"✅ Current Price of {ticker}: ₹{current_price:.2f}"

#     # --- SCENARIO B: FUTURE PREDICTION ---
#     if days_ahead > 365:
#         return "⚠️ Prediction limited to 1 year."

#     print("📊 1. Running Mathematical Models (LSTM/ARIMA)...")
#     best_model, results = advanced_ml.race_models_and_predict(df, days_ahead)
#     raw_prediction = results[best_model]['prediction']

#     print("🌍 2. Scraping News for Sentiment Adjustment...")
#     sentiment_data = scraper.analyze_sentiment_from_news(ticker)
#     sentiment_score = sentiment_data['score'] # e.g., +0.2 or -0.1
    
#     # --- HYBRID CALCULATION ---
#     # We adjust the math prediction by the sentiment %
#     # If News is Good (+0.2), price gets a 2% boost.
#     adjusted_price = raw_prediction * (1 + sentiment_data['score'])

#     output = (
#         f"\n🇮🇳 **INDIAN MARKET PREDICTION: {ticker}**\n"
#         f"📅 Target: {date_str} (+{days_ahead} days)\n"
#         f"💰 **Current Price:** ₹{current_price:.2f}\n"
#         f"----------------------------------------\n"
#         f"🤖 **AI Model ({best_model}):** ₹{raw_prediction:.2f}\n"
#         f"📰 **News Sentiment:** {sentiment_data['summary']}\n"
#         f"   (Headlines: {sentiment_data.get('headlines', [])})\n"
#         f"----------------------------------------\n"
#         f"🎯 **FINAL ADJUSTED PRICE:** ₹{adjusted_price:.2f}\n"
#         f"----------------------------------------\n"
#     )
#     return output

# @mcp.tool()
# def get_stock_price(company_name: str, date_str: str) -> str:
#     return stock_logic(company_name, date_str)

# if __name__ == "__main__":
#     mcp.run()

























import sys
import os
from datetime import datetime

# ==========================================
# 🔧 PATH FIX (Critical for Imports)
# ==========================================
# This ensures Python can find 'servers.tools' regardless of where you run the command.
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from fastmcp import FastMCP
# Import our custom tools
from servers.tools import market_data, advanced_ml, scraper 

# Initialize FastMCP Server
mcp = FastMCP("StockQuantAgent")

# ==========================================
# 🧠 CORE LOGIC (Business Logic Layer)
# ==========================================
def stock_logic(company_name: str, date_str: str) -> str:
    """
    Orchestrates the prediction pipeline:
    1. Find Ticker (Smart Search)
    2. Get Data (Yahoo Finance)
    3. Predict (LSTM/ARIMA + News Sentiment)
    """
    
    # --- STEP 1: SMART TICKER SEARCH ---
    print(f"\n🔎 Searching for '{company_name}' in Indian Markets...")
    
    try:
        ticker = market_data.get_ticker_from_name(company_name)
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

    # --- STEP 2: DATA FETCHING & VALIDATION ---
    print(f"🇮🇳 Found Ticker: {ticker}. Fetching historical data...")
    
    # We fetch data immediately to verify if the ticker is valid
    df = market_data.fetch_historical_data(ticker, period="2y")
    
    # ERROR HANDLER: If data is empty, the ticker or spelling was wrong
    if df is None or len(df) < 10:
        return (f"❌ Error: Could not find market data for '{company_name}' (Ticker: {ticker}).\n"
                f"   • The company might be delisted.\n"
                f"   • Or you made a typo (e.g., 'Infoysys' instead of 'Infosys').\n"
                f"   👉 Please try checking the spelling.")

    current_price = df['Close'].iloc[-1]

    # --- STEP 3: DATE CALCULATION ---
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return "❌ Error: Date must be in YYYY-MM-DD format (e.g., 2025-12-19)."
        
    today = datetime.now().date()
    days_ahead = (target_date - today).days

    # --- SCENARIO A: PAST OR TODAY (Exact Price) ---
    if days_ahead <= 0:
        past_price = market_data.get_specific_historical_price(ticker, date_str)
        if past_price:
            return f"✅ ACTUAL Price for {ticker} on {date_str}: ₹{past_price:.2f}"
        else:
            return f"✅ Current Price for {ticker}: ₹{current_price:.2f} (Exact date data missing)"

    # --- SCENARIO B: FUTURE PREDICTION (Hybrid AI) ---
    if days_ahead > 365:
        return "⚠️ Prediction limited to 1 year (Markets are too volatile beyond that)."

    print(f"📊 Running AI Model Arena (ARIMA vs LSTM vs GRU)...")
    
    try:
        # A. Mathematical Prediction
        best_model, results = advanced_ml.race_models_and_predict(df, days_ahead)
        raw_prediction = results[best_model]['prediction']
        
        # B. News Sentiment Analysis
        print(f"🌍 Scraping Google News for Sentiment Adjustment...")
        sentiment_data = scraper.analyze_sentiment_from_news(ticker)
        sentiment_score = sentiment_data['score'] # e.g., 0.1 (Bullish) or -0.1 (Bearish)
        
        # C. Hybrid Calculation
        # Formula: Math_Price * (1 + Sentiment_Impact)
        adjusted_price = raw_prediction * (1 + sentiment_score)
        
        # Calculate Trend
        trend_direction = "📈 UP" if adjusted_price > current_price else "📉 DOWN"
        pct_change = ((adjusted_price - current_price) / current_price) * 100

        # --- STEP 4: FINAL OUTPUT ---
        output = (
            f"\n🇮🇳 **INDIAN MARKET PREDICTION: {ticker}**\n"
            f"📅 Target Date: {date_str} (+{days_ahead} days)\n"
            f"💰 **Current Price:** ₹{current_price:.2f}\n"
            f"----------------------------------------\n"
            f"🏆 **Winning Algo:** {best_model} (Raw: ₹{raw_prediction:.2f})\n"
            f"📰 **News Impact:** {sentiment_data.get('headlines', ['No news'])[0]}...\n"
            f"   (Sentiment Score: {sentiment_score:.2f})\n"
            f"----------------------------------------\n"
            f"🎯 **FINAL PREDICTED PRICE:** ₹{adjusted_price:.2f}\n"
            f"📊 **Trend:** {trend_direction} ({pct_change:+.2f}%)\n"
            f"----------------------------------------\n"
        )
        return output

    except Exception as e:
        return f"❌ Prediction Engine Error: {str(e)}"

# ==========================================
# 🔌 MCP INTERFACE (Exposed to Agents)
# ==========================================
@mcp.tool()
def get_stock_price(company_name: str, date_str: str) -> str:
    """
    Get stock price for Indian companies (Actual or Predicted).
    Args:
        company_name: Name of company (e.g. 'Infosys', 'Tata Motors')
        date_str: Date in YYYY-MM-DD
    """
    return stock_logic(company_name, date_str)

if __name__ == "__main__":
    print("🚀 StockQuantAgent Server Running...")
    mcp.run()