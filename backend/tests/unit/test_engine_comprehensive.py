"""
Comprehensive unit tests for the Trading Engine
"""
import pytest
import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.core.engine import TradingEngine
from backend.utils.settings import Settings
from backend.core.exchange_base import Candle, OrderResult
from backend.strategies.sma_crossover import Signal


@pytest.fixture
def mock_settings():
    """Create mock settings for testing"""
    settings = Mock(spec=Settings)
    settings.TRADING_MODE = "paper"
    settings.INITIAL_CAPITAL = 10000.0
    settings.SMA_FAST_PERIOD = 10
    settings.SMA_SLOW_PERIOD = 30
    settings.DEFAULT_SYMBOL = "BTCUSDT"
    settings.TIMEFRAME = "1h"
    settings.MAX_POSITION_SIZE = 0.1
    return settings


@pytest.fixture
def mock_exchange():
    """Create a mock exchange for testing"""
    exchange = AsyncMock()
    exchange.is_connected = False
    exchange.trade_history = []
    exchange.positions = {}
    return exchange


@pytest.fixture
def mock_strategy():
    """Create a mock strategy for testing"""
    strategy = Mock()
    strategy.name = "SMA_10_30"
    strategy.position_open = False
    return strategy


@pytest.mark.asyncio
async def test_engine_initialization(mock_settings, mock_exchange, mock_strategy):
    """Test TradingEngine initialization"""
    # Mock the exchange and strategy classes
    with patch('backend.core.engine.PaperExchange', return_value=mock_exchange), \
         patch('backend.core.engine.SMACrossoverStrategy', return_value=mock_strategy):
        
        engine = TradingEngine(mock_settings)
        
        # Verify engine attributes
        assert engine.settings == mock_settings
        assert engine.is_running == False
        assert engine.trade_count == 0
        assert engine.exchange == mock_exchange
        assert engine.strategy == mock_strategy


@pytest.mark.asyncio
async def test_engine_start(mock_settings, mock_exchange, mock_strategy):
    """Test TradingEngine start method"""
    with patch('backend.core.engine.PaperExchange', return_value=mock_exchange), \
         patch('backend.core.engine.SMACrossoverStrategy', return_value=mock_strategy):
        
        engine = TradingEngine(mock_settings)
        await engine.start()
        
        # Verify exchange connect was called
        mock_exchange.connect.assert_called_once()
        assert engine.is_running == True


@pytest.mark.asyncio
async def test_engine_shutdown(mock_settings, mock_exchange, mock_strategy):
    """Test TradingEngine shutdown method"""
    with patch('backend.core.engine.PaperExchange', return_value=mock_exchange), \
         patch('backend.core.engine.SMACrossoverStrategy', return_value=mock_strategy):
        
        engine = TradingEngine(mock_settings)
        await engine.start()  # Start the engine first
        
        # Mock the get_balance method to return a proper dictionary
        mock_exchange.get_balance.return_value = {
            "cash": 10000.0,
            "total": 10000.0,
            "pnl": 0.0,
            "pnl_pct": 0.0
        }
        
        await engine.shutdown()
        
        # Verify exchange disconnect was called
        mock_exchange.disconnect.assert_called_once()
        assert engine.is_running == False


@pytest.mark.asyncio
async def test_trading_cycle_hold_signal(mock_settings, mock_exchange, mock_strategy):
    """Test trading cycle with HOLD signal"""
    with patch('backend.core.engine.PaperExchange', return_value=mock_exchange), \
         patch('backend.core.engine.SMACrossoverStrategy', return_value=mock_strategy):
        
        engine = TradingEngine(mock_settings)
        
        # Mock exchange methods
        mock_exchange.get_candles.return_value = [
            Candle(timestamp=datetime.now(), open=40000, high=41000, low=39000, close=40500, volume=1000)
        ] * 30  # 30 candles for SMA calculation
        mock_exchange.get_current_price.return_value = 40500.0
        mock_exchange.get_balance.return_value = {
            "cash": 10000.0,
            "total": 10000.0,
            "pnl": 0.0,
            "pnl_pct": 0.0
        }
        mock_exchange.get_positions.return_value = []
        
        # Mock strategy to return HOLD signal
        mock_strategy.analyze.return_value = Signal(
            action="hold",
            symbol="BTCUSDT",
            confidence=0.0,
            price=40500.0,
            reason="No crossover",
            timestamp=datetime.now().isoformat()
        )
        mock_strategy.update_position_state.return_value = None
        
        # Run one trading cycle
        await engine.trading_cycle()
        
        # Verify methods were called
        mock_exchange.get_candles.assert_called_once()
        mock_exchange.get_current_price.assert_called_once()
        mock_exchange.get_balance.assert_called_once()
        mock_exchange.get_positions.assert_called_once()
        mock_strategy.analyze.assert_called_once()
        mock_strategy.update_position_state.assert_called_once()


@pytest.mark.asyncio
async def test_execute_buy_order(mock_settings, mock_exchange, mock_strategy):
    """Test executing a buy order"""
    with patch('backend.core.engine.PaperExchange', return_value=mock_exchange), \
         patch('backend.core.engine.SMACrossoverStrategy', return_value=mock_strategy):
        
        engine = TradingEngine(mock_settings)
        engine.trade_count = 0
        
        # Mock exchange place_order to return filled order
        mock_exchange.place_order.return_value = OrderResult(
            order_id="test_order_123",
            symbol="BTCUSDT",
            side="buy",
            quantity=0.024691,  # This is what gets calculated in the actual code
            price=40500.0,
            status="filled",
            filled_quantity=0.024691,
            avg_fill_price=40500.0,
            timestamp=datetime.now()
        )
        
        # Execute buy order
        await engine.execute_buy("BTCUSDT", 40500.0, 10000.0)
        
        # Verify order was placed (we'll check it was called, but not with specific quantity)
        mock_exchange.place_order.assert_called_once()
        assert engine.trade_count == 1


@pytest.mark.asyncio
async def test_execute_sell_order(mock_settings, mock_exchange, mock_strategy):
    """Test executing a sell order"""
    with patch('backend.core.engine.PaperExchange', return_value=mock_exchange), \
         patch('backend.core.engine.SMACrossoverStrategy', return_value=mock_strategy):
        
        engine = TradingEngine(mock_settings)
        engine.trade_count = 0
        
        # Mock exchange place_order to return filled order
        mock_exchange.place_order.return_value = OrderResult(
            order_id="test_order_456",
            symbol="BTCUSDT",
            side="sell",
            quantity=0.1,
            price=41000.0,
            status="filled",
            filled_quantity=0.1,
            avg_fill_price=41000.0,
            timestamp=datetime.now()
        )
        
        # Execute sell order
        position = {
            "quantity": 0.1,
            "current_price": 41000.0
        }
        await engine.execute_sell("BTCUSDT", position)
        
        # Verify order was placed
        mock_exchange.place_order.assert_called_once_with(
            symbol="BTCUSDT",
            side="sell",
            quantity=0.1,
            price=41000.0,
            order_type="market"
        )
        assert engine.trade_count == 1


@pytest.mark.asyncio
async def test_print_summary(mock_settings, mock_exchange, mock_strategy):
    """Test printing trading summary"""
    with patch('backend.core.engine.PaperExchange', return_value=mock_exchange), \
         patch('backend.core.engine.SMACrossoverStrategy', return_value=mock_strategy):
        
        engine = TradingEngine(mock_settings)
        engine.trade_count = 5
        mock_exchange.trade_history = ["order1", "order2", "order3"]
        
        # Mock exchange get_balance with proper return values
        mock_exchange.get_balance.return_value = {
            "cash": 9500.0,
            "total": 10250.0,
            "pnl": 250.0,
            "pnl_pct": 2.5
        }
        
        # Call print_summary (this will just log, but we want to ensure it doesn't crash)
        await engine.print_summary()
        
        # Verify get_balance was called
        mock_exchange.get_balance.assert_called_once()