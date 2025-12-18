import sys
import os

# Path Fix to find the servers folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# IMPORT THE LOGIC FUNCTION, NOT THE TOOL
from servers.mcp_server import stock_logic

def main():
    print("📈 AI Stock Price Predictor (FastMCP Architecture)")
    print("------------------------------------------------")
    
    while True:
        company = input("\nEnter Company Name (or 'q' to quit): ").strip()
        if company.lower() == 'q':
            break
            
        date = input("Enter Date (YYYY-MM-DD): ").strip()
        
        try:
            print("\n🔄 Processing request...")
            # CALL THE LOGIC FUNCTION
            result = stock_logic(company, date) 
            print("\n" + result)
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()