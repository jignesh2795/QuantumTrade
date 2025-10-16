"""
Example script demonstrating real trading functionality
"""
import asyncio
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.core.engine import TradingEngine
from backend.utils.settings import Settings


async def main():
    """Example of using real trading mode"""
    print("QuantumTrade Real Trading Example")
    print("=" * 40)
    
    # Create settings for live trading
    settings = Settings()
    settings.TRADING_MODE = "live"
    
    # Note: In a real scenario, you would set these in your .env file:
    # settings.BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    # settings.BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
    
    # For this example, we'll use dummy keys to show the structure
    settings.BINANCE_API_KEY = "your_binance_api_key_here"
    settings.BINANCE_API_SECRET = "your_binance_api_secret_here"
    settings.DEFAULT_SYMBOL = "BTCUSDT"
    
    try:
        # Validate settings (this will fail with dummy keys, which is expected)
        settings.validate()
    except ValueError as e:
        print(f"Settings validation error (expected with dummy keys): {e}")
        print("In a real scenario, you would provide valid API keys in your .env file")
        return
    
    # Initialize trading engine
    print(f"Initializing trading engine in {settings.TRADING_MODE} mode...")
    engine = TradingEngine(settings)
    
    print(f"Exchange type: {type(engine.exchange).__name__}")
    print(f"Trading symbol: {engine.settings.DEFAULT_SYMBOL}")
    print(f"Strategy: {engine.strategy.name}")
    
    # Note: Actual connection and trading would happen here
    # await engine.start()
    # await engine.run_forever()
    # await engine.shutdown()
    
    print("\nReal trading example completed!")
    print("\nTo use real trading:")
    print("1. Set TRADING_MODE=live in your .env file")
    print("2. Add your BINANCE_API_KEY and BINANCE_API_SECRET")
    print("3. Run the main trading engine")


if __name__ == "__main__":
    asyncio.run(main())