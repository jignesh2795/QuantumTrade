"""
QuantumTrade - Main Entry Point
Phase 1: Minimal Viable Trader
"""
import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.core.engine import TradingEngine
from backend.utils.settings import Settings
from backend.utils.logger import setup_logger
from backend.db.database import init_database

logger = setup_logger(__name__)


async def main():
    """Initialize and run the trading engine"""
    try:
        # Load settings
        settings = Settings()
        
        # Force emoji output for demonstration (normally we'd check os.name)
        logger.info("🚀 Starting QuantumTrade v0.1.0 (Phase 1)")
        logger.info(f"Mode: {settings.TRADING_MODE}")
        
        # Initialize database
        logger.info("📊 Initializing database...")
            
        await init_database()
        
        # Create trading engine
        logger.info("⚙️  Starting trading engine...")
            
        engine = TradingEngine(settings)
        
        # Start the engine
        await engine.start()
        
        # Keep running until interrupted
        logger.info("✅ QuantumTrade is running. Press Ctrl+C to stop.")
            
        await engine.run_forever()
        
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down gracefully...")
            
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
            
        sys.exit(1)
    finally:
        if 'engine' in locals():
            await engine.shutdown()
        logger.info("✅ QuantumTrade stopped.")


if __name__ == "__main__":
    asyncio.run(main())