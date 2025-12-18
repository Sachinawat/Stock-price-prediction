import sys
import os

# PATH FIX
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from fastmcp import FastMCP
from servers.tools import market_data, features, machine_learning
from datetime import datetime

# Initialize FastMCP Server
mcp = FastMCP("StockQuantAgent")

# ==========================================
# 🧠 CORE LOGIC (Pure Python - Callable)
# ==========================================
def stock_logic(company_name: str, date_str: str) -> str:
    """
    The actual business logic. Separated so it can be called by CLI or MCP.
    """
    # 1. Convert Name to Ticker
    try:
        ticker = market_data.get_ticker_from_name(company_name)
    except Exception as e:
        return f"Error connecting to tools: {str(e)}"
        
    if not ticker:
        return f"Error: Could not find ticker for {company_name}"

    print(f"📊 Analyzing {ticker} for date {date_str}...")

    # 2. Check Dates
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return "❌ Error: Date must be in YYYY-MM-DD format."
        
    today = datetime.now().date()

    # 3. SCENARIO A: Historical Data (Past/Today)
    if target_date <= today:
        price = market_data.get_specific_historical_price(ticker, date_str)
        if price:
            return f"✅ ACTUAL Price for {ticker} on {date_str}: ${price:.2f}"
        else:
            return f"❌ No market data found for {ticker} on {date_str} (Weekend/Holiday?)"

    # 4. SCENARIO B: Future Prediction (Machine Learning)
    else:
        print("🚀 Future date detected. Initializing AI Prediction pipeline...")
        
        # A. Get Data
        raw_df = market_data.fetch_historical_data(ticker, period="5y")
        
        # B. Feature Engineering
        processed_df = features.add_technical_indicators(raw_df)
        
        # C. Calculate Days to Forecast
        days_ahead = (target_date - today).days
        
        if days_ahead > 365:
            return "⚠️ Prediction too far in future. Please limit to 1 year."

        # D. Run XGBoost Recursive Prediction
        predicted_price = machine_learning.train_and_predict_recursive(processed_df, days_ahead)
        
        return (f"🤖 PREDICTED Price for {ticker} on {date_str} "
                f"(+{days_ahead} days): ${predicted_price:.2f}\n"
                f"Model: XGBoost Regressor | trained on {len(processed_df)} records.")

# ==========================================
# 🔌 MCP INTERFACE (The Wrapper)
# ==========================================
@mcp.tool()
def get_stock_price(company_name: str, date_str: str) -> str:
    """
    Main Orchestrator exposed to AI Agents.
    Input: Company Name (e.g., 'Apple') and Date ('YYYY-MM-DD').
    """
    # Simply call the core logic function
    return stock_logic(company_name, date_str)

if __name__ == "__main__":
    mcp.run()