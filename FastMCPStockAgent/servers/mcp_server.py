# import sys
# import os
# from datetime import datetime

# # ==========================================
# # 🔧 PATH FIX (Critical for Imports)
# # ==========================================
# # This ensures Python can find 'servers.tools' regardless of where you run the command.
# current_dir = os.path.dirname(os.path.abspath(__file__))
# root_dir = os.path.dirname(current_dir)
# sys.path.append(root_dir)

# from fastmcp import FastMCP
# # Import our custom tools
# from servers.tools import market_data, advanced_ml, scraper 

# # Initialize FastMCP Server
# mcp = FastMCP("StockQuantAgent")

# # ==========================================
# # 🧠 CORE LOGIC (Business Logic Layer)
# # ==========================================
# def stock_logic(company_name: str, date_str: str) -> str:
#     """
#     Orchestrates the prediction pipeline:
#     1. Find Ticker (Smart Search)
#     2. Get Data (Yahoo Finance)
#     3. Predict (LSTM/ARIMA + News Sentiment)
#     """
    
#     # --- STEP 1: SMART TICKER SEARCH ---
#     print(f"\n🔎 Searching for '{company_name}' in Indian Markets...")
    
#     try:
#         ticker = market_data.get_ticker_from_name(company_name)
#     except Exception as e:
#         return f"❌ Connection Error: {str(e)}"

#     # --- STEP 2: DATA FETCHING & VALIDATION ---
#     print(f"🇮🇳 Found Ticker: {ticker}. Fetching historical data...")
    
#     # We fetch data immediately to verify if the ticker is valid
#     df = market_data.fetch_historical_data(ticker, period="2y")
    
#     # ERROR HANDLER: If data is empty, the ticker or spelling was wrong
#     if df is None or len(df) < 10:
#         return (f"❌ Error: Could not find market data for '{company_name}' (Ticker: {ticker}).\n"
#                 f"   • The company might be delisted.\n"
#                 f"   • Or you made a typo (e.g., 'Infoysys' instead of 'Infosys').\n"
#                 f"   👉 Please try checking the spelling.")

#     current_price = df['Close'].iloc[-1]

#     # --- STEP 3: DATE CALCULATION ---
#     try:
#         target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#     except ValueError:
#         return "❌ Error: Date must be in YYYY-MM-DD format (e.g., 2025-12-19)."
        
#     today = datetime.now().date()
#     days_ahead = (target_date - today).days

#     # --- SCENARIO A: PAST OR TODAY (Exact Price) ---
#     if days_ahead <= 0:
#         past_price = market_data.get_specific_historical_price(ticker, date_str)
#         if past_price:
#             return f"✅ ACTUAL Price for {ticker} on {date_str}: ₹{past_price:.2f}"
#         else:
#             return f"✅ Current Price for {ticker}: ₹{current_price:.2f} (Exact date data missing)"

#     # --- SCENARIO B: FUTURE PREDICTION (Hybrid AI) ---
#     if days_ahead > 365:
#         return "⚠️ Prediction limited to 1 year (Markets are too volatile beyond that)."

#     print(f"📊 Running AI Model Arena (ARIMA vs LSTM vs GRU)...")
    
#     try:
#         # A. Mathematical Prediction
#         best_model, results = advanced_ml.race_models_and_predict(df, days_ahead)
#         raw_prediction = results[best_model]['prediction']
        
#         # B. News Sentiment Analysis
#         print(f"🌍 Scraping Google News for Sentiment Adjustment...")
#         sentiment_data = scraper.analyze_sentiment_from_news(ticker)
#         sentiment_score = sentiment_data['score'] # e.g., 0.1 (Bullish) or -0.1 (Bearish)
        
#         # C. Hybrid Calculation
#         # Formula: Math_Price * (1 + Sentiment_Impact)
#         adjusted_price = raw_prediction * (1 + sentiment_score)
        
#         # Calculate Trend
#         trend_direction = "📈 UP" if adjusted_price > current_price else "📉 DOWN"
#         pct_change = ((adjusted_price - current_price) / current_price) * 100

#         # --- STEP 4: FINAL OUTPUT ---
#         output = (
#             f"\n🇮🇳 **INDIAN MARKET PREDICTION: {ticker}**\n"
#             f"📅 Target Date: {date_str} (+{days_ahead} days)\n"
#             f"💰 **Current Price:** ₹{current_price:.2f}\n"
#             f"----------------------------------------\n"
#             f"🏆 **Winning Algo:** {best_model} (Raw: ₹{raw_prediction:.2f})\n"
#             f"📰 **News Impact:** {sentiment_data.get('headlines', ['No news'])[0]}...\n"
#             f"   (Sentiment Score: {sentiment_score:.2f})\n"
#             f"----------------------------------------\n"
#             f"🎯 **FINAL PREDICTED PRICE:** ₹{adjusted_price:.2f}\n"
#             f"📊 **Trend:** {trend_direction} ({pct_change:+.2f}%)\n"
#             f"----------------------------------------\n"
#         )
#         return output

#     except Exception as e:
#         return f"❌ Prediction Engine Error: {str(e)}"

# # ==========================================
# # 🔌 MCP INTERFACE (Exposed to Agents)
# # ==========================================
# @mcp.tool()
# def get_stock_price(company_name: str, date_str: str) -> str:
#     """
#     Get stock price for Indian companies (Actual or Predicted).
#     Args:
#         company_name: Name of company (e.g. 'Infosys', 'Tata Motors')
#         date_str: Date in YYYY-MM-DD
#     """
#     return stock_logic(company_name, date_str)

# if __name__ == "__main__":
#     print("🚀 StockQuantAgent Server Running...")
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
    2. Get Data (Yahoo Finance - 10 Years)
    3. Predict (LSTM/ARIMA + News Sentiment)
    """
    
    # --- STEP 1: SMART TICKER SEARCH ---
    print(f"\n🔎 Searching for '{company_name}' in Global Database...")
    
    try:
        ticker = market_data.get_ticker_from_name(company_name)
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

    # Identify Currency
    currency_symbol = market_data.get_currency_symbol(ticker)

    # --- STEP 2: DATA FETCHING (10 YEARS) ---
    print(f"🌍 Found Ticker: {ticker} ({currency_symbol}). Fetching 10 Years of Data...")
    
    # We fetch 10 years of data now for deep training
    df = market_data.fetch_historical_data(ticker, period="10y")
    
    # ERROR HANDLER: If data is empty, the ticker or spelling was wrong
    if df is None or len(df) < 50:
        return (f"❌ Error: Could not find market data for '{company_name}' (Ticker: {ticker}).\n"
                f"   • The company might be delisted.\n"
                f"   • Or you made a typo (e.g., 'Infoysys' instead of 'Infosys').\n"
                f"   👉 Please try checking the spelling.")

    current_price = df['Close'].iloc[-1]
    data_points = len(df)

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
            return f"✅ ACTUAL Price for {ticker} on {date_str}: {currency_symbol}{past_price:.2f}"
        else:
            return f"✅ Current Price for {ticker}: {currency_symbol}{current_price:.2f} (Exact date data missing)"

    # --- SCENARIO B: FUTURE PREDICTION (Hybrid AI) ---
    if days_ahead > 365:
        return "⚠️ Prediction limited to 1 year (Markets are too volatile beyond that)."

    print(f"🧠 Training AI Models on {data_points} records (Daily/Weekly/Yearly patterns)...")
    
    try:
        # A. Mathematical Prediction (The Race)
        best_model, results = advanced_ml.race_models_and_predict(df, days_ahead)
        raw_prediction = results[best_model]['prediction']
        
        # B. News Sentiment Analysis
        print(f"📰 Scraping Google News for Sentiment Adjustment...")
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
            f"\n🚀 **PREDICTION REPORT: {ticker}**\n"
            f"📅 Target Date: {date_str} (+{days_ahead} days)\n"
            f"📚 Data Used: 10 Years ({data_points} trading days)\n"
            f"💰 **Current Price:** {currency_symbol}{current_price:.2f}\n"
            f"----------------------------------------\n"
            f"🏆 **Winning Algo:** {best_model} (Raw: {currency_symbol}{raw_prediction:.2f})\n"
            f"📰 **News Impact:** {sentiment_data.get('headlines', ['No news'])[0]}...\n"
            f"   (Sentiment Score: {sentiment_score:.2f})\n"
            f"----------------------------------------\n"
            f"🎯 **FINAL PREDICTED PRICE:** {currency_symbol}{adjusted_price:.2f}\n"
            f"📊 **Trend:** {trend_direction} ({pct_change:+.2f}%)\n"
            f"----------------------------------------\n"
        )
        return output

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"❌ Prediction Engine Error: {str(e)}"

# ==========================================
# 🔌 MCP INTERFACE (Exposed to Agents)
# ==========================================
@mcp.tool()
def get_stock_price(company_name: str, date_str: str) -> str:
    """
    Get stock price for Global companies (India/US).
    Args:
        company_name: Name of company (e.g. 'Infosys', 'Dell', 'Tesla')
        date_str: Date in YYYY-MM-DD
    """
    return stock_logic(company_name, date_str)

if __name__ == "__main__":
    print("🚀 StockQuantAgent Server Running...")
    mcp.run()