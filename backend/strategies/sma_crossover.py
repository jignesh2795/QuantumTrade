"""
Simple Moving Average Crossover Strategy
"""
import os
from typing import Dict, Optional, List
from dataclasses import dataclass
import pandas as pd
from backend.core.exchange_base import Candle
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class Signal:
    """Trading signal"""
    action: str  # buy, sell, hold
    symbol: str
    confidence: float  # 0.0 to 1.0
    price: float
    reason: str
    timestamp: str


class SMACrossoverStrategy:
    """
    Simple Moving Average Crossover Strategy
    
    Rules:
    - BUY when fast SMA crosses above slow SMA
    - SELL when fast SMA crosses below slow SMA
    """
    
    def __init__(
        self,
        fast_period: int = 10,
        slow_period: int = 30,
        symbol: str = "BTCUSDT"
    ):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.symbol = symbol
        self.name = f"SMA_{fast_period}_{slow_period}"
        
        # State tracking
        self.last_signal = None
        self.position_open = False
        
        # Force emoji output for demonstration (normally we'd check os.name)
        logger.info(
            f"📊 SMA Crossover Strategy initialized | "
            f"Fast: {fast_period}, Slow: {slow_period}, Symbol: {symbol}"
        )
    
    def calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period
    
    def analyze(self, candles: List[Candle]) -> Signal:
        """
        Analyze candles and generate trading signal
        
        Args:
            candles: List of OHLCV candles
            
        Returns:
            Signal object with action recommendation
        """
        if len(candles) < self.slow_period:
            return Signal(
                action="hold",
                symbol=self.symbol,
                confidence=0.0,
                price=candles[-1].close if candles else 0.0,
                reason="Insufficient data",
                timestamp=candles[-1].timestamp.isoformat() if candles else ""
            )
        
        # Extract close prices
        closes = [c.close for c in candles]
        current_price = closes[-1]
        
        # Calculate SMAs
        fast_sma = self.calculate_sma(closes, self.fast_period)
        slow_sma = self.calculate_sma(closes, self.slow_period)
        
        # Previous SMAs for crossover detection
        prev_fast_sma = self.calculate_sma(closes[:-1], self.fast_period)
        prev_slow_sma = self.calculate_sma(closes[:-1], self.slow_period)
        
        if not all([fast_sma, slow_sma, prev_fast_sma, prev_slow_sma]):
            return Signal(
                action="hold",
                symbol=self.symbol,
                confidence=0.0,
                price=current_price,
                reason="Calculating indicators",
                timestamp=candles[-1].timestamp.isoformat()
            )
        
        # Detect crossovers
        bullish_cross = prev_fast_sma <= prev_slow_sma and fast_sma > slow_sma
        bearish_cross = prev_fast_sma >= prev_slow_sma and fast_sma < slow_sma
        
        # Calculate confidence based on SMA distance
        sma_distance = abs(fast_sma - slow_sma) / slow_sma
        confidence = min(sma_distance * 100, 1.0)  # Cap at 1.0
        
        # Generate signal
        if bullish_cross and not self.position_open:
            signal = Signal(
                action="buy",
                symbol=self.symbol,
                confidence=confidence,
                price=current_price,
                reason=f"Bullish crossover: Fast SMA ({fast_sma:.2f}) > Slow SMA ({slow_sma:.2f})",
                timestamp=candles[-1].timestamp.isoformat()
            )
            self.last_signal = "buy"
            logger.info(f"🟢 BUY Signal | {signal.reason} | Confidence: {confidence:.2%}")
            
        elif bearish_cross and self.position_open:
            signal = Signal(
                action="sell",
                symbol=self.symbol,
                confidence=confidence,
                price=current_price,
                reason=f"Bearish crossover: Fast SMA ({fast_sma:.2f}) < Slow SMA ({slow_sma:.2f})",
                timestamp=candles[-1].timestamp.isoformat()
            )
            self.last_signal = "sell"
            logger.info(f"🔴 SELL Signal | {signal.reason} | Confidence: {confidence:.2%}")
            
        else:
            signal = Signal(
                action="hold",
                symbol=self.symbol,
                confidence=0.0,
                price=current_price,
                reason=f"No crossover. Fast: {fast_sma:.2f}, Slow: {slow_sma:.2f}",
                timestamp=candles[-1].timestamp.isoformat()
            )
        
        return signal
    
    def update_position_state(self, is_open: bool):
        """Update position state"""
        self.position_open = is_open