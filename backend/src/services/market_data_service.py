"""
Service for fetching market data using aiohttp
"""
import aiohttp
import asyncio
from typing import Dict, List

class MarketDataService:
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_stock_price(self, symbol: str) -> Dict[str, float]:
        """
        Fetch stock price for a given symbol
        In a real implementation, this would call a financial API
        """
        # Simulate API call with delay
        await asyncio.sleep(0.1)
        # Return mock data
        return {
            "symbol": symbol,
            "price": 150.00 + hash(symbol) % 100  # Simple mock price
        }
    
    async def fetch_multiple_prices(self, symbols: List[str]) -> List[Dict[str, float]]:
        """
        Fetch prices for multiple symbols concurrently
        """
        tasks = [self.fetch_stock_price(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks)
        return results

# Example usage
async def main():
    symbols = ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN"]
    
    async with MarketDataService() as service:
        prices = await service.fetch_multiple_prices(symbols)
        for price in prices:
            print(f"{price['symbol']}: ${price['price']}")

if __name__ == "__main__":
    asyncio.run(main())