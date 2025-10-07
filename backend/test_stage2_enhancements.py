"""
Test script for Stage 2 enhancements to QuantumTrade platform
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Use absolute imports
from agents.data_agent import DataAgent
from agents.strategy_agent import StrategyAgent
from agents.risk_agent import RiskAgent
from agents.portfolio import PortfolioAgent
from agents.execution_agent import ExecutionAgent
from agents.performance_agent import PerformanceAgent


def test_data_agent():
    """Test DataAgent enhancements"""
    print("Testing DataAgent...")

    # Initialize DataAgent
    data_agent = DataAgent("../data")

    # Test getting current price
    btc_price = data_agent.get_price("BTC-USD")
    print(f"BTC-USD current price: {btc_price}")

    # Test getting historical data
    btc_history = data_agent.get_historical_data("BTC-USD", 5)
    print(f"BTC-USD historical data points: {len(btc_history)}")

    # Test available symbols
    symbols = data_agent.get_available_symbols()
    print(f"Available symbols: {symbols}")

    print("DataAgent test completed.\n")


def test_strategy_agent():
    """Test StrategyAgent enhancements"""
    print("Testing StrategyAgent...")

    # Test available strategies
    strategy_agent = StrategyAgent()
    strategies = strategy_agent.get_available_strategies()
    print(f"Available strategies: {strategies}")

    # Test MACD strategy
    macd_agent = StrategyAgent("BTC-USD", "macd")
    # Add some price data for testing
    for i in range(30):
        price_data = {"price": 30000 + i * 100}
        signal = macd_agent.generate_signal(price_data)
    print(f"MACD strategy signal: {signal}")

    # Test Bollinger Bands strategy
    bb_agent = StrategyAgent("ETH-USD", "bollinger_bands")
    # Add some price data for testing
    for i in range(30):
        price_data = {"price": 2000 + i * 10}
        signal = bb_agent.generate_signal(price_data)
    print(f"Bollinger Bands strategy signal: {signal}")

    print("StrategyAgent test completed.\n")


def test_risk_agent():
    """Test RiskAgent enhancements"""
    print("Testing RiskAgent...")

    # Initialize RiskAgent with drawdown and leverage limits
    risk_agent = RiskAgent(max_drawdown_limit=15.0, max_leverage=3.0)

    # Test risk assessment
    risk_result = risk_agent.assess_risk(
        position_size=1.0,
        account_balance=10000.0,
        entry_price=30000.0,
        symbol="BTC-USD",
    )
    print(f"Risk assessment result: {risk_result}")

    # Test risk report
    risk_report = risk_agent.get_risk_report()
    print(f"Risk report: {risk_report}")

    print("RiskAgent test completed.\n")


def test_portfolio_agent():
    """Test PortfolioAgent enhancements"""
    print("Testing PortfolioAgent...")

    # Initialize PortfolioAgent
    portfolio_agent = PortfolioAgent(50000.0)

    # Add a position
    result = portfolio_agent.add_position("BTC-USD", 0.5, 30000.0)
    print(f"Add position result: {result}")

    # Update position prices
    portfolio_agent.update_position_prices({"BTC-USD": 31000.0})

    # Get position details
    position = portfolio_agent.get_position("BTC-USD")
    print(f"Position details: {position}")

    # Get portfolio summary
    summary = portfolio_agent.get_portfolio_summary()
    print(f"Portfolio summary: {summary}")

    print("PortfolioAgent test completed.\n")


def test_execution_agent():
    """Test ExecutionAgent enhancements"""
    print("Testing ExecutionAgent...")

    # Initialize ExecutionAgent
    execution_agent = ExecutionAgent()

    # Execute a trade
    result = execution_agent.execute_trade("BTC-USD", "BUY", 0.1, 30000.0)
    print(f"Trade execution result: {result}")

    # Get order book
    order_book = execution_agent.get_order_book("BTC-USD")
    print(f"Order book: {order_book}")

    # Get trade logs
    trade_logs = execution_agent.get_trade_logs()
    print(f"Trade logs count: {len(trade_logs)}")

    print("ExecutionAgent test completed.\n")


def test_performance_agent():
    """Test PerformanceAgent"""
    print("Testing PerformanceAgent...")

    # Initialize PerformanceAgent
    perf_agent = PerformanceAgent(10000.0)

    # Simulate some trades
    from datetime import datetime

    trade_data = {
        "symbol": "BTC-USD",
        "action": "BUY",
        "size": 0.1,
        "price": 30000.0,
        "timestamp": datetime.utcnow(),
        "pnl": 500.0,
        "commission": 3.0,
    }

    perf_agent.update_metrics(trade_data)

    # Get performance summary
    summary = perf_agent.get_performance_summary()
    print(f"Performance summary: {summary}")

    print("PerformanceAgent test completed.\n")


def main():
    """Run all tests"""
    print("Running Stage 2 enhancements tests...\n")

    try:
        test_data_agent()
        test_strategy_agent()
        test_risk_agent()
        test_portfolio_agent()
        test_execution_agent()
        test_performance_agent()

        print("All tests completed successfully!")

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
