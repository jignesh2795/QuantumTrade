"""
Simplified Database Module for QuantumTrade Platform
"""

import os
import asyncpg
import logging

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@db:5432/quantumtrade"
)


async def init_db():
    """
    Initialize database tables

    Creates required tables if they don't exist
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (
                id SERIAL PRIMARY KEY,
                symbol TEXT,
                price FLOAT,
                volume INT,
                trade_type TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS portfolio (
                id SERIAL PRIMARY KEY,
                symbol TEXT,
                quantity FLOAT,
                avg_price FLOAT,
                current_price FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        await conn.close()
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def get_db_connection():
    """
    Get database connection

    Returns:
        Database connection object
    """
    return await asyncpg.connect(DATABASE_URL)
