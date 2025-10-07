#!/usr/bin/env python3
"""
Simplified Mock Data Loader for QuantumTrade
"""

import os
import sys
import random
import csv

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))


def generate_mock_trades(count=1000):
    """Generate mock trade data"""
    symbols = ["AAPL", "TSLA", "BTC", "ETH", "GOOGL", "AMZN", "MSFT", "NFLX"]
    trades = []

    for i in range(count):
        trade = {
            "symbol": random.choice(symbols),
            "price": round(random.uniform(50, 500), 2),
            "volume": random.randint(1, 1000),
            "trade_type": random.choice(["BUY", "SELL"]),
        }
        trades.append(trade)

    return trades


def save_mock_data_to_csv(trades, filename="data/mock_trades.csv"):
    """Save mock data to CSV file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["symbol", "price", "volume", "trade_type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for trade in trades:
            writer.writerow(trade)

    print(f"✅ Saved {len(trades)} mock trades to {filename}")


def main():
    """Main function"""
    print("📊 Generating mock data...")
    trades = generate_mock_trades(5000)
    save_mock_data_to_csv(trades)
    print("🎉 Mock data generation complete!")


if __name__ == "__main__":
    main()
