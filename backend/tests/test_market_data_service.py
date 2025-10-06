import pytest
import asyncio
from src.services.market_data_service import MarketDataService

@pytest.mark.asyncio
async def test_fetch_stock_price():
    async with MarketDataService() as service:
        result = await service.fetch_stock_price("AAPL")
        assert "symbol" in result
        assert "price" in result
        assert result["symbol"] == "AAPL"

@pytest.mark.asyncio
async def test_fetch_multiple_prices():
    symbols = ["AAPL", "GOOGL", "TSLA"]
    
    async with MarketDataService() as service:
        results = await service.fetch_multiple_prices(symbols)
        assert len(results) == len(symbols)
        for result in results:
            assert "symbol" in result
            assert "price" in result
            assert result["symbol"] in symbols

if __name__ == "__main__":
    pytest.main([__file__])