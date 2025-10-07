"""
QuantumTrade Backtesting Script
Runs backtesting for trading strategies using historical data
"""

import os
import sys
import argparse
from datetime import datetime, timedelta

# Add backend src to path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "backend", "src")
)

from agents.strategy_agent import StrategyAgent
from core.market_data import MarketDataHandler


def run_backtest(symbol, strategy, days):
    """Run backtest for a specific symbol and strategy"""
    try:
        print(f"Running backtest for {symbol} using {strategy} strategy...")

        # Initialize components
        market_data_handler = MarketDataHandler()
        strategy_agent = StrategyAgent(symbol, strategy)

        # Get historical data
        historical_data = market_data_handler.get_historical_data(symbol, days)

        if not historical_data:
            print(f"No historical data available for {symbol}")
            return

        # Run backtest simulation
        signals = []
        for data_point in historical_data:
            price_data = {
                "symbol": symbol,
                "price": data_point["close"],
                "timestamp": data_point["date"],
            }
            signal = strategy_agent.generate_signal(price_data)
            signals.append(signal)

        # Print results
        buy_signals = [s for s in signals if s["action"] == "BUY"]
        sell_signals = [s for s in signals if s["action"] == "SELL"]
        hold_signals = [s for s in signals if s["action"] == "HOLD"]

        print(f"Backtest results for {symbol} ({strategy}):")
        print(f"  Total signals: {len(signals)}")
        print(f"  Buy signals: {len(buy_signals)}")
        print(f"  Sell signals: {len(sell_signals)}")
        print(f"  Hold signals: {len(hold_signals)}")

        print("Backtest completed successfully!")

    except Exception as e:
        print(f"Error running backtest: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="QuantumTrade Backtesting")
    parser.add_argument("--symbol", default="BTC-USD", help="Trading symbol")
    parser.add_argument("--strategy", default="moving_average", help="Trading strategy")
    parser.add_argument(
        "--days", type=int, default=30, help="Number of days to backtest"
    )

    args = parser.parse_args()
    run_backtest(args.symbol, args.strategy, args.days)


if __name__ == "__main__":
    main()
