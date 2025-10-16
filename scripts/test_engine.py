#!/usr/bin/env python3
"""
Test script for the Trading Engine
This script demonstrates basic functionality of the trading engine.
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.core.engine import TradingEngine
from backend.utils.settings import Settings
from backend.utils.logger import setup_logger

# Set up logger
logger = setup_logger("test_engine")


async def test_engine_basic():
    """Test basic engine functionality"""
    logger.info("Starting Trading Engine Test")
    
    try:
        # Load settings
        settings = Settings()
        logger.info(f"Loaded settings: Mode={settings.TRADING_MODE}, Symbol={settings.DEFAULT_SYMBOL}")
        
        # Create trading engine
        logger.info("Creating trading engine...")
        engine = TradingEngine(settings)
        
        # Test engine initialization
        logger.info("Testing engine initialization...")
        assert engine.settings == settings
        assert engine.is_running == False
        assert engine.trade_count == 0
        logger.info("✓ Engine initialization test passed")
        
        # Test engine start
        logger.info("Testing engine start...")
        await engine.start()
        assert engine.is_running == True
        logger.info("✓ Engine start test passed")
        
        # Test one trading cycle
        logger.info("Testing trading cycle...")
        await engine.trading_cycle()
        logger.info("✓ Trading cycle test passed")
        
        # Test shutdown
        logger.info("Testing engine shutdown...")
        await engine.shutdown()
        assert engine.is_running == False
        logger.info("✓ Engine shutdown test passed")
        
        logger.info("All tests passed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        return False


async def test_engine_with_mock_data():
    """Test engine with mock market data"""
    logger.info("Starting Mock Data Test")
    
    try:
        # Load settings
        settings = Settings()
        
        # Create trading engine
        engine = TradingEngine(settings)
        await engine.start()
        
        # Run a few trading cycles
        logger.info("Running 3 trading cycles...")
        for i in range(3):
            logger.info(f"Cycle {i+1}/3")
            await engine.trading_cycle()
            await asyncio.sleep(1)  # Small delay between cycles
            
        # Shutdown
        await engine.shutdown()
        
        logger.info("Mock data test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Mock data test failed with error: {e}")
        return False


def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("QUANTUMTRADE ENGINE TEST SCRIPT")
    logger.info("=" * 60)
    
    # Run basic tests
    logger.info("Running basic engine tests...")
    success1 = asyncio.run(test_engine_basic())
    
    if success1:
        logger.info("Running mock data tests...")
        success2 = asyncio.run(test_engine_with_mock_data())
        
        if success2:
            logger.info("=" * 60)
            logger.info("ALL TESTS COMPLETED SUCCESSFULLY!")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Mock data tests failed!")
            return 1
    else:
        logger.error("Basic tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())