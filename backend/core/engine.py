"""
Core Trading Engine
"""
import asyncio
import os
from datetime import datetime
from typing import Optional
from backend.core.paper_exchange import PaperExchange
from backend.strategies.sma_crossover import SMACrossoverStrategy
from backend.utils.settings import Settings
from backend.utils.logger import setup_logger, TradingLogger

logger = setup_logger(__name__)
trade_logger = TradingLogger()


class TradingEngine:
    """
    Core trading engine that orchestrates:
    - Exchange connections
    - Strategy execution
    - Order management
    - Position tracking
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.is_running = False
        
        # Initialize exchange
        if settings.TRADING_MODE == "paper":
            self.exchange = PaperExchange(initial_capital=settings.INITIAL_CAPITAL)
        else:
            # TODO: Initialize real exchange in Phase 2
            raise NotImplementedError("Live trading not yet implemented")
        
        # Initialize strategy
        self.strategy = SMACrossoverStrategy(
            fast_period=settings.SMA_FAST_PERIOD,
            slow_period=settings.SMA_SLOW_PERIOD,
            symbol=settings.DEFAULT_SYMBOL
        )
        
        # Tracking
        self.current_position = None
        self.trade_count = 0
        
    async def start(self):
        """Start the trading engine"""
        if os.name == 'nt':  # Windows
            logger.info("=" * 60)
            logger.info("QUANTUMTRADE TRADING ENGINE")
            logger.info("=" * 60)
        else:
            logger.info("=" * 60)
            logger.info("🚀 QUANTUMTRADE TRADING ENGINE")
            logger.info("=" * 60)
            
        logger.info(f"Mode: {self.settings.TRADING_MODE.upper()}")
        logger.info(f"Symbol: {self.settings.DEFAULT_SYMBOL}")
        logger.info(f"Strategy: {self.strategy.name}")
        logger.info(f"Capital: ${self.settings.INITIAL_CAPITAL:,.2f}")
        logger.info("=" * 60)
        
        # Connect to exchange
        if os.name == 'nt':  # Windows
            logger.info("Connecting to Paper Trading Exchange")
        else:
            logger.info("📝 Connecting to Paper Trading Exchange")
            
        await self.exchange.connect()
        if os.name == 'nt':  # Windows
            logger.info(f"Paper exchange connected | Initial capital: ${self.settings.INITIAL_CAPITAL:,.2f}")
        else:
            logger.info(f"✅ Paper exchange connected | Initial capital: ${self.settings.INITIAL_CAPITAL:,.2f}")
            
        self.is_running = True
        
    async def shutdown(self):
        """Shutdown the trading engine"""
        logger.info("Shutting down trading engine...")
        self.is_running = False
        await self.exchange.disconnect()
        
        # Print final statistics
        await self.print_summary()
        
    async def run_forever(self):
        """Main trading loop"""
        check_interval = 60  # Check every 60 seconds
        
        while self.is_running:
            try:
                await self.trading_cycle()
                await asyncio.sleep(check_interval)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error in trading cycle: {e}", exc_info=True)
                await asyncio.sleep(check_interval)
    
    async def trading_cycle(self):
        """Execute one trading cycle"""
        symbol = self.settings.DEFAULT_SYMBOL
        
        # Get market data
        candles = await self.exchange.get_candles(
            symbol=symbol,
            timeframe=self.settings.TIMEFRAME,
            limit=100
        )
        
        # Get current price
        current_price = await self.exchange.get_current_price(symbol)
        
        # Get account balance
        balance = await self.exchange.get_balance()
        
        # Get positions
        positions = await self.exchange.get_positions()
        has_position = len(positions) > 0
        
        # Update strategy position state
        self.strategy.update_position_state(has_position)
        
        # Get trading signal
        signal = self.strategy.analyze(candles)
        
        # Log current status
        logger.info("-" * 60)
        if os.name == 'nt':  # Windows
            logger.info(f"Market Update | {symbol} @ ${current_price:.2f}")
        else:
            logger.info(f"📊 Market Update | {symbol} @ ${current_price:.2f}")
            
        if os.name == 'nt':  # Windows
            logger.info(f"Balance: ${balance['cash']:.2f} | Total: ${balance['total']:.2f} | P&L: ${balance['pnl']:.2f} ({balance['pnl_pct']:.2f}%)")
        else:
            logger.info(f"💰 Balance: ${balance['cash']:.2f} | Total: ${balance['total']:.2f} | P&L: ${balance['pnl']:.2f} ({balance['pnl_pct']:.2f}%)")
        
        if positions:
            for pos in positions:
                logger.info(
                    f"Position: {pos['quantity']:.6f} {pos['symbol']} @ ${pos['avg_price']:.2f} | "
                    f"Current: ${pos['current_price']:.2f} | P&L: ${pos['pnl']:.2f} ({pos['pnl_pct']:.2f}%)"
                )
        
        if os.name == 'nt':  # Windows
            logger.info(f"Signal: {signal.action.upper()} | Confidence: {signal.confidence:.2%} | {signal.reason}")
        else:
            logger.info(f"🎯 Signal: {signal.action.upper()} | Confidence: {signal.confidence:.2%} | {signal.reason}")
        
        # Execute signal
        if signal.action == "buy" and not has_position:
            await self.execute_buy(symbol, current_price, balance['cash'])
        elif signal.action == "sell" and has_position:
            await self.execute_sell(symbol, positions[0])
    
    async def execute_buy(self, symbol: str, price: float, cash: float):
        """Execute buy order"""
        # Calculate position size (using max position size limit)
        max_position_value = cash * self.settings.MAX_POSITION_SIZE
        quantity = max_position_value / price
        
        # Round to reasonable precision
        quantity = round(quantity, 6)
        
        if os.name == 'nt':  # Windows
            logger.info(f"Executing BUY order | {quantity} {symbol} @ ${price:.2f}")
        else:
            logger.info(f"🔵 Executing BUY order | {quantity} {symbol} @ ${price:.2f}")
        
        # Place order
        result = await self.exchange.place_order(
            symbol=symbol,
            side="buy",
            quantity=quantity,
            price=price,
            order_type="market"
        )
        
        if result.status == "filled":
            self.trade_count += 1
            trade_logger.log_trade({
                "order_id": result.order_id,
                "side": "buy",
                "symbol": symbol,
                "quantity": quantity,
                "price": price,
                "strategy": self.strategy.name
            })
            if os.name == 'nt':  # Windows
                logger.info(f"BUY order filled | Order ID: {result.order_id}")
            else:
                logger.info(f"✅ BUY order filled | Order ID: {result.order_id}")
        else:
            if os.name == 'nt':  # Windows
                logger.warning(f"BUY order {result.status} | Order ID: {result.order_id}")
            else:
                logger.warning(f"⚠️  BUY order {result.status} | Order ID: {result.order_id}")
    
    async def execute_sell(self, symbol: str, position: dict):
        """Execute sell order"""
        quantity = position['quantity']
        price = position['current_price']
        
        if os.name == 'nt':  # Windows
            logger.info(f"Executing SELL order | {quantity} {symbol} @ ${price:.2f}")
        else:
            logger.info(f"🔴 Executing SELL order | {quantity} {symbol} @ ${price:.2f}")
        
        # Place order
        result = await self.exchange.place_order(
            symbol=symbol,
            side="sell",
            quantity=quantity,
            price=price,
            order_type="market"
        )
        
        if result.status == "filled":
            self.trade_count += 1
            trade_logger.log_trade({
                "order_id": result.order_id,
                "side": "sell",
                "symbol": symbol,
                "quantity": quantity,
                "price": price,
                "strategy": self.strategy.name
            })
            if os.name == 'nt':  # Windows
                logger.info(f"SELL order filled | Order ID: {result.order_id}")
            else:
                logger.info(f"✅ SELL order filled | Order ID: {result.order_id}")
        else:
            if os.name == 'nt':  # Windows
                logger.warning(f"SELL order {result.status} | Order ID: {result.order_id}")
            else:
                logger.warning(f"⚠️  SELL order {result.status} | Order ID: {result.order_id}")
    
    async def print_summary(self):
        """Print trading summary"""
        balance = await self.exchange.get_balance()
        
        logger.info("=" * 60)
        if os.name == 'nt':  # Windows
            logger.info("TRADING SUMMARY")
        else:
            logger.info("📈 TRADING SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Initial Capital: ${self.settings.INITIAL_CAPITAL:,.2f}")
        logger.info(f"Final Balance: ${balance['total']:,.2f}")
        logger.info(f"Total P&L: ${balance['pnl']:,.2f} ({balance['pnl_pct']:.2f}%)")
        logger.info(f"Total Trades: {self.trade_count}")
        logger.info(f"Trade History: {len(self.exchange.trade_history)} orders")
        logger.info("=" * 60)