"""
Mock services for testing QuantumTrade
"""
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_api_client():
    """Mock API client for testing"""
    client = Mock()
    client.get_portfolio.return_value = {
        "assets": [],
        "total_value": 0.00
    }
    return client

@pytest.fixture
def mock_market_data_service():
    """Mock market data service for testing"""
    service = Mock()
    service.fetch_stock_price.return_value = {"symbol": "TEST", "price": 100.00}
    return service