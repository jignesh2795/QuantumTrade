"""
Test script for Binance exchange
"""
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.core.binance_exchange import BinanceExchange


async def test_binance():
    """Test Binance exchange functionality"""
    print("Testing Binance exchange...")
    
    # Initialize exchange (with dummy keys for testing)
    exchange = BinanceExchange("dummy_key", "dummy_secret")
    
    # Test initialization
    print(f"Exchange initialized: {exchange.__class__.__name__}")
    print(f"Base URL: {exchange.base_url}")
    
    # Test signature generation
    params = {"timestamp": 1234567890, "symbol": "BTCUSDT"}
    signature = exchange._generate_signature(params)
    print(f"Signature generated: {signature[:20]}... (truncated)")
    
    # Test price retrieval (will use default value since we have dummy keys)
    try:
        price = await exchange.get_current_price("BTCUSDT")
        print(f"Current BTCUSDT price: ${price}")
    except Exception as e:
        print(f"Price retrieval test completed (expected with dummy keys): {e}")
    
    print("Binance exchange test completed!")


if __name__ == "__main__":
    asyncio.run(test_binance())