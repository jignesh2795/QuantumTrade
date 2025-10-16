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
        
        # Use text-only format for Windows compatibility
        if os.name == 'nt':  # Windows
            logger.info("Starting QuantumTrade v0.1.0 (Phase 1)")
        else:
            logger.info("🚀 Starting QuantumTrade v0.1.0 (Phase 1)")
            
        logger.info(f"Mode: {settings.TRADING_MODE}")
        
        # Initialize database
        if os.name == 'nt':  # Windows
            logger.info("Initializing database...")
        else:
            logger.info("📊 Initializing database...")
            
        await init_database()
        
        # Create trading engine
        if os.name == 'nt':  # Windows
            logger.info("Starting trading engine...")
        else:
            logger.info("⚙️  Starting trading engine...")
            
        engine = TradingEngine(settings)
        
        # Start the engine
        await engine.start()
        
        # Keep running until interrupted
        if os.name == 'nt':  # Windows
            logger.info("QuantumTrade is running. Press Ctrl+C to stop.")
        else:
            logger.info("✅ QuantumTrade is running. Press Ctrl+C to stop.")
            
        await engine.run_forever()
        
    except KeyboardInterrupt:
        if os.name == 'nt':  # Windows
            logger.info("\nShutting down gracefully...")
        else:
            logger.info("\n👋 Shutting down gracefully...")
            
    except Exception as e:
        if os.name == 'nt':  # Windows
            logger.error(f"Fatal error: {e}", exc_info=True)
        else:
            logger.error(f"❌ Fatal error: {e}", exc_info=True)
            
        sys.exit(1)
    finally:
        if 'engine' in locals():
            await engine.shutdown()
        if os.name == 'nt':  # Windows
            logger.info("QuantumTrade stopped.")
        else:
            logger.info("✅ QuantumTrade stopped.")


if __name__ == "__main__":
    asyncio.run(main())