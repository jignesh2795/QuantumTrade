"""
Test Trading Engine Phase 2 functionality
"""
import pytest
import asyncio
from backend.core.engine import TradingEngine
from backend.utils.settings import Settings


def test_engine_initialization_with_risk_manager():
    """Test trading engine initialization with risk manager"""
    settings = Settings()
    settings.TRADING_MODE = "paper"
    settings.INITIAL_CAPITAL = 10000
    
    engine = TradingEngine(settings)
    
    # Check that risk manager is initialized
    assert hasattr(engine, 'risk_manager')
    assert engine.risk_manager.initial_capital == 10000
    assert engine.risk_manager.max_position_size == settings.MAX_POSITION_SIZE
    assert engine.risk_manager.max_daily_loss == settings.MAX_DAILY_LOSS
    assert engine.risk_manager.max_drawdown == settings.MAX_DRAWDOWN
    assert engine.risk_manager.stop_loss_pct == settings.STOP_LOSS_PCT
    assert engine.risk_manager.take_profit_pct == settings.TAKE_PROFIT_PCT


def test_engine_initialization_with_notification_manager():
    """Test trading engine initialization with notification manager"""
    settings = Settings()
    settings.TRADING_MODE = "paper"
    settings.INITIAL_CAPITAL = 10000
    
    engine = TradingEngine(settings)
    
    # Check that notification manager is initialized
    assert hasattr(engine, 'notifier')
    assert engine.notifier.email_enabled == settings.EMAIL_ENABLED


@pytest.mark.asyncio
async def test_engine_with_binance_exchange():
    """Test trading engine with Binance exchange"""
    settings = Settings()
    settings.TRADING_MODE = "live"
    settings.API_KEY = "test_key"
    settings.API_SECRET = "test_secret"
    settings.USE_TESTNET = True  # Use testnet for testing
    
    # Mock the validation to avoid user input
    original_validate = settings.validate
    settings.validate = lambda: True
    
    engine = TradingEngine(settings)
    
    # Check that Binance exchange is initialized
    from backend.core.binance_exchange import BinanceExchange
    assert isinstance(engine.exchange, BinanceExchange)
    assert engine.exchange.testnet == True
    assert engine.exchange.api_key == "test_key"
    assert engine.exchange.api_secret == "test_secret"
    
    # Restore original validate method
    settings.validate = original_validate


def test_engine_settings_validation():
    """Test engine settings validation"""
    settings = Settings()
    settings.TRADING_MODE = "live"
    settings.API_KEY = ""
    settings.API_SECRET = ""
    
    # Should raise ValueError for live trading without API keys
    with pytest.raises(ValueError, match="API_KEY and API_SECRET required for live trading"):
        settings.validate()


def test_engine_dry_run_mode():
    """Test engine dry run mode"""
    settings = Settings()
    settings.TRADING_MODE = "paper"
    settings.DRY_RUN = True
    
    engine = TradingEngine(settings)
    assert engine.settings.DRY_RUN == True