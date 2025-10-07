"""
Strategy Agent for QuantumTrade Platform
Generates buy/sell/hold signals based on various technical indicators and strategies
"""

import random
import logging
from typing import Dict, List, Optional
from datetime import datetime
import math

logger = logging.getLogger(__name__)


class StrategyAgent:
    """
    Generates buy/sell/hold signals based on various technical indicators and strategies
    """

    def __init__(self, symbol: str = "BTC-USD", strategy: str = "random"):
        self.symbol = symbol
        self.strategy = strategy
        self.price_history = []

    def generate_signal(self, price_data: Dict = None) -> Dict:
        """
        Generate trading signal based on selected strategy

        Args:
            price_data: Dictionary containing current price information

        Returns:
            Dictionary with signal information
        """
        try:
            # Update price history
            if price_data and "price" in price_data:
                self.price_history.append(
                    {
                        "price": price_data["price"],
                        "timestamp": datetime.utcnow(),
                        "open": price_data.get("open", price_data["price"]),
                        "high": price_data.get("high", price_data["price"]),
                        "low": price_data.get("low", price_data["price"]),
                        "close": price_data.get("close", price_data["price"]),
                        "volume": price_data.get("volume", 0),
                    }
                )

                # Keep only last 100 data points
                if len(self.price_history) > 100:
                    self.price_history = self.price_history[-100:]

            # Generate signal based on strategy
            if self.strategy == "random":
                signal = self._random_strategy()
            elif self.strategy == "moving_average":
                signal = self._moving_average_strategy()
            elif self.strategy == "rsi":
                signal = self._rsi_strategy()
            elif self.strategy == "breakout":
                signal = self._breakout_strategy()
            elif self.strategy == "mean_reversion":
                signal = self._mean_reversion_strategy()
            elif self.strategy == "macd":
                signal = self._macd_strategy()
            elif self.strategy == "bollinger_bands":
                signal = self._bollinger_bands_strategy()
            else:
                signal = self._random_strategy()

            return {
                "symbol": self.symbol,
                "strategy": self.strategy,
                "action": signal["action"],
                "size": signal.get("size", 1.0),
                "confidence": signal.get("confidence", 0.5),
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return {
                "symbol": self.symbol,
                "strategy": self.strategy,
                "action": "HOLD",
                "size": 0.0,
                "confidence": 0.0,
                "timestamp": datetime.utcnow().isoformat(),
            }

    def _random_strategy(self) -> Dict:
        """Random signal generation strategy"""
        action = random.choice(["BUY", "SELL", "HOLD"])
        size = random.uniform(0.1, 1.0)
        confidence = random.uniform(0.3, 0.8)

        return {"action": action, "size": size, "confidence": confidence}

    def _moving_average_strategy(self) -> Dict:
        """Moving average crossover strategy"""
        if len(self.price_history) < 20:
            return self._random_strategy()

        # Calculate simple moving averages
        prices = [p["price"] for p in self.price_history[-20:]]
        short_ma = sum(prices[-5:]) / 5  # 5-period MA
        long_ma = sum(prices) / 20  # 20-period MA

        # Generate signal based on MA crossover
        if short_ma > long_ma:
            action = "BUY"
            confidence = min(
                1.0, (short_ma - long_ma) / long_ma * 10
            )  # Scale confidence
        elif short_ma < long_ma:
            action = "SELL"
            confidence = min(1.0, (long_ma - short_ma) / long_ma * 10)
        else:
            action = "HOLD"
            confidence = 0.1

        size = min(1.0, confidence * 2)  # Size based on confidence

        return {"action": action, "size": size, "confidence": confidence}

    def _rsi_strategy(self) -> Dict:
        """Relative Strength Index strategy"""
        if len(self.price_history) < 15:
            return self._random_strategy()

        # Calculate RSI
        prices = [p["price"] for p in self.price_history[-15:]]
        rsi = self._calculate_rsi(prices)

        # Generate signal based on RSI
        if rsi < 30:  # Oversold
            action = "BUY"
            confidence = (30 - rsi) / 30
        elif rsi > 70:  # Overbought
            action = "SELL"
            confidence = (rsi - 70) / 30
        else:
            action = "HOLD"
            confidence = 0.1

        size = min(1.0, confidence)

        return {"action": action, "size": size, "confidence": confidence}

    def _calculate_rsi(self, prices: List[float]) -> float:
        """Calculate RSI from price list"""
        if len(prices) < 2:
            return 50.0

        # Calculate price changes
        deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]

        # Separate gains and losses
        gains = [max(0, delta) for delta in deltas]
        losses = [max(0, -delta) for delta in deltas]

        # Calculate average gains and losses
        avg_gain = sum(gains) / len(gains)
        avg_loss = sum(losses) / len(losses)

        if avg_loss == 0:
            return 100.0

        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def _breakout_strategy(self) -> Dict:
        """Breakout strategy based on price range"""
        if len(self.price_history) < 20:
            return self._random_strategy()

        # Calculate price range
        prices = [p["price"] for p in self.price_history[-20:]]
        min_price = min(prices)
        max_price = max(prices)
        current_price = prices[-1]
        range_size = max_price - min_price

        if range_size == 0:
            return self._random_strategy()

        # Check for breakout
        breakout_threshold = range_size * 0.05  # 5% of range

        if current_price > max_price - breakout_threshold:  # Breakout above resistance
            action = "BUY"
            confidence = min(
                1.0,
                (current_price - (max_price - breakout_threshold)) / breakout_threshold,
            )
        elif current_price < min_price + breakout_threshold:  # Breakdown below support
            action = "SELL"
            confidence = min(
                1.0,
                ((min_price + breakout_threshold) - current_price) / breakout_threshold,
            )
        else:
            action = "HOLD"
            confidence = 0.1

        size = min(1.0, confidence * 1.5)

        return {"action": action, "size": size, "confidence": confidence}

    def _mean_reversion_strategy(self) -> Dict:
        """Mean reversion strategy"""
        if len(self.price_history) < 20:
            return self._random_strategy()

        # Calculate mean and standard deviation
        prices = [p["price"] for p in self.price_history[-20:]]
        mean_price = sum(prices) / len(prices)
        std_dev = math.sqrt(sum((p - mean_price) ** 2 for p in prices) / len(prices))
        current_price = prices[-1]

        if std_dev == 0:
            return self._random_strategy()

        # Calculate z-score
        z_score = (current_price - mean_price) / std_dev

        # Generate signal based on z-score
        if z_score < -1:  # Price is below mean by more than 1 std dev
            action = "BUY"
            confidence = min(1.0, abs(z_score) / 3)  # Cap at 3 std devs
        elif z_score > 1:  # Price is above mean by more than 1 std dev
            action = "SELL"
            confidence = min(1.0, abs(z_score) / 3)
        else:
            action = "HOLD"
            confidence = 0.1

        size = min(1.0, confidence)

        return {"action": action, "size": size, "confidence": confidence}

    def _macd_strategy(self) -> Dict:
        """MACD strategy"""
        if len(self.price_history) < 26:
            return self._random_strategy()

        prices = [p["price"] for p in self.price_history[-26:]]

        # Calculate MACD line (12-day EMA - 26-day EMA)
        ema_12 = self._calculate_ema(prices[-12:], 12)
        ema_26 = self._calculate_ema(prices, 26)
        macd_line = ema_12 - ema_26

        # Calculate signal line (9-day EMA of MACD line)
        # For simplicity, we'll use a simple moving average as approximation
        macd_history = []
        for i in range(9, len(prices)):
            hist_ema_12 = self._calculate_ema(prices[i - 11 : i + 1], 12)
            hist_ema_26 = self._calculate_ema(prices[i - 25 : i + 1], 26)
            macd_history.append(hist_ema_12 - hist_ema_26)

        signal_line = sum(macd_history[-9:]) / 9 if len(macd_history) >= 9 else 0

        # Generate signal based on MACD crossover
        if macd_line > signal_line:
            action = "BUY"
            confidence = min(1.0, abs(macd_line - signal_line) * 10)
        elif macd_line < signal_line:
            action = "SELL"
            confidence = min(1.0, abs(macd_line - signal_line) * 10)
        else:
            action = "HOLD"
            confidence = 0.1

        size = min(1.0, confidence)

        return {"action": action, "size": size, "confidence": confidence}

    def _calculate_ema(self, prices: List[float], period: int) -> float:
        """Calculate Exponential Moving Average"""
        if len(prices) == 0:
            return 0.0

        if len(prices) < period:
            return sum(prices) / len(prices)

        # Simple calculation for EMA
        multiplier = 2 / (period + 1)
        ema = prices[0]

        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))

        return ema

    def _bollinger_bands_strategy(self) -> Dict:
        """Bollinger Bands strategy"""
        if len(self.price_history) < 20:
            return self._random_strategy()

        prices = [p["price"] for p in self.price_history[-20:]]

        # Calculate middle band (20-period SMA)
        middle_band = sum(prices) / len(prices)

        # Calculate standard deviation
        std_dev = math.sqrt(sum((p - middle_band) ** 2 for p in prices) / len(prices))

        # Calculate upper and lower bands
        upper_band = middle_band + (2 * std_dev)
        lower_band = middle_band - (2 * std_dev)

        current_price = prices[-1]

        # Generate signal based on price position relative to bands
        if current_price < lower_band:  # Price below lower band
            action = "BUY"
            confidence = min(1.0, (lower_band - current_price) / lower_band * 10)
        elif current_price > upper_band:  # Price above upper band
            action = "SELL"
            confidence = min(1.0, (current_price - upper_band) / upper_band * 10)
        else:
            action = "HOLD"
            confidence = 0.1

        size = min(1.0, confidence)

        return {"action": action, "size": size, "confidence": confidence}

    def set_strategy(self, strategy: str) -> None:
        """Change the active strategy"""
        self.strategy = strategy
        logger.info(f"Strategy changed to: {strategy}")

    def get_available_strategies(self) -> List[str]:
        """Get list of available strategies"""
        return [
            "random",
            "moving_average",
            "rsi",
            "breakout",
            "mean_reversion",
            "macd",
            "bollinger_bands",
        ]
