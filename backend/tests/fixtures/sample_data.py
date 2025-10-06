"""
Sample test data for QuantumTrade
"""
import pytest

@pytest.fixture
def sample_portfolio():
    """Sample portfolio data for testing"""
    return {
        "assets": [
            {"symbol": "AAPL", "quantity": 10, "price": 150.00, "value": 1500.00},
            {"symbol": "GOOGL", "quantity": 5, "price": 2500.00, "value": 12500.00},
            {"symbol": "TSLA", "quantity": 20, "price": 200.00, "value": 4000.00}
        ],
        "total_value": 18000.00
    }

@pytest.fixture
def sample_market_data():
    """Sample market data for testing"""
    return [
        {"symbol": "AAPL", "price": 150.00},
        {"symbol": "GOOGL", "price": 2500.00},
        {"symbol": "TSLA", "price": 200.00}
    ]