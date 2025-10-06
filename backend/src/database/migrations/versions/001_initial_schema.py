"""
Initial database schema migration
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

Base = declarative_base()

class Portfolio(Base):
    __tablename__ = 'portfolio'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    quantity = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    trade_type = Column(String(4), nullable=False)  # BUY or SELL
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

def upgrade():
    """Apply the migration"""
    # This would contain the actual migration logic
    pass

def downgrade():
    """Revert the migration"""
    # This would contain the rollback logic
    pass