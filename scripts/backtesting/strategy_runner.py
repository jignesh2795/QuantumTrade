"""
QuantumTrade Strategy Runner
Executes backtests for multiple strategies sequentially
"""

import os
import sys
from datetime import datetime, timedelta

# Add backend src to path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "backend", "src")
)

from agents.strategy_agent import StrategyAgent
from core.market_data import MarketDataHandler


def run_strategy_backtests(symbol, days=30):
    """Run backtests for all available strategies"""
    try:
        print(f"Running strategy backtests for {symbol}...")

        # Initialize components
        market_data_handler = MarketDataHandler()
        strategies = ["moving_average", "rsi", "macd", "bollinger_bands"]

        # Get historical data
        historical_data = market_data_handler.get_historical_data(symbol, days)

        if not historical_data:
            print(f"No historical data available for {symbol}")
            return

        results = {}

        # Run backtest for each strategy
        for strategy_name in strategies:
            print(f"\nTesting {strategy_name} strategy...")
            strategy_agent = StrategyAgent(symbol, strategy_name)

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

            # Calculate statistics
            buy_signals = [s for s in signals if s["action"] == "BUY"]
            sell_signals = [s for s in signals if s["action"] == "SELL"]

            results[strategy_name] = {
                "total_signals": len(signals),
                "buy_signals": len(buy_signals),
                "sell_signals": len(sell_signals),
                "win_rate": len(buy_signals) / len(signals) if signals else 0,
            }

            print(f"  Buy signals: {len(buy_signals)}")
            print(f"  Sell signals: {len(sell_signals)}")
            print(f"  Win rate: {results[strategy_name]['win_rate']:.2%}")

        # Print summary
        print("\n" + "=" * 50)
        print("STRATEGY BACKTEST SUMMARY")
        print("=" * 50)
        for strategy, stats in results.items():
            print(
                f"{strategy:20} | Signals: {stats['total_signals']:3} | Buy: {stats['buy_signals']:3} | Sell: {stats['sell_signals']:3} | Win Rate: {stats['win_rate']:.2%}"
            )

        print("Strategy backtests completed successfully!")

    except Exception as e:
        print(f"Error running strategy backtests: {e}")
        sys.exit(1)


if __name__ == "__main__":
    symbol = "BTC-USD"
    if len(sys.argv) > 1:
        symbol = sys.argv[1]

    run_strategy_backtests(symbol)
