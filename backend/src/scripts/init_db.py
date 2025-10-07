"""
Database initialization script for QuantumTrade backend.
Sets up the database schema.
"""

from ..core.database import engine, Base
from ..models import user, trade, strategy, market_data, backtest


def init_db():
    """Initialize the database schema."""
    print("Initializing database schema...")

    # Create all tables
    Base.metadata.create_all(bind=engine)

    print("Database schema initialized successfully!")


if __name__ == "__main__":
    init_db()
