"""
Strategy model for QuantumTrade backend.
Defines the strategy schema for storing trading strategies.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    JSON,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.sql import func
from ..core.database import Base


class Strategy(Base):
    """Strategy model for storing trading strategies."""

    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    parameters = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return (
            f"<Strategy(id={self.id}, name='{self.name}', is_active={self.is_active})>"
        )
