"""
Database Initialization Script for Supabase Tables
Creates the tables needed for Supabase CRUD operations
"""

import logging
from sqlalchemy import text
from .connection import engine

logger = logging.getLogger(__name__)


def create_supabase_tables():
    """Create tables needed for Supabase CRUD operations"""

    # SQL to create the required tables
    create_tables_sql = """
    -- Create trades table for Supabase CRUD
    CREATE TABLE IF NOT EXISTS trades (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        asset TEXT NOT NULL,
        trade_type TEXT NOT NULL,
        amount FLOAT NOT NULL,
        price FLOAT NOT NULL,
        timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
    );

    -- Create portfolio table for Supabase CRUD
    CREATE TABLE IF NOT EXISTS portfolio (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        asset TEXT NOT NULL,
        quantity FLOAT NOT NULL,
        avg_price FLOAT NOT NULL
    );

    -- Create strategy_executions table for Supabase CRUD
    CREATE TABLE IF NOT EXISTS strategy_executions (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        strategy_name TEXT NOT NULL,
        asset TEXT NOT NULL,
        signal TEXT NOT NULL,
        confidence FLOAT NOT NULL,
        executed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
    );

    -- Create strategy_configurations table for Supabase CRUD
    CREATE TABLE IF NOT EXISTS strategy_configurations (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        strategy_name TEXT NOT NULL,
        asset TEXT NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        config JSONB,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
        updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
    );

    -- Create users table for Supabase CRUD
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
    );

    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_trades_user_id ON trades(user_id);
    CREATE INDEX IF NOT EXISTS idx_trades_asset ON trades(asset);
    CREATE INDEX IF NOT EXISTS idx_trades_timestamp ON trades(timestamp);
    
    CREATE INDEX IF NOT EXISTS idx_portfolio_user_id ON portfolio(user_id);
    CREATE INDEX IF NOT EXISTS idx_portfolio_asset ON portfolio(asset);
    
    CREATE INDEX IF NOT EXISTS idx_strategy_executions_user_id ON strategy_executions(user_id);
    CREATE INDEX IF NOT EXISTS idx_strategy_executions_strategy_name ON strategy_executions(strategy_name);
    CREATE INDEX IF NOT EXISTS idx_strategy_executions_asset ON strategy_executions(asset);
    
    CREATE INDEX IF NOT EXISTS idx_strategy_configurations_user_id ON strategy_configurations(user_id);
    CREATE INDEX IF NOT EXISTS idx_strategy_configurations_strategy_name ON strategy_configurations(strategy_name);
    CREATE INDEX IF NOT EXISTS idx_strategy_configurations_asset ON strategy_configurations(asset);
    
    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    """

    try:
        # Execute the SQL to create tables
        with engine.connect() as connection:
            connection.execute(text(create_tables_sql))
            connection.commit()
        logger.info("Supabase tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating Supabase tables: {e}")
        return False


if __name__ == "__main__":
    create_supabase_tables()
