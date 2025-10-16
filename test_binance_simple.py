"""
Simple test for Binance exchange component
"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

async def test_binance_imports():
    """Test that we can import and instantiate BinanceExchange"""
    try:
        from backend.core.binance_exchange import BinanceExchange
        
        # Create an instance (without real API keys)
        exchange = BinanceExchange(
            api_key="test_key",
            api_secret="test_secret",
            testnet=True
        )
        
        print("✅ BinanceExchange imported and instantiated successfully")
        print(f"   Base URL: {exchange.BASE_URL}")
        print(f"   Testnet: {exchange.testnet}")
        
        return True
    except Exception as e:
        print(f"❌ BinanceExchange test failed: {e}")
        return False

async def test_binance_methods():
    """Test that BinanceExchange methods exist"""
    try:
        from backend.core.binance_exchange import BinanceExchange
        
        # Check that required methods exist
        exchange = BinanceExchange("test", "test")
        
        required_methods = [
            'connect', 'disconnect', '_generate_signature', '_signed_request',
            'get_account_info', 'get_current_price', 'get_candles',
            'place_order', 'cancel_order', 'get_order_status',
            'get_balance', 'get_positions'
        ]
        
        for method in required_methods:
            if hasattr(exchange, method):
                print(f"   ✅ Method '{method}' exists")
            else:
                print(f"   ❌ Method '{method}' missing")
                return False
        
        print("✅ All required BinanceExchange methods present")
        return True
    except Exception as e:
        print(f"❌ BinanceExchange methods test failed: {e}")
        return False

async def main():
    print("Testing Binance Exchange components...")
    print("=" * 50)
    
    tests = [
        test_binance_imports(),
        test_binance_methods()
    ]
    
    results = await asyncio.gather(*tests)
    passed = sum(results)
    
    print("=" * 50)
    print(f"Passed: {passed}/{len(results)} tests")

if __name__ == "__main__":
    asyncio.run(main())