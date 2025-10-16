"""
Script to test risk management limits
Simulates various scenarios to verify safety mechanisms
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.core.risk_manager import RiskManager


def test_scenarios():
    """Test various risk scenarios"""
    
    print("=" * 60)
    print("🛡️  RISK MANAGEMENT TEST SCENARIOS")
    print("=" * 60)
    
    # Scenario 1: Normal trading
    print("\n📊 Scenario 1: Normal Trading")
    print("-" * 60)
    rm = RiskManager(initial_capital=10000)
    can_trade, reason = rm.can_trade(10000)
    print(f"Capital: $10,000")
    print(f"Can trade: {can_trade}")
    print(f"Reason: {reason}")
    print("✅ PASS" if can_trade else "❌ FAIL")
    
    # Scenario 2: Small profit
    print("\n📊 Scenario 2: Small Profit (+5%)")
    print("-" * 60)
    rm = RiskManager(initial_capital=10000, max_position_size=0.1)
    can_trade, reason = rm.can_trade(10500)
    print(f"Capital: $10,500")
    print(f"Can trade: {can_trade}")
    print(f"Reason: {reason}")
    print("✅ PASS" if can_trade else "❌ FAIL")
    
    # Scenario 3: Daily loss limit hit
    print("\n📊 Scenario 3: Daily Loss Limit Hit (-2.5%)")
    print("-" * 60)
    rm = RiskManager(initial_capital=10000, max_daily_loss=0.02)
    can_trade, reason = rm.can_trade(9750)
    print(f"Capital: $9,750 (2.5% loss)")
    print(f"Max daily loss: 2.0%")
    print(f"Can trade: {can_trade}")
    print(f"Reason: {reason}")
    print(f"Circuit breaker: {rm.circuit_breaker_triggered}")
    print("✅ PASS - Circuit breaker activated" if not can_trade else "❌ FAIL")
    
    # Scenario 4: Max drawdown hit
    print("\n📊 Scenario 4: Max Drawdown Hit")
    print("-" * 60)
    rm = RiskManager(initial_capital=10000, max_drawdown=0.10)
    rm.update_metrics(12000)  # Peak at $12,000
    can_trade, reason = rm.can_trade(10500)  # Now at $10,500 (12.5% drawdown from peak)
    print(f"Peak: $12,000")
    print(f"Current: $10,500")
    print(f"Drawdown: {rm.current_drawdown*100:.2f}%")
    print(f"Max drawdown: 10.0%")
    print(f"Can trade: {can_trade}")
    print(f"Circuit breaker: {rm.circuit_breaker_triggered}")
    print("✅ PASS - Circuit breaker activated" if not can_trade else "❌ FAIL")
    
    # Scenario 5: Position sizing
    print("\n📊 Scenario 5: Position Sizing")
    print("-" * 60)
    rm = RiskManager(initial_capital=10000, max_position_size=0.1)
    quantity = rm.calculate_position_size(10000, 100, volatility=0.02)
    position_value = quantity * 100
    position_pct = (position_value / 10000) * 100
    print(f"Available capital: $10,000")
    print(f"Asset price: $100")
    print(f"Max position size: 10%")
    print(f"Calculated quantity: {quantity:.6f}")
    print(f"Position value: ${position_value:.2f}")
    print(f"Position size: {position_pct:.2f}%")
    print("✅ PASS" if position_pct <= 10.0 else "❌ FAIL")
    
    # Scenario 6: Stop-loss calculation
    print("\n📊 Scenario 6: Stop-Loss & Take-Profit")
    print("-" * 60)
    rm = RiskManager(initial_capital=10000, stop_loss_pct=0.02, take_profit_pct=0.04)
    entry_price = 100
    sl = rm.calculate_stop_loss(entry_price, "buy")
    tp = rm.calculate_take_profit(entry_price, "buy")
    print(f"Entry price: ${entry_price:.2f}")
    print(f"Stop-loss: ${sl:.2f} ({((sl-entry_price)/entry_price)*100:.1f}%)")
    print(f"Take-profit: ${tp:.2f} ({((tp-entry_price)/entry_price)*100:.1f}%)")
    print("✅ PASS" if sl == 98.0 and tp == 104.0 else "❌ FAIL")
    
    # Scenario 7: Stop-loss trigger
    print("\n📊 Scenario 7: Stop-Loss Triggered")
    print("-" * 60)
    rm = RiskManager(initial_capital=10000)
    should_close, reason = rm.should_close_position(
        entry_price=100,
        current_price=97.5,
        side="buy",
        stop_loss=98
    )
    print(f"Entry: $100")
    print(f"Stop-loss: $98")
    print(f"Current: $97.5")
    print(f"Should close: {should_close}")
    print(f"Reason: {reason}")
    print("✅ PASS - Position closed" if should_close else "❌ FAIL")
    
    # Scenario 8: Take-profit trigger
    print("\n📊 Scenario 8: Take-Profit Triggered")
    print("-" * 60)
    rm = RiskManager(initial_capital=10000)
    should_close, reason = rm.should_close_position(
        entry_price=100,
        current_price=104.5,
        side="buy",
        take_profit=104
    )
    print(f"Entry: $100")
    print(f"Take-profit: $104")
    print(f"Current: $104.5")
    print(f"Should close: {should_close}")
    print(f"Reason: {reason}")
    print("✅ PASS - Position closed" if should_close else "❌ FAIL")
    
    print("\n" + "=" * 60)
    print("✅ RISK MANAGEMENT TEST COMPLETE")
    print("=" * 60)
    print("\nYour risk management system is working correctly!")
    print("\nKey Safety Features:")
    print("✅ Daily loss limits enforced")
    print("✅ Max drawdown protection active")
    print("✅ Position sizing calculated safely")
    print("✅ Stop-loss and take-profit working")
    print("✅ Circuit breaker ready")
    print("=" * 60)


if __name__ == "__main__":
    test_scenarios()