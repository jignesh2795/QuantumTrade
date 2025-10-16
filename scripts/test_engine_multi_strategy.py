"""
Test Script: Run one trading cycle for multiple strategies
Phase 5 Ready: Multi-strategy support
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.core.engine import TradingEngine
from backend.utils.settings import Settings
from backend.db.database import init_database
from backend.strategies.sma_crossover import SMACrossoverStrategy
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


async def test_multi_strategy():
    # Load settings
    settings = Settings()
    logger.info("🚀 Running multi-strategy single-cycle test for QuantumTrade Phase 5")
    
    # Initialize database
    await init_database()
    
    # Initialize exchange
    engine = TradingEngine(settings)
    await engine.exchange.connect()
    
    # Define multiple strategies (Phase 5-ready)
    strategies = [
        SMACrossoverStrategy(fast_period=10, slow_period=30, symbol=settings.DEFAULT_SYMBOL),
        SMACrossoverStrategy(fast_period=5, slow_period=20, symbol=settings.DEFAULT_SYMBOL),
        SMACrossoverStrategy(fast_period=15, slow_period=50, symbol=settings.DEFAULT_SYMBOL)
    ]
    
    # Run one cycle per strategy
    candles = await engine.exchange.get_candles(symbol=settings.DEFAULT_SYMBOL, timeframe=settings.TIMEFRAME, limit=100)
    current_price = await engine.exchange.get_current_price(settings.DEFAULT_SYMBOL)
    balance = await engine.exchange.get_balance()
    
    logger.info(f"💰 Balance: ${balance['cash']:.2f} | Total: ${balance['total']:.2f} | P&L: ${balance['pnl']:.2f}")
    
    for strategy in strategies:
        # Update position state (simplified: check if any positions exist)
        positions = await engine.exchange.get_positions()
        has_position = len(positions) > 0
        strategy.update_position_state(has_position)
        
        # Analyze strategy
        signal = strategy.analyze(candles)
        
        # Compute SMAs for logging
        closes = [c.close for c in candles]
        fast_sma = strategy.calculate_sma(closes, strategy.fast_period)
        slow_sma = strategy.calculate_sma(closes, strategy.slow_period)
        
        logger.info("-" * 60)
        logger.info(f"⚙️  Strategy: {strategy.name} | Fast SMA: {fast_sma:.2f}, Slow SMA: {slow_sma:.2f}")
        logger.info(f"🎯 Signal: {signal.action.upper()} | Confidence: {signal.confidence:.2%} | {signal.reason}")
        
        # Execute signal (paper trading only)
        if signal.action == "buy" and not has_position:
            await engine.execute_buy(settings.DEFAULT_SYMBOL, current_price, balance['cash'])
        elif signal.action == "sell" and has_position:
            await engine.execute_sell(settings.DEFAULT_SYMBOL, positions[0])
    
    # Print summary
    await engine.print_summary()
    
    # Disconnect
    await engine.exchange.disconnect()
    logger.info("✅ Multi-strategy single-cycle test completed.")


if __name__ == "__main__":
    asyncio.run(test_multi_strategy())
