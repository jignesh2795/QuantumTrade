"""
Test script to verify Binance API connection
Run this before live trading to ensure everything works
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.core.binance_exchange import BinanceExchange
from backend.utils.settings import settings
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


async def test_connection():
    """Test Binance connection and API"""
    
    print("=" * 60)
    print("🧪 BINANCE CONNECTION TEST")
    print("=" * 60)
    
    if not settings.API_KEY or not settings.API_SECRET:
        print("❌ API_KEY and API_SECRET not configured")
        print("Please update your .env file")
        return False
    
    # Create exchange
    exchange = BinanceExchange(
        api_key=settings.API_KEY,
        api_secret=settings.API_SECRET,
        testnet=settings.USE_TESTNET
    )
    
    try:
        # Test 1: Connection
        print("\n1️⃣  Testing connection...")
        connected = await exchange.connect()
        if connected:
            print("   ✅ Connection successful")
        else:
            print("   ❌ Connection failed")
            return False
        
        # Test 2: Get account info
        print("\n2️⃣  Testing authentication...")
        account = await exchange.get_account_info()
        print(f"   ✅ Account type: {account.get('accountType', 'N/A')}")
        print(f"   ✅ Can trade: {account.get('canTrade', False)}")
        
        # Test 3: Get current price
        print("\n3️⃣  Testing market data...")
        symbol = settings.DEFAULT_SYMBOL
        price = await exchange.get_current_price(symbol)
        print(f"   ✅ {symbol} price: ${price:,.2f}")
        
        # Test 4: Get balance
        print("\n4️⃣  Testing balance retrieval...")
        balance = await exchange.get_balance()
        print(f"   ✅ Cash: ${balance['cash']:,.2f}")
        print(f"   ✅ Total: ${balance['total']:,.2f}")
        
        # Test 5: Get candles
        print("\n5️⃣  Testing historical data...")
        candles = await exchange.get_candles(symbol, "1h", limit=10)
        print(f"   ✅ Retrieved {len(candles)} candles")
        if candles:
            latest = candles[-1]
            print(f"   ✅ Latest: Open=${latest.open:.2f}, Close=${latest.close:.2f}")
        
        # Test 6: Check positions
        print("\n6️⃣  Testing positions...")
        positions = await exchange.get_positions()
        print(f"   ✅ Open positions: {len(positions)}")
        for pos in positions[:3]:  # Show first 3
            print(f"      - {pos['symbol']}: {pos['quantity']:.6f} @ ${pos['current_price']:.2f}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print("\nYou're ready to start trading!")
        print(f"Mode: {'Testnet' if settings.USE_TESTNET else '🔴 LIVE'}")
        print(f"Symbol: {symbol}")
        print(f"Balance: ${balance['cash']:,.2f}")
        print("\nNext steps:")
        print("1. Review your risk settings in .env")
        print("2. Run: python main.py")
        print("=" * 60)
        
        await exchange.disconnect()
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("\nTroubleshooting:")
        print("1. Check your API_KEY and API_SECRET")
        print("2. Verify API has trading permissions")
        print("3. Check IP whitelist on Binance")
        print("4. Ensure you're using correct testnet/live settings")
        await exchange.disconnect()
        return False


if __name__ == "__main__":
    result = asyncio.run(test_connection())
    sys.exit(0 if result else 1)