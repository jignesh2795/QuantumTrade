"""
Test Script: Run one trading cycle of QuantumTrade Phase 1
"""
import asyncio
import sys
from pathlib import Path
import pytest

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.core.engine import TradingEngine
from backend.utils.settings import Settings
from backend.db.database import init_database
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


@pytest.mark.asyncio
async def test_one_cycle():
    """Test one trading cycle"""
    # Load settings
    settings = Settings()
    logger.info("🚀 Running single-cycle test for QuantumTrade Phase 1")
    logger.info(f"Mode: {settings.TRADING_MODE} | Symbol: {settings.DEFAULT_SYMBOL}")
    
    # Initialize database
    await init_database()
    
    # Create trading engine
    engine = TradingEngine(settings)
    
    # Connect to exchange
    await engine.exchange.connect()
    
    # Run one trading cycle
    await engine.trading_cycle()
    
    # Print summary
    await engine.print_summary()
    
    # Disconnect
    await engine.exchange.disconnect()
    logger.info("✅ Single-cycle test completed.")


if __name__ == "__main__":
    asyncio.run(test_one_cycle())