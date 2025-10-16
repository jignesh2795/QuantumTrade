"""
Test script for Phase 2 components
"""
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.core.risk_manager import RiskManager
from backend.core.binance_exchange import BinanceExchange
from backend.utils.notifications import NotificationManager
from backend.utils.settings import Settings
from backend.core.engine import TradingEngine


async def test_risk_manager():
    """Test risk manager functionality"""
    print("Testing Risk Manager...")
    
    rm = RiskManager(
        initial_capital=10000,
        max_position_size=0.1,
        max_daily_loss=0.02,
        max_drawdown=0.10,
        stop_loss_pct=0.02,
        take_profit_pct=0.04
    )
    
    print(f"Risk Manager initialized with capital: ${rm.initial_capital:,.2f}")
    
    # Test position sizing
    quantity = rm.calculate_position_size(available_capital=10000, current_price=100)
    print(f"Position size for $100 asset with $10000 capital: {quantity}")
    
    # Test stop loss calculation
    stop_loss = rm.calculate_stop_loss(entry_price=100, side="buy")
    print(f"Stop loss for buy at $100: ${stop_loss}")
    
    # Test risk check
    can_trade, reason = rm.can_trade(10000)
    print(f"Can trade with $10000: {can_trade} - {reason}")
    
    print("Risk Manager test completed!\n")


async def test_notification_manager():
    """Test notification manager functionality"""
    print("Testing Notification Manager...")
    
    nm = NotificationManager(email_enabled=False)
    print(f"Notification Manager initialized - Email enabled: {nm.email_enabled}")
    
    print("Notification Manager test completed!\n")


async def test_binance_exchange():
    """Test Binance exchange functionality"""
    print("Testing Binance Exchange...")
    
    # Initialize with dummy keys for testing
    exchange = BinanceExchange(
        api_key="dummy_key",
        api_secret="dummy_secret",
        testnet=True
    )
    
    print(f"Binance Exchange initialized - Testnet: {exchange.testnet}")
    print(f"Base URL: {exchange.BASE_URL}")
    
    print("Binance Exchange test completed!\n")


async def test_trading_engine():
    """Test trading engine functionality"""
    print("Testing Trading Engine...")
    
    # Create settings for paper trading
    settings = Settings()
    settings.TRADING_MODE = "paper"
    settings.INITIAL_CAPITAL = 10000
    
    # Initialize engine
    engine = TradingEngine(settings)
    
    print(f"Trading Engine initialized with {engine.settings.TRADING_MODE} mode")
    print(f"Exchange type: {type(engine.exchange).__name__}")
    print(f"Risk Manager: {type(engine.risk_manager).__name__}")
    print(f"Notification Manager: {type(engine.notification_manager).__name__}")
    
    print("Trading Engine test completed!\n")


async def main():
    """Run all tests"""
    print("Phase 2 Components Test")
    print("=" * 30)
    
    await test_risk_manager()
    await test_notification_manager()
    await test_binance_exchange()
    await test_trading_engine()
    
    print("All Phase 2 tests completed!")


if __name__ == "__main__":
    asyncio.run(main())