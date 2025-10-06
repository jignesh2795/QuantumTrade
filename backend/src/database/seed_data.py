"""
Sample seed data for local development and testing
"""
import json

# Sample portfolio data
portfolio_data = [
    {
        "symbol": "AAPL",
        "quantity": 10,
        "purchase_price": 145.00,
        "current_price": 150.00
    },
    {
        "symbol": "GOOGL",
        "quantity": 5,
        "purchase_price": 2400.00,
        "current_price": 2500.00
    },
    {
        "symbol": "TSLA",
        "quantity": 20,
        "purchase_price": 180.00,
        "current_price": 200.00
    }
]

# Sample trade data
trade_data = [
    {
        "symbol": "AAPL",
        "trade_type": "BUY",
        "quantity": 10,
        "price": 145.00
    },
    {
        "symbol": "GOOGL",
        "trade_type": "BUY",
        "quantity": 5,
        "price": 2400.00
    }
]

# Sample market data
market_data = [
    {"symbol": "AAPL", "price": 150.00},
    {"symbol": "GOOGL", "price": 2500.00},
    {"symbol": "TSLA", "price": 200.00},
    {"symbol": "MSFT", "price": 300.00},
    {"symbol": "AMZN", "price": 3200.00}
]

def get_sample_portfolio():
    """Get sample portfolio data"""
    return portfolio_data

def get_sample_trades():
    """Get sample trade data"""
    return trade_data

def get_sample_market_data():
    """Get sample market data"""
    return market_data

if __name__ == "__main__":
    print("Sample Portfolio Data:")
    print(json.dumps(portfolio_data, indent=2))
    
    print("\nSample Trade Data:")
    print(json.dumps(trade_data, indent=2))
    
    print("\nSample Market Data:")
    print(json.dumps(market_data, indent=2))