"""
Market data model for QuantumTrade backend.
Defines the market data schema for storing candle/ticker data.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.sql import func
from ..core.database import Base


class MarketData(Base):
    """Market data model for storing candle/ticker data."""

    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Composite index for symbol and timestamp for faster queries
    __table_args__ = (Index("ix_symbol_timestamp", "symbol", "timestamp"),)

    def __repr__(self):
        return f"<MarketData(id={self.id}, symbol='{self.symbol}', timestamp='{self.timestamp}')>"
