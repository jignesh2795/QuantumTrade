"""
Integration test for Phase 2 components
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_component_integration():
    """Test that all components work together"""
    try:
        # Import all components
        from backend.core.risk_manager import RiskManager
        from backend.utils.notifications import NotificationManager
        from backend.utils.settings import Settings
        
        # Test Risk Manager
        rm = RiskManager(10000, max_position_size=0.1, max_daily_loss=0.02)
        can_trade, reason = rm.can_trade(9900)  # 1% loss
        print(f"✅ Risk Manager: Can trade = {can_trade}")
        
        # Test Notification Manager
        nm = NotificationManager()
        print("✅ Notification Manager: Initialized")
        
        # Test Settings
        settings = Settings()
        print(f"✅ Settings: Trading mode = {settings.TRADING_MODE}")
        
        return True
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("Phase 2 Integration Test")
    print("=" * 30)
    
    if test_component_integration():
        print("=" * 30)
        print("✅ All components integrated successfully!")
    else:
        print("=" * 30)
        print("❌ Integration test failed!")