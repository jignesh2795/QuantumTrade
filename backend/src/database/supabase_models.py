"""
Supabase Models for QuantumTrade Platform
Defines data models that match Supabase database schema
"""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class SupabaseModel:
    """Base class for Supabase models"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return self.__dict__.copy()


class User(SupabaseModel):
    """Model representing a user"""

    def __init__(
        self,
        id: Optional[str] = None,
        email: Optional[str] = None,
        password_hash: Optional[str] = None,
        created_at: Optional[datetime] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.id = id or str(uuid.uuid4())
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.utcnow()


class Trade(SupabaseModel):
    """Model representing a trade transaction"""

    def __init__(
        self,
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        asset: Optional[str] = None,
        trade_type: Optional[str] = None,  # BUY, SELL
        amount: Optional[float] = None,
        price: Optional[float] = None,
        timestamp: Optional[datetime] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.asset = asset
        self.trade_type = trade_type
        self.amount = amount
        self.price = price
        self.timestamp = timestamp or datetime.utcnow()


class Portfolio(SupabaseModel):
    """Model representing a portfolio position"""

    def __init__(
        self,
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        asset: Optional[str] = None,
        quantity: Optional[float] = None,
        avg_price: Optional[float] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.asset = asset
        self.quantity = quantity
        self.avg_price = avg_price


class StrategyExecution(SupabaseModel):
    """Model representing a strategy execution"""

    def __init__(
        self,
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        strategy_name: Optional[str] = None,
        asset: Optional[str] = None,
        signal: Optional[str] = None,  # BUY, SELL, HOLD
        confidence: Optional[float] = None,
        executed_at: Optional[datetime] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.strategy_name = strategy_name
        self.asset = asset
        self.signal = signal
        self.confidence = confidence
        self.executed_at = executed_at or datetime.utcnow()


class StrategyConfiguration(SupabaseModel):
    """Model representing a strategy configuration"""

    def __init__(
        self,
        id: Optional[str] = None,
        user_id: Optional[str] = None,
        strategy_name: Optional[str] = None,
        asset: Optional[str] = None,
        is_active: Optional[bool] = True,
        config: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.strategy_name = strategy_name
        self.asset = asset
        self.is_active = is_active
        self.config = config or {}
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
