"""
SQLAlchemy database models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.db.database import Base
import enum


class TradeSide(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"


class TradeStatus(str, enum.Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class Trade(Base):
    """Trade execution records"""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    symbol = Column(String, index=True)
    side = Column(Enum(TradeSide))
    quantity = Column(Float)
    price = Column(Float)
    filled_quantity = Column(Float, default=0)
    avg_fill_price = Column(Float, nullable=True)
    status = Column(Enum(TradeStatus), default=TradeStatus.PENDING)
    
    # Strategy info
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    strategy = relationship("Strategy", back_populates="trades")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)
    
    # P&L
    pnl = Column(Float, default=0.0)
    fees = Column(Float, default=0.0)
    
    # Trading mode
    is_paper = Column(Boolean, default=True)
    
    # Additional metadata
    notes = Column(Text, nullable=True)


class Position(Base):
    """Current open positions"""
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    quantity = Column(Float)
    avg_entry_price = Column(Float)
    current_price = Column(Float)
    unrealized_pnl = Column(Float, default=0.0)
    
    # Strategy
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    strategy = relationship("Strategy", back_populates="positions")
    
    # Timestamps
    opened_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Risk management
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)


class Strategy(Base):
    """Strategy configurations"""
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)  # sma_crossover, rsi_mean_reversion, etc.
    
    # Status
    is_active = Column(Boolean, default=False)
    is_paper = Column(Boolean, default=True)
    
    # Configuration (JSON stored as text)
    config = Column(Text)
    
    # Performance
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    total_pnl = Column(Float, default=0.0)
    
    # Relationships
    trades = relationship("Trade", back_populates="strategy")
    positions = relationship("Position", back_populates="strategy")
    metrics = relationship("PerformanceMetric", back_populates="strategy")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PerformanceMetric(Base):
    """Performance metrics tracking"""
    __tablename__ = "performance_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    strategy = relationship("Strategy", back_populates="metrics")
    
    # Metrics
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    portfolio_value = Column(Float)
    cash_balance = Column(Float)
    total_pnl = Column(Float)
    daily_pnl = Column(Float)
    
    # Risk metrics
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    win_rate = Column(Float, nullable=True)
    
    # Trade stats
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)