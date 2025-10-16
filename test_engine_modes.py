"""
Test script for trading engine with different modes
"""
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.core.engine import TradingEngine
from backend.utils.settings import Settings


async def test_paper_mode():
    """Test trading engine in paper mode"""
    print("Testing Paper Trading Mode...")
    
    # Create settings for paper trading
    settings = Settings()
    settings.TRADING_MODE = "paper"
    settings.INITIAL_CAPITAL = 10000
    
    # Initialize engine
    engine = TradingEngine(settings)
    
    # Test initialization
    print(f"Engine initialized with {engine.settings.TRADING_MODE} mode")
    print(f"Exchange type: {type(engine.exchange).__name__}")
    
    print("Paper trading mode test completed!")


async def test_live_mode():
    """Test trading engine in live mode"""
    print("Testing Live Trading Mode...")
    
    # Create settings for live trading (with dummy keys)
    settings = Settings()
    settings.TRADING_MODE = "live"
    settings.BINANCE_API_KEY = "dummy_key"
    settings.BINANCE_API_SECRET = "dummy_secret"
    
    # Initialize engine
    engine = TradingEngine(settings)
    
    # Test initialization
    print(f"Engine initialized with {engine.settings.TRADING_MODE} mode")
    print(f"Exchange type: {type(engine.exchange).__name__}")
    
    print("Live trading mode test completed!")


async def main():
    """Run all tests"""
    await test_paper_mode()
    print()
    await test_live_mode()


if __name__ == "__main__":
    asyncio.run(main())