"""
Backtest model for QuantumTrade backend.
Defines the backtest schema for storing backtest runs and results.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from ..core.database import Base


class Backtest(Base):
    """Backtest model for storing backtest runs and results."""

    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    symbol = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    strategy_name = Column(String, nullable=False)
    parameters = Column(JSON, nullable=True)
    initial_capital = Column(Float, nullable=False)
    final_portfolio_value = Column(Float, nullable=False)
    total_return = Column(Float, nullable=False)
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    win_rate = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"<Backtest(id={self.id}, name='{self.name}', symbol='{self.symbol}', total_return={self.total_return})>"
