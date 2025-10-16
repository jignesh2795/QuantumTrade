"""
Core Trading Engine - Updated for Phase 2
"""
import asyncio
import os
from datetime import datetime
from typing import Optional
from backend.core.paper_exchange import PaperExchange
from backend.core.binance_exchange import BinanceExchange
from backend.core.risk_manager import RiskManager
from backend.strategies.sma_crossover import SMACrossoverStrategy
from backend.utils.settings import Settings
from backend.utils.logger import setup_logger, TradingLogger
from backend.utils.notifications import NotificationManager

logger = setup_logger(__name__)
trade_logger = TradingLogger()


class TradingEngine:
    """
    Core trading engine that orchestrates:
    - Exchange connections
    - Strategy execution
    - Order management
    - Position tracking
    - Risk management (Phase 2)
    - Notifications (Phase 2)
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.is_running = False
        
        # Initialize exchange
        if settings.TRADING_MODE == "paper":
            self.exchange = PaperExchange(initial_capital=settings.INITIAL_CAPITAL)
            logger.info("📝 Paper trading mode selected")
        else:
            # Live trading with Binance
            if settings.EXCHANGE.lower() == "binance":
                self.exchange = BinanceExchange(
                    api_key=settings.API_KEY,
                    api_secret=settings.API_SECRET,
                    testnet=settings.USE_TESTNET
                )
                mode = "Testnet" if settings.USE_TESTNET else "LIVE"
                logger.info(f"🔴 Live trading mode selected - Binance {mode}")
            else:
                raise ValueError(f"Unsupported exchange: {settings.EXCHANGE}")
        
        # Initialize risk manager (Phase 2)
        self.risk_manager = RiskManager(
            initial_capital=settings.INITIAL_CAPITAL,
            max_position_size=settings.MAX_POSITION_SIZE,
            max_daily_loss=settings.MAX_DAILY_LOSS,
            max_drawdown=settings.MAX_DRAWDOWN,
            stop_loss_pct=settings.STOP_LOSS_PCT,
            take_profit_pct=settings.TAKE_PROFIT_PCT
        )
        
        # Initialize notification manager (Phase 2)
        self.notifier = NotificationManager(
            email_enabled=settings.EMAIL_ENABLED,
            smtp_server=settings.SMTP_SERVER,
            smtp_port=settings.SMTP_PORT,
            smtp_username=settings.SMTP_USERNAME,
            smtp_password=settings.SMTP_PASSWORD,
            from_email=settings.FROM_EMAIL,
            to_email=settings.TO_EMAIL
        )
        
        # Initialize strategy
        self.strategy = SMACrossoverStrategy(
            fast_period=settings.SMA_FAST_PERIOD,
            slow_period=settings.SMA_SLOW_PERIOD,
            symbol=settings.DEFAULT_SYMBOL
        )
        
        # Tracking
        self.current_position = None
        self.trade_count = 0
        self.positions_with_stops = {}  # Track stop-loss/take-profit levels
        
    async def start(self):
        """Start the trading engine"""
        if os.name == 'nt':  # Windows
            logger.info("=" * 60)
            logger.info("QUANTUMTRADE TRADING ENGINE - PHASE 2")
            logger.info("=" * 60)
        else:
            logger.info("=" * 60)
            logger.info("🚀 QUANTUMTRADE TRADING ENGINE - PHASE 2")
            logger.info("=" * 60)
            
        logger.info(f"Mode: {self.settings.TRADING_MODE.upper()}")
        logger.info(f"Exchange: {self.settings.EXCHANGE}")
        
        if self.settings.TRADING_MODE == "live":
            mode = "Testnet" if self.settings.USE_TESTNET else "LIVE"
            if os.name == 'nt':  # Windows
                logger.warning(f"⚠️  LIVE TRADING ENABLED - {mode}")
            else:
                logger.warning(f"⚠️  LIVE TRADING ENABLED - {mode}")
        
        logger.info(f"Symbol: {self.settings.DEFAULT_SYMBOL}")
        logger.info(f"Strategy: {self.strategy.name}")
        logger.info(f"Capital: ${self.settings.INITIAL_CAPITAL:,.2f}")
        if os.name == 'nt':  # Windows
            logger.info(f"Risk Management: ON 🛡️")
        else:
            logger.info(f"Risk Management: ON 🛡️")
        logger.info("=" * 60)
        
        # Validate settings
        self.settings.validate()
        
        # Connect to exchange
        await self.exchange.connect()
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
        
        # Check risk limits (Phase 2)
        can_trade, risk_reason = self.risk_manager.can_trade(balance['total'] if self.settings.TRADING_MODE == "paper" else balance.get('cash', 0))
        
        if not can_trade:
            logger.warning(f"🚨 Trading halted: {risk_reason}")
            try:
                await self.notifier.send_risk_alert("Trading Halted", risk_reason)
            except Exception as e:
                logger.warning(f"Failed to send risk alert: {e}")
            
            # Close all positions if circuit breaker triggered
            if self.risk_manager.circuit_breaker_triggered and has_position:
                logger.warning("⚠️  Circuit breaker active - closing all positions")
                for pos in positions:
                    await self.execute_sell(pos['symbol'], pos, force=True)
            
            return
        
        # Check stop-loss and take-profit for existing positions (Phase 2)
        if has_position:
            await self.check_position_exits(positions, current_price)
        
        # Update strategy position state
        self.strategy.update_position_state(has_position)
        
        # Get trading signal
        signal = self.strategy.analyze(candles)
        
        # Get risk report
        risk_report = self.risk_manager.get_risk_report()
        
        # Log current status
        logger.info("-" * 60)
        if os.name == 'nt':  # Windows
            logger.info(f"Market Update | {symbol} @ ${current_price:.2f}")
        else:
            logger.info(f"📊 Market Update | {symbol} @ ${current_price:.2f}")
            
        if self.settings.TRADING_MODE == "paper":
            if os.name == 'nt':  # Windows
                logger.info(f"Balance: ${balance['cash']:.2f} | Total: ${balance['total']:.2f} | P&L: ${balance['pnl']:.2f} ({balance['pnl_pct']:.2f}%)")
            else:
                logger.info(f"💰 Balance: ${balance['cash']:.2f} | Total: ${balance['total']:.2f} | P&L: ${balance['pnl']:.2f} ({balance['pnl_pct']:.2f}%)")
        else:
            # For live trading, show available balance
            available_balance = balance.get('cash', 0) if isinstance(balance, dict) else 0
            if os.name == 'nt':  # Windows
                logger.info(f"Balance: ${available_balance:.2f}")
            else:
                logger.info(f"💰 Balance: ${available_balance:.2f}")
        
        if os.name == 'nt':  # Windows
            logger.info(f"Risk: Daily P&L: {risk_report['daily_pnl_pct']:.2f}% | Drawdown: {risk_report['current_drawdown_pct']:.2f}% | Circuit Breaker: {'🔴 ACTIVE' if risk_report['circuit_breaker_active'] else '🟢 OK'}")
        else:
            logger.info(f"🛡️  Risk: Daily P&L: {risk_report['daily_pnl_pct']:.2f}% | Drawdown: {risk_report['current_drawdown_pct']:.2f}% | Circuit Breaker: {'🔴 ACTIVE' if risk_report['circuit_breaker_active'] else '🟢 OK'}")
        
        if positions:
            for pos in positions:
                # Get stop-loss and take-profit for this position
                stops = self.positions_with_stops.get(pos['symbol'], {})
                sl = stops.get('stop_loss', 'N/A')
                tp = stops.get('take_profit', 'N/A')
                
                if os.name == 'nt':  # Windows
                    logger.info(f"Position: {pos['quantity']:.6f} {pos['symbol']} @ ${pos['avg_price']:.2f} | Current: ${pos['current_price']:.2f} | P&L: ${pos['pnl']:.2f} ({pos['pnl_pct']:.2f}%) | SL: {sl if sl == 'N/A' else f'${sl:.2f}'} | TP: {tp if tp == 'N/A' else f'${tp:.2f}'}")
                else:
                    logger.info(f"📍 Position: {pos['quantity']:.6f} {pos['symbol']} @ ${pos['avg_price']:.2f} | Current: ${pos['current_price']:.2f} | P&L: ${pos['pnl']:.2f} ({pos['pnl_pct']:.2f}%) | SL: {sl if sl == 'N/A' else f'${sl:.2f}'} | TP: {tp if tp == 'N/A' else f'${tp:.2f}'}")
        
        if os.name == 'nt':  # Windows
            logger.info(f"Signal: {signal.action.upper()} | Confidence: {signal.confidence:.2%} | {signal.reason}")
        else:
            logger.info(f"🎯 Signal: {signal.action.upper()} | Confidence: {signal.confidence:.2%} | {signal.reason}")
        
        # Execute signal
        if signal.action == "buy" and not has_position and can_trade:
            await self.execute_buy(symbol, current_price, balance.get('cash', available_balance))
        elif signal.action == "sell" and has_position:
            await self.execute_sell(symbol, positions[0])
    
    async def check_position_exits(self, positions, current_price):
        """Check if any positions should be closed due to stop-loss or take-profit"""
        for pos in positions:
            symbol = pos['symbol']
            stops = self.positions_with_stops.get(symbol, {})
            
            if not stops:
                continue
            
            stop_loss = stops.get('stop_loss')
            take_profit = stops.get('take_profit')
            entry_price = stops.get('entry_price', pos.get('avg_price', current_price))
            
            # Check if we should close
            should_close, reason = self.risk_manager.should_close_position(
                entry_price=entry_price,
                current_price=current_price,
                side="buy",  # Assuming long positions
                stop_loss=stop_loss,
                take_profit=take_profit
            )
            
            if should_close:
                logger.warning(f"🚨 Position exit triggered: {reason}")
                await self.execute_sell(symbol, pos, force=True, reason=reason)
    
    async def execute_buy(self, symbol: str, price: float, cash: float):
        """Execute buy order with risk management"""
        # Calculate position size with risk management
        quantity = self.risk_manager.calculate_position_size(
            available_capital=cash,
            current_price=price,
            volatility=0.02  # TODO: Calculate actual volatility
        )
        
        # Round to reasonable precision
        quantity = round(quantity, 6)
        
        # Calculate stop-loss and take-profit
        stop_loss = self.risk_manager.calculate_stop_loss(price, "buy")
        take_profit = self.risk_manager.calculate_take_profit(price, "buy")
        
        if os.name == 'nt':  # Windows
            logger.info(f"Executing BUY order | {quantity} {symbol} @ ${price:.2f} | SL: ${stop_loss:.2f} | TP: ${take_profit:.2f}")
        else:
            logger.info(f"🔵 Executing BUY order | {quantity} {symbol} @ ${price:.2f} | SL: ${stop_loss:.2f} | TP: ${take_profit:.2f}")
        
        # Dry run check
        if self.settings.DRY_RUN:
            if os.name == 'nt':  # Windows
                logger.info("DRY RUN MODE - Order not sent to exchange")
            else:
                logger.info("🔸 DRY RUN MODE - Order not sent to exchange")
            return
        
        # Place order
        try:
            result = await self.exchange.place_order(
                symbol=symbol,
                side="buy",
                quantity=quantity,
                price=price,
                order_type="market"
            )
            
            if result.status == "filled":
                self.trade_count += 1
                
                # Store stop-loss and take-profit levels
                self.positions_with_stops[symbol] = {
                    'entry_price': price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'quantity': quantity
                }
                
                # Log trade
                trade_data = {
                    "order_id": result.order_id,
                    "side": "buy",
                    "symbol": symbol,
                    "quantity": quantity,
                    "price": price,
                    "strategy": self.strategy.name,
                    "stop_loss": stop_loss,
                    "take_profit": take_profit
                }
                
                trade_logger.log_trade(trade_data)
                if os.name == 'nt':  # Windows
                    logger.info(f"BUY order filled | Order ID: {result.order_id}")
                else:
                    logger.info(f"✅ BUY order filled | Order ID: {result.order_id}")
                
                # Send notification
                try:
                    await self.notifier.send_trade_alert(trade_data)
                except Exception as e:
                    logger.warning(f"Failed to send trade alert: {e}")
            else:
                if os.name == 'nt':  # Windows
                    logger.warning(f"BUY order {result.status} | Order ID: {result.order_id}")
                else:
                    logger.warning(f"⚠️  BUY order {result.status} | Order ID: {result.order_id}")
        
        except Exception as e:
            logger.error(f"❌ Failed to execute BUY order: {e}")
            try:
                await self.notifier.send_risk_alert("Order Execution Failed", str(e))
            except Exception as e2:
                logger.warning(f"Failed to send risk alert: {e2}")
    
    async def execute_sell(self, symbol: str, position: dict, force: bool = False, reason: str = "Signal"):
        """Execute sell order"""
        quantity = position['quantity']
        price = position['current_price']
        
        if os.name == 'nt':  # Windows
            logger.info(f"Executing SELL order | {quantity} {symbol} @ ${price:.2f} | Reason: {reason}")
        else:
            logger.info(f"🔴 Executing SELL order | {quantity} {symbol} @ ${price:.2f} | Reason: {reason}")
        
        # Dry run check
        if self.settings.DRY_RUN and not force:
            if os.name == 'nt':  # Windows
                logger.info("DRY RUN MODE - Order not sent to exchange")
            else:
                logger.info("🔸 DRY RUN MODE - Order not sent to exchange")
            return
        
        # Place order
        try:
            result = await self.exchange.place_order(
                symbol=symbol,
                side="sell",
                quantity=quantity,
                price=price,
                order_type="market"
            )
            
            if result.status == "filled":
                self.trade_count += 1
                
                # Remove from positions tracking
                if symbol in self.positions_with_stops:
                    del self.positions_with_stops[symbol]
                
                # Log trade
                trade_data = {
                    "order_id": result.order_id,
                    "side": "sell",
                    "symbol": symbol,
                    "quantity": quantity,
                    "price": price,
                    "strategy": self.strategy.name,
                    "reason": reason
                }
                
                trade_logger.log_trade(trade_data)
                if os.name == 'nt':  # Windows
                    logger.info(f"SELL order filled | Order ID: {result.order_id}")
                else:
                    logger.info(f"✅ SELL order filled | Order ID: {result.order_id}")
                
                # Send notification
                try:
                    await self.notifier.send_trade_alert(trade_data)
                except Exception as e:
                    logger.warning(f"Failed to send trade alert: {e}")
            else:
                if os.name == 'nt':  # Windows
                    logger.warning(f"SELL order {result.status} | Order ID: {result.order_id}")
                else:
                    logger.warning(f"⚠️  SELL order {result.status} | Order ID: {result.order_id}")
        
        except Exception as e:
            logger.error(f"❌ Failed to execute SELL order: {e}")
            try:
                await self.notifier.send_risk_alert("Order Execution Failed", str(e))
            except Exception as e2:
                logger.warning(f"Failed to send risk alert: {e2}")
    
    async def print_summary(self):
        """Print trading summary"""
        balance = await self.exchange.get_balance()
        risk_report = self.risk_manager.get_risk_report()
        
        if os.name == 'nt':  # Windows
            logger.info("=" * 60)
            logger.info("TRADING SUMMARY - PHASE 2")
            logger.info("=" * 60)
        else:
            logger.info("=" * 60)
            logger.info("📈 TRADING SUMMARY - PHASE 2")
            logger.info("=" * 60)
            
        logger.info(f"Initial Capital: ${self.settings.INITIAL_CAPITAL:,.2f}")
        if self.settings.TRADING_MODE == "paper":
            logger.info(f"Final Balance: ${balance['total']:,.2f}")
            logger.info(f"Total P&L: ${balance['pnl']:,.2f} ({balance['pnl_pct']:.2f}%)")
        else:
            # For live trading, show available balance
            available_balance = balance.get('cash', 0) if isinstance(balance, dict) else 0
            logger.info(f"Available Balance: ${available_balance:,.2f}")
        logger.info(f"Total Trades: {self.trade_count}")
        logger.info("-" * 60)
        if os.name == 'nt':  # Windows
            logger.info("Risk Metrics:")
            logger.info(f"  Daily P&L: {risk_report['daily_pnl_pct']:.2f}%")
            logger.info(f"  Max Drawdown: {risk_report['current_drawdown_pct']:.2f}%")
            logger.info(f"  Peak Capital: ${risk_report['peak_capital']:,.2f}")
            logger.info(f"  Circuit Breaker: {'🔴 TRIGGERED' if risk_report['circuit_breaker_active'] else '🟢 Never Triggered'}")
        else:
            logger.info("Risk Metrics:")
            logger.info(f"  Daily P&L: {risk_report['daily_pnl_pct']:.2f}%")
            logger.info(f"  Max Drawdown: {risk_report['current_drawdown_pct']:.2f}%")
            logger.info(f"  Peak Capital: ${risk_report['peak_capital']:,.2f}")
            logger.info(f"  Circuit Breaker: {'🔴 TRIGGERED' if risk_report['circuit_breaker_active'] else '🟢 Never Triggered'}")
        logger.info("=" * 60)
        
        # Send daily summary
        if self.settings.EMAIL_ENABLED:
            try:
                summary_data = {
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'total_pnl': balance['pnl'] if self.settings.TRADING_MODE == "paper" else 0,
                    'pnl_pct': balance['pnl_pct'] if self.settings.TRADING_MODE == "paper" else 0,
                    'trades_count': self.trade_count,
                    'win_rate': 0.0,  # TODO: Calculate
                    'current_balance': balance['total'] if self.settings.TRADING_MODE == "paper" else available_balance,
                    'open_positions': len(await self.exchange.get_positions()),
                    'daily_drawdown': risk_report['current_drawdown_pct'],
                    'circuit_breaker': risk_report['circuit_breaker_active']
                }
                await self.notifier.send_daily_summary(summary_data)
            except Exception as e:
                logger.warning(f"Failed to send daily summary: {e}")