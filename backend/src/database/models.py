"""
Database Models for QuantumTrade Platform
Defines SQLAlchemy models for all database entities
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any

Base = declarative_base()


class Trade(Base):
    """Model representing a trade transaction"""

    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    action = Column(String(10), nullable=False)  # BUY, SELL
    size = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    strategy_id = Column(String(50), nullable=True)
    commission = Column(Float, default=0.0)
    slippage = Column(Float, default=0.0)
    status = Column(String(20), default="filled")  # filled, pending, cancelled
    notes = Column(Text, nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert trade to dictionary"""
        return {
            "id": self.id,
            "symbol": self.symbol,
            "action": self.action,
            "size": self.size,
            "price": self.price,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "strategy_id": self.strategy_id,
            "commission": self.commission,
            "slippage": self.slippage,
            "status": self.status,
            "notes": self.notes,
        }


class Position(Base):
    """Model representing a current position"""

    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True, unique=True)
    size = Column(Float, nullable=False)
    avg_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert position to dictionary"""
        return {
            "id": self.id,
            "symbol": self.symbol,
            "size": self.size,
            "avg_price": self.avg_price,
            "current_price": self.current_price,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class MarketData(Base):
    """Model representing historical market data"""

    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    interval = Column(String(10), default="1d")  # 1m, 5m, 15m, 1h, 1d, etc.

    def to_dict(self) -> Dict[str, Any]:
        """Convert market data to dictionary"""
        return {
            "id": self.id,
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "open_price": self.open_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "close_price": self.close_price,
            "volume": self.volume,
            "interval": self.interval,
        }


class StrategyResult(Base):
    """Model representing backtest strategy results"""

    __tablename__ = "strategy_results"

    id = Column(Integer, primary_key=True, index=True)
    strategy_name = Column(String(100), nullable=False)
    symbol = Column(String(20), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    initial_capital = Column(Float, nullable=False)
    final_capital = Column(Float, nullable=False)
    total_return = Column(Float, nullable=False)  # Percentage
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)  # Percentage
    win_rate = Column(Float, nullable=True)  # Percentage
    total_trades = Column(Integer, nullable=False)
    profitable_trades = Column(Integer, nullable=True)
    config = Column(Text, nullable=True)  # JSON configuration
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert strategy result to dictionary"""
        return {
            "id": self.id,
            "strategy_name": self.strategy_name,
            "symbol": self.symbol,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "initial_capital": self.initial_capital,
            "final_capital": self.final_capital,
            "total_return": self.total_return,
            "sharpe_ratio": self.sharpe_ratio,
            "max_drawdown": self.max_drawdown,
            "win_rate": self.win_rate,
            "total_trades": self.total_trades,
            "profitable_trades": self.profitable_trades,
            "config": self.config,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PerformanceMetric(Base):
    """Model representing performance metrics"""

    __tablename__ = "performance_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    context = Column(String(50), nullable=True)  # daily, weekly, monthly, etc.

    def to_dict(self) -> Dict[str, Any]:
        """Convert performance metric to dictionary"""
        return {
            "id": self.id,
            "metric_name": self.metric_name,
            "value": self.value,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "context": self.context,
        }


class BacktestResult(Base):
    """Model representing backtest execution results"""

    __tablename__ = "backtest_results"

    id = Column(Integer, primary_key=True, index=True)
    strategy = Column(String(100), nullable=False)
    symbol = Column(String(20), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    initial_capital = Column(Float, nullable=False)
    final_capital = Column(Float, nullable=False)
    total_return = Column(Float, nullable=False)
    max_drawdown = Column(Float, nullable=False)
    sharpe_ratio = Column(Float, nullable=False)
    win_rate = Column(Float, nullable=False)
    total_trades = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert backtest result to dictionary"""
        return {
            "id": self.id,
            "strategy": self.strategy,
            "symbol": self.symbol,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "initial_capital": self.initial_capital,
            "final_capital": self.final_capital,
            "total_return": self.total_return,
            "max_drawdown": self.max_drawdown,
            "sharpe_ratio": self.sharpe_ratio,
            "win_rate": self.win_rate,
            "total_trades": self.total_trades,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


# Additional models for user management and configuration
class User(Base):
    """Model representing a user"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Configuration(Base):
    """Model representing system configuration"""

    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "description": self.description,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
