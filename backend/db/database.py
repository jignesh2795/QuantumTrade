"""
Database initialization and session management
"""
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from backend.utils.settings import settings
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

# Create async engine
DATABASE_URL = settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# Create session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


async def init_database():
    """Initialize database and create tables"""
    try:
        async with engine.begin() as conn:
            # Import all models
            from backend.db.models import Trade, Position, Strategy, PerformanceMetric
            
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            if os.name == 'nt':  # Windows
                logger.info("Database initialized successfully")
            else:
                logger.info("✅ Database initialized successfully")
    except Exception as e:
        if os.name == 'nt':  # Windows
            logger.error(f"Failed to initialize database: {e}")
        else:
            logger.error(f"❌ Failed to initialize database: {e}")
        raise


async def get_session() -> AsyncSession:
    """Get database session"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def close_database():
    """Close database connections"""
    await engine.dispose()
    logger.info("Database connections closed")