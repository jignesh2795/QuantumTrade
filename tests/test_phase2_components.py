"""
Test Phase 2 components integration
"""
import pytest
from backend.core import BinanceExchange
from backend.core.engine import TradingEngine
from backend.utils.settings import Settings


def test_binance_exchange_import():
    """Test BinanceExchange import"""
    # Should be able to import BinanceExchange
    exchange = BinanceExchange("test_key", "test_secret")
    assert isinstance(exchange, BinanceExchange)
    assert exchange.api_key == "test_key"
    assert exchange.api_secret == "test_secret"


def test_engine_with_binance():
    """Test TradingEngine with Binance exchange"""
    settings = Settings()
    settings.TRADING_MODE = "live"
    settings.API_KEY = "test_key"
    settings.API_SECRET = "test_secret"
    settings.USE_TESTNET = True
    
    # Initialize engine with live trading mode
    engine = TradingEngine(settings)
    
    # Should have BinanceExchange instance
    assert isinstance(engine.exchange, BinanceExchange)
    assert engine.exchange.api_key == "test_key"
    assert engine.exchange.api_secret == "test_secret"


def test_engine_mode_selection():
    """Test engine correctly selects exchange based on mode"""
    # Test paper mode
    paper_settings = Settings()
    paper_settings.TRADING_MODE = "paper"
    paper_engine = TradingEngine(paper_settings)
    from backend.core import PaperExchange
    assert isinstance(paper_engine.exchange, PaperExchange)
    
    # Test live mode
    live_settings = Settings()
    live_settings.TRADING_MODE = "live"
    live_settings.API_KEY = "test_key"
    live_settings.API_SECRET = "test_secret"
    live_engine = TradingEngine(live_settings)
    assert isinstance(live_engine.exchange, BinanceExchange)