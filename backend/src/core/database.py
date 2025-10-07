"""
Database module for QuantumTrade backend.
Handles database connection setup for Supabase and PostgreSQL.
"""

import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from .config import Config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Database setup
if Config.DATABASE_URL:
    engine = create_engine(
        Config.DATABASE_URL,
        pool_size=Config.DB_POOL_SIZE,
        max_overflow=Config.DB_MAX_OVERFLOW,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False,  # Set to True for SQL debugging
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
else:
    engine = None
    SessionLocal = None
    Base = None


def get_db_session() -> Session:
    """
    Get a database session

    Returns:
        SQLAlchemy session
    """
    if SessionLocal:
        return SessionLocal()
    return None


@contextmanager
def get_db_context():
    """
    Context manager for database sessions

    Yields:
        SQLAlchemy session
    """
    if not SessionLocal:
        raise Exception("Database not configured")

    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()


def init_database():
    """
    Initialize database tables

    Creates all tables defined in models
    """
    if not engine:
        raise Exception("Database not configured")

    try:
        # Import all models to ensure they are registered
        from ..models import user, trade, strategy, market_data, backtest

        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

    except SQLAlchemyError as e:
        logger.error(f"Error initializing database: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error initializing database: {e}")
        raise


def drop_database():
    """
    Drop all database tables

    WARNING: This will delete all data
    """
    if not engine:
        raise Exception("Database not configured")

    try:
        # Import all models to ensure they are registered
        from ..models import user, trade, strategy, market_data, backtest

        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        logger.warning("All database tables dropped")

    except SQLAlchemyError as e:
        logger.error(f"Error dropping database: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error dropping database: {e}")
        raise


def get_database_status() -> dict:
    """
    Get database connection status

    Returns:
        Dictionary with database status information
    """
    if not engine:
        return {"status": "disconnected", "error": "Database not configured"}

    try:
        # Test connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()

        return {
            "status": "connected",
            "database_url": Config.DATABASE_URL.split("@")[-1],  # Hide credentials
            "engine": engine.name,
        }
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return {"status": "disconnected", "error": str(e)}


def health_check() -> bool:
    """
    Perform database health check

    Returns:
        True if database is healthy, False otherwise
    """
    if not engine:
        return False

    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


def get_db():
    """Dependency to get DB session."""
    if SessionLocal:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
