"""
Database Connection for QuantumTrade Platform
Handles database connection setup and session management
"""

import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db_session() -> Session:
    """
    Get a database session

    Returns:
        SQLAlchemy session
    """
    return SessionLocal()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions

    Yields:
        SQLAlchemy session
    """
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
    try:
        # Import all models to ensure they are registered
        from . import models

        # Create all tables
        Base.metadata.create_all(bind=engine)

        # Create Supabase tables
        from .init_supabase_tables import create_supabase_tables

        create_supabase_tables()

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
    try:
        # Import all models to ensure they are registered
        from . import models

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
    try:
        # Test connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()

        return {
            "status": "connected",
            "database_url": DATABASE_URL.split("@")[-1],  # Hide credentials
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
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


# Dependency for FastAPI
def get_db():
    """
    FastAPI dependency for database sessions

    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
