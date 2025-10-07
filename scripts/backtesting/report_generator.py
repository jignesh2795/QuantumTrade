"""
QuantumTrade Backtest Report Generator
Generates performance reports and visualizations for backtest results
"""

import os
import sys
import json
from datetime import datetime

# Add backend src to path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "backend", "src")
)

from agents.performance_agent import PerformanceAgent


def generate_backtest_report(symbol, strategy, results):
    """Generate backtest performance report"""
    try:
        print(f"Generating backtest report for {symbol} using {strategy} strategy...")

        # Initialize performance agent
        perf_agent = PerformanceAgent()

        # Generate report
        report = {
            "symbol": symbol,
            "strategy": strategy,
            "timestamp": datetime.utcnow().isoformat(),
            "results": results,
            "performance_metrics": perf_agent.get_performance_summary(),
        }

        # Save report to file
        report_filename = f"backtest_report_{symbol}_{strategy}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, "w") as f:
            json.dump(report, f, indent=2)

        print(f"Backtest report saved to {report_filename}")
        print("Backtest report generated successfully!")

        return report

    except Exception as e:
        print(f"Error generating backtest report: {e}")
        sys.exit(1)


def main():
    # Example usage
    symbol = "BTC-USD"
    strategy = "moving_average"
    results = {
        "total_trades": 100,
        "winning_trades": 60,
        "losing_trades": 40,
        "win_rate": 0.6,
        "total_pnl": 1500.0,
        "max_drawdown": -0.15,
        "sharpe_ratio": 1.5,
    }

    generate_backtest_report(symbol, strategy, results)


if __name__ == "__main__":
    main()
