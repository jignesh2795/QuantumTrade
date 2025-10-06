import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.data_agent import DataAgent

def test_data_agent():
    agent = DataAgent()
    print("DataAgent created successfully")
    
    # Test price retrieval
    result = agent.get_price("BTC-USD")
    print(f"Price result: {result}")
    
    # Test historical data
    result = agent.get_historical_data("BTC-USD", 5)
    print(f"Historical data result: {result}")

if __name__ == "__main__":
    test_data_agent()