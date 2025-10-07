"""
Supabase Client for QuantumTrade Platform
Handles Supabase database connection and operations
"""

import os
import logging

logger = logging.getLogger(__name__)

# For local development with PostgreSQL, we'll use direct database access
# instead of the Supabase client since we're not using a full Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL", "http://localhost:54321")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "local-dev-key")

# We'll use the existing database connection instead of Supabase client
# Import the existing database connection
from .connection import get_db_session, engine
from sqlalchemy import text


def get_supabase_client():
    """
    Get the database session for CRUD operations
    For local development, we're using direct PostgreSQL access
    instead of Supabase client
    """
    return get_db_session()


def test_supabase_connection() -> bool:
    """
    Test database connection

    Returns:
        True if connection is successful, False otherwise
    """
    try:
        # Use the existing database connection
        db = get_db_session()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False


def initialize_supabase_tables():
    """
    Initialize database tables if they don't exist
    """
    try:
        logger.info("Initializing database tables...")
        # Import all models to ensure they are registered
        from . import models

        # Create all tables using the existing engine
        from .models import Base

        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized")
    except Exception as e:
        logger.error(f"Error initializing database tables: {e}")
        raise


if __name__ == "__main__":
    # Test the database connection
    if test_supabase_connection():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")
