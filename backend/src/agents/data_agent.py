"""
Data Agent for QuantumTrade Platform
Collects & cleans market data from CSV files or exchange APIs
"""

import os
import csv
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class DataAgent:
    """
    Collects & cleans market data from CSV files or exchange APIs
    """

    def __init__(self, data_dir: str = "data"):
        """
        Initialize DataAgent

        Args:
            data_dir: Directory containing CSV data files
        """
        self.data_dir = data_dir
        self.historical_data = {}
        self.current_prices = {
            "BTC-USD": 30000,
            "ETH-USD": 2000,
            "SOL-USD": 25,
            "AAPL": 150,
            "GOOGL": 2500,
            "TSLA": 200,
        }
        self._load_historical_data()

    def _load_historical_data(self) -> None:
        """Load historical data from CSV files"""
        try:
            if not os.path.exists(self.data_dir):
                logger.warning(f"Data directory {self.data_dir} not found")
                return

            for filename in os.listdir(self.data_dir):
                if filename.endswith(".csv"):
                    symbol = filename.replace(".csv", "")
                    file_path = os.path.join(self.data_dir, filename)

                    with open(file_path, "r") as file:
                        reader = csv.DictReader(file)
                        self.historical_data[symbol] = list(reader)

                    logger.info(f"Loaded historical data for {symbol} from {filename}")

        except Exception as e:
            logger.error(f"Error loading historical data: {e}")

    def get_price(self, symbol: str) -> Dict:
        """
        Get current price for a symbol (simulated live data)

        Args:
            symbol: Trading symbol

        Returns:
            Dictionary with symbol and price
        """
        try:
            # Add some random volatility to simulate live data
            base_price = self.current_prices.get(symbol, 100.0)
            volatility = 0.005  # 0.5% volatility
            random_factor = 1 + random.uniform(-volatility, volatility)
            current_price = base_price * random_factor

            return {
                "symbol": symbol,
                "price": round(current_price, 2),
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            return {"symbol": symbol, "price": None}

    def get_historical_data(self, symbol: str, days: int = 30) -> List[Dict]:
        """
        Get historical data for a symbol

        Args:
            symbol: Trading symbol
            days: Number of days of historical data

        Returns:
            List of historical data points
        """
        try:
            # If we have CSV data, use it
            if symbol in self.historical_data:
                data = self.historical_data[symbol]
                # Return last N days
                return data[-days:] if len(data) > days else data

            # Generate simulated historical data if no CSV data
            base_price = self.current_prices.get(symbol, 100.0)
            historical_data = []

            for i in range(days, 0, -1):
                # Simulate price movement with some randomness
                days_ago = i
                time_decay = 1 + random.uniform(-0.02, 0.02) * (days_ago / days)
                price = base_price * time_decay

                # Add OHLC data
                open_price = price * (1 + random.uniform(-0.005, 0.005))
                high_price = price * (1 + random.uniform(0, 0.02))
                low_price = price * (1 - random.uniform(0, 0.02))
                close_price = price

                data_point = {
                    "date": (datetime.utcnow() - timedelta(days=days_ago)).isoformat(),
                    "open": round(open_price, 2),
                    "high": round(high_price, 2),
                    "low": round(low_price, 2),
                    "close": round(close_price, 2),
                    "volume": random.randint(10000, 100000),
                }

                historical_data.append(data_point)

            return historical_data

        except Exception as e:
            logger.error(f"Error getting historical data for {symbol}: {e}")
            return []

    def get_available_symbols(self) -> List[str]:
        """
        Get list of available symbols

        Returns:
            List of available symbols
        """
        try:
            # Return symbols from CSV files and hardcoded symbols
            csv_symbols = list(self.historical_data.keys())
            hardcoded_symbols = list(self.current_prices.keys())
            return list(set(csv_symbols + hardcoded_symbols))
        except Exception as e:
            logger.error(f"Error getting available symbols: {e}")
            return list(self.current_prices.keys())

    def update_live_prices(self) -> None:
        """Update live prices with new simulated values"""
        try:
            for symbol in self.current_prices:
                # Add some random movement to simulate live updates
                current = self.current_prices[symbol]
                change = random.uniform(-0.01, 0.01)  # ±1% change
                self.current_prices[symbol] = max(0.01, current * (1 + change))
        except Exception as e:
            logger.error(f"Error updating live prices: {e}")
