"""
Simple test for Phase 2 components
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_risk_manager():
    """Test risk manager"""
    try:
        from backend.core.risk_manager import RiskManager
        rm = RiskManager(10000)
        print("✅ RiskManager imported and initialized successfully")
        return True
    except Exception as e:
        print(f"❌ RiskManager test failed: {e}")
        return False

def test_binance_exchange():
    """Test binance exchange"""
    try:
        from backend.core.binance_exchange import BinanceExchange
        print("✅ BinanceExchange imported successfully")
        return True
    except Exception as e:
        print(f"❌ BinanceExchange test failed: {e}")
        return False

def test_notifications():
    """Test notifications"""
    try:
        from backend.utils.notifications import NotificationManager
        nm = NotificationManager()
        print("✅ NotificationManager imported and initialized successfully")
        return True
    except Exception as e:
        print(f"❌ NotificationManager test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Phase 2 components...")
    print("=" * 50)
    
    tests = [
        test_risk_manager,
        test_binance_exchange,
        test_notifications
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 50)
    print(f"Passed: {passed}/{len(tests)} tests")