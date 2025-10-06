import pytest
from src.utils.data_processor import calculate_portfolio_metrics, generate_price_series

def test_calculate_portfolio_metrics():
    portfolio_data = [
        {"symbol": "AAPL", "quantity": 10, "price": 150.00, "value": 1500.00},
        {"symbol": "GOOGL", "quantity": 5, "price": 2500.00, "value": 12500.00},
        {"symbol": "TSLA", "quantity": 20, "price": 200.00, "value": 4000.00}
    ]
    
    metrics = calculate_portfolio_metrics(portfolio_data)
    
    assert metrics['total_value'] == 18000.00
    assert metrics['position_count'] == 3
    assert metrics['max_position'] == 12500.00
    assert metrics['min_position'] == 1500.00

def test_calculate_portfolio_metrics_empty():
    metrics = calculate_portfolio_metrics([])
    assert metrics == {}

def test_generate_price_series():
    prices = generate_price_series(100.0, 5)
    assert len(prices) == 5
    # All prices should be positive
    assert all(p > 0 for p in prices)

if __name__ == "__main__":
    pytest.main([__file__])