"""
Test script to verify Binance API functionality
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from backend.core.binance_exchange import BinanceExchange
from backend.utils.settings import settings


async def test_binance_api():
    """Test Binance API functionality"""
    
    print("=" * 60)
    print("Binance API Functionality Test")
    print("=" * 60)
    
    # Check if API keys are configured
    if not settings.API_KEY or not settings.API_SECRET:
        print("❌ API keys not configured in .env")
        print("Please set API_KEY and API_SECRET in your .env file")
        return
    
    # Create exchange instance
    exchange = BinanceExchange(
        api_key=settings.API_KEY,
        api_secret=settings.API_SECRET,
        testnet=settings.USE_TESTNET
    )
    
    try:
        # Test 1: Connection
        print("\n1. Testing connection...")
        connected = await exchange.connect()
        if connected:
            print("   ✅ Connection successful")
        else:
            print("   ❌ Connection failed")
            return
        
        # Test 2: Get current price
        print("\n2. Testing current price retrieval...")
        symbol = settings.DEFAULT_SYMBOL
        try:
            price = await exchange.get_current_price(symbol)
            print(f"   ✅ {symbol} price: ${price:,.2f}")
        except Exception as e:
            print(f"   ❌ Failed to get price: {e}")
        
        # Test 3: Get candles
        print("\n3. Testing candle data retrieval...")
        try:
            candles = await exchange.get_candles(symbol, "1h", limit=5)
            print(f"   ✅ Retrieved {len(candles)} candles")
            if candles:
                latest = candles[-1]
                print(f"   ✅ Latest candle: Open=${latest.open:.2f}, Close=${latest.close:.2f}")
        except Exception as e:
            print(f"   ❌ Failed to get candles: {e}")
        
        # Test 4: Get account info
        print("\n4. Testing account information...")
        try:
            account_info = await exchange.get_account_info()
            print(f"   ✅ Account type: {account_info.get('accountType', 'N/A')}")
            print(f"   ✅ Can trade: {account_info.get('canTrade', False)}")
        except Exception as e:
            print(f"   ❌ Failed to get account info: {e}")
        
        # Test 5: Get balance
        print("\n5. Testing balance retrieval...")
        try:
            balance = await exchange.get_balance()
            print(f"   ✅ Cash: ${balance['cash']:,.2f}")
            print(f"   ✅ Total: ${balance['total']:,.2f}")
        except Exception as e:
            print(f"   ❌ Failed to get balance: {e}")
        
        # Test 6: Get positions
        print("\n6. Testing position retrieval...")
        try:
            positions = await exchange.get_positions()
            print(f"   ✅ Open positions: {len(positions)}")
            for pos in positions[:3]:  # Show first 3 positions
                print(f"      - {pos['symbol']}: {pos['quantity']:.6f} @ ${pos['current_price']:.2f}")
        except Exception as e:
            print(f"   ❌ Failed to get positions: {e}")
        
        print("\n" + "=" * 60)
        print("API Functionality Test Complete")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        # Disconnect
        await exchange.disconnect()
        print("Disconnected from Binance")


if __name__ == "__main__":
    asyncio.run(test_binance_api())