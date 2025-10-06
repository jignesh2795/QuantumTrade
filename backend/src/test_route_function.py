from agents.data_agent import DataAgent

def get_historical_data(symbol: str = "BTC-USD", days: int = 30):
    agent = DataAgent()
    return agent.get_historical_data(symbol, days)

if __name__ == "__main__":
    result = get_historical_data("BTC-USD", 5)
    print(f"Result: {result}")