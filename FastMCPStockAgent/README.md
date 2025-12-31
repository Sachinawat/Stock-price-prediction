# Stock Price Prediction (FastMCP Architecture)

## Overview
This application predicts stock prices using a hybrid approach: it fetches actual historical prices for past dates and uses machine learning (XGBoost) to forecast future prices. The system is built with a modular FastMCP agent architecture, making it easy to extend and integrate with other AI agents or tools.

## Features
- **Company Name to Ticker Mapping**: Enter a company name (e.g., "Apple") and the system maps it to its stock ticker (e.g., "AAPL").
- **Historical Price Lookup**: Retrieves the actual closing price for a given date using Yahoo Finance data
- **Future Price Prediction**: For future dates (up to 1 year ahead), predicts the price using an XGBoost regression model trained on technical indicators and lag features.
- **Command-Line Interface**: Simple CLI for user interaction.
- **Modular Design**: Clean separation between data fetching, feature engineering, and machine learning logic.

## Project Structure
```
FastMCPStockAgent/
	clients/
		client.py            # CLI entry point
	servers/
		mcp_server.py        # Main MCP server and logic
		tools/
			market_data.py     # Data fetching utilities
			features.py        # Feature engineering
			machine_learning.py# ML model training & prediction
	requirements.txt       # Python dependencies
README.md                # This file
```

## How It Works
1. **User Input**: Enter a company name and a date.
2. **Ticker Resolution**: The system maps the name to a stock ticker.
3. **Date Handling**:
	 - If the date is in the past or today, fetch the actual closing price.
	 - If the date is in the future (≤1 year ahead), run the ML pipeline to predict the price.
4. **Output**: Displays the actual or predicted price, with model details for predictions.

## Example Usage
```
python -m FastMCPStockAgent.clients.client

📈 AI Stock Price Predictor (FastMCP Architecture)
------------------------------------------------

Enter Company Name (or 'q' to quit): Apple
Enter Date (YYYY-MM-DD): 2025-12-18

🔄 Processing request...
🤖 PREDICTED Price for AAPL on 2025-12-18 (+365 days): $XXX.XX
Model: XGBoost Regressor | trained on N records.
```

## Requirements
- Python 3.8+
- See `FastMCPStockAgent/requirements.txt` for dependencies

## Installation
1. Clone the repository.
2. Install dependencies:
	 ```
	 pip install -r FastMCPStockAgent/requirements.txt
	 ```
3. Run the CLI:
	 
	 python -m FastMCPStockAgent.clients.client
	 

## Architecture
- **FastMCP**: Orchestrates tools and exposes the main interface for agent integration.
- **Tools**: Modular Python files for market data, feature engineering, and ML.
- **Client**: CLI for user interaction.

## Extending
- Add more companies to the mapping in `market_data.py` or integrate a search API.
- Improve feature engineering in `features.py`.
- Swap out the ML model in `machine_learning.py` for experimentation.

## License
See LICENSE file