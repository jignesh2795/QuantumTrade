"""
Test SMA Crossover strategy
"""
import pytest
from datetime import datetime, timedelta
from backend.strategies.sma_crossover import SMACrossoverStrategy, Signal
from backend.core.exchange_base import Candle


def create_mock_candles(num_candles: int, start_price: float = 100) -> list:
    """Create mock candles for testing"""
    candles = []
    now = datetime.utcnow()
    
    for i in range(num_candles):
        price = start_price + i * 0.5  # Gradually increasing
        candles.append(Candle(
            timestamp=now - timedelta(hours=num_candles-i),
            open=price,
            high=price + 1,
            low=price - 1,
            close=price,
            volume=1000
        ))
    
    return candles


def test_strategy_initialization():
    """Test strategy initialization"""
    strategy = SMACrossoverStrategy(fast_period=10, slow_period=30, symbol="BTCUSDT")
    assert strategy.fast_period == 10
    assert strategy.slow_period == 30
    assert strategy.symbol == "BTCUSDT"


def test_insufficient_data():
    """Test behavior with insufficient data"""
    strategy = SMACrossoverStrategy(fast_period=10, slow_period=30)
    candles = create_mock_candles(20)  # Less than slow_period
    
    signal = strategy.analyze(candles)
    
    assert signal.action == "hold"
    assert signal.confidence == 0.0


def test_bullish_crossover():
    """Test bullish crossover detection"""
    strategy = SMACrossoverStrategy(fast_period=5, slow_period=10)
    
    # Create candles with uptrend
    candles = create_mock_candles(50, start_price=100)
    
    signal = strategy.analyze(candles)
    
    # With uptrend, fast SMA should be above slow SMA
    assert signal.action in ["buy", "hold"]


def test_calculate_sma():
    """Test SMA calculation"""
    strategy = SMACrossoverStrategy()
    prices = [100, 102, 104, 106, 108]
    
    sma = strategy.calculate_sma(prices, 5)
    
    expected = sum(prices) / 5
    assert sma == expected


def test_update_position_state():
    """Test position state update"""
    strategy = SMACrossoverStrategy()
    assert strategy.position_open == False
    
    strategy.update_position_state(True)
    assert strategy.position_open == True
    
    strategy.update_position_state(False)
    assert strategy.position_open == False