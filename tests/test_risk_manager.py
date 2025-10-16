"""
Test Risk Manager functionality
"""
import pytest
from backend.core.risk_manager import RiskManager


def test_risk_manager_initialization():
    """Test risk manager initialization"""
    rm = RiskManager(
        initial_capital=10000,
        max_position_size=0.1,
        max_daily_loss=0.02
    )
    
    assert rm.initial_capital == 10000
    assert rm.max_position_size == 0.1
    assert rm.max_daily_loss == 0.02
    assert rm.circuit_breaker_triggered == False


def test_can_trade_within_limits():
    """Test trading allowed within limits"""
    rm = RiskManager(initial_capital=10000)
    
    can_trade, reason = rm.can_trade(10000)
    
    assert can_trade == True
    assert "passed" in reason.lower()


def test_daily_loss_limit():
    """Test daily loss limit enforcement"""
    rm = RiskManager(initial_capital=10000, max_daily_loss=0.02)
    
    # Simulate 3% loss (exceeds 2% limit)
    current_capital = 9700
    can_trade, reason = rm.can_trade(current_capital)
    
    assert can_trade == False
    assert rm.circuit_breaker_triggered == True


def test_max_drawdown_limit():
    """Test max drawdown enforcement"""
    rm = RiskManager(initial_capital=10000, max_drawdown=0.10)
    
    # Set peak
    rm.update_metrics(12000)
    
    # Simulate 15% drawdown from peak (exceeds 10% limit)
    current_capital = 10200
    can_trade, reason = rm.can_trade(current_capital)
    
    assert can_trade == False
    assert rm.circuit_breaker_triggered == True


def test_position_sizing():
    """Test position size calculation"""
    rm = RiskManager(initial_capital=10000, max_position_size=0.1)
    
    quantity = rm.calculate_position_size(
        available_capital=10000,
        current_price=100,
        volatility=0.02
    )
    
    # With 10% max position, should be around 10 units
    assert 5 <= quantity <= 15  # Allow for volatility adjustment


def test_stop_loss_calculation():
    """Test stop-loss price calculation"""
    rm = RiskManager(initial_capital=10000, stop_loss_pct=0.02)
    
    # Buy position
    stop_loss = rm.calculate_stop_loss(entry_price=100, side="buy")
    assert stop_loss == 98.0  # 2% below entry
    
    # Sell position
    stop_loss = rm.calculate_stop_loss(entry_price=100, side="sell")
    assert stop_loss == 102.0  # 2% above entry


def test_take_profit_calculation():
    """Test take-profit price calculation"""
    rm = RiskManager(initial_capital=10000, take_profit_pct=0.04)
    
    # Buy position
    take_profit = rm.calculate_take_profit(entry_price=100, side="buy")
    assert take_profit == 104.0  # 4% above entry
    
    # Sell position
    take_profit = rm.calculate_take_profit(entry_price=100, side="sell")
    assert take_profit == 96.0  # 4% below entry


def test_should_close_position_stop_loss():
    """Test position closure on stop-loss"""
    rm = RiskManager(initial_capital=10000)
    
    # Buy position with stop-loss hit
    should_close, reason = rm.should_close_position(
        entry_price=100,
        current_price=97,  # Below stop-loss
        side="buy",
        stop_loss=98
    )
    
    assert should_close == True
    assert "stop-loss" in reason.lower()


def test_should_close_position_take_profit():
    """Test position closure on take-profit"""
    rm = RiskManager(initial_capital=10000)
    
    # Buy position with take-profit hit
    should_close, reason = rm.should_close_position(
        entry_price=100,
        current_price=105,  # Above take-profit
        side="buy",
        take_profit=104
    )
    
    assert should_close == True
    assert "take-profit" in reason.lower()


def test_risk_report():
    """Test risk report generation"""
    rm = RiskManager(initial_capital=10000)
    rm.update_metrics(9800)
    
    report = rm.get_risk_report()
    
    assert 'daily_pnl' in report
    assert 'current_drawdown' in report
    assert 'circuit_breaker_active' in report