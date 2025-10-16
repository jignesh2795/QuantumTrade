"""
Core Trading Engine - Updated for Phase 3 (AI Agents)
"""
import asyncio
import os
from datetime import datetime
from typing import Optional, List
from backend.core.paper_exchange import PaperExchange
from backend.core.binance_exchange import BinanceExchange
from backend.core.risk_manager import RiskManager
from backend.strategies.sma_crossover import SMACrossoverStrategy
from backend.utils.settings import Settings
from backend.utils.logger import setup_logger, TradingLogger
from backend.utils.notifications import NotificationManager

# Phase 3: Import AI Agents
from backend.ai_agents.agentx_executor import AgentXExecutor
from backend.ai_agents.optima_optimizer import OptimaOptimizer
from backend.ai_agents.hivemind_coordinator import HiveMindCoordinator
from backend.ai_agents.ml_signal_generator import MLSignalGenerator
from backend.ai_agents.base_agent import Signal

logger = setup_logger(__name__)
trade_logger = TradingLogger()


class TradingEngine:
    """
    Core trading engine - Phase 3 with AI Agents
    
    Features:
    - Exchange connections
    - Strategy execution
    - Risk management
    - AI agent coordination
    - ML signal generation
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.is_running = False
        
        # Initialize exchange
        if settings.TRADING_MODE == "paper":
            self.exchange = PaperExchange(initial_capital=settings.INITIAL_CAPITAL)
            logger.info("📝 Paper trading mode selected")
        else:
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
        
        # Initialize risk manager
        self.risk_manager = RiskManager(
            initial_capital=settings.INITIAL_CAPITAL,
            max_position_size=settings.MAX_POSITION_SIZE,
            max_daily_loss=settings.MAX_DAILY_LOSS,
            max_drawdown=settings.MAX_DRAWDOWN,
            stop_loss_pct=settings.STOP_LOSS_PCT,
            take_profit_pct=settings.TAKE_PROFIT_PCT
        )
        
        # Initialize notification manager
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
        
        # Phase 3: Initialize AI Agents
        self.agentx = AgentXExecutor()
        self.optima = OptimaOptimizer()
        self.hivemind = HiveMindCoordinator()
        self.ml_signal = MLSignalGenerator()
        
        # Agent ensemble
        self.agents = {
            "AgentX": self.agentx,
            "Optima": self.optima,
            "HiveMind": self.hivemind,
            "MLSignal": self.ml_signal
        }
        
        # Tracking
        self.current_position = None
        self.trade_count = 0
        self.positions_with_stops = {}
        
    async def start(self):
        """Start the trading engine"""
        if os.name == 'nt':  # Windows
            logger.info("=" * 60)
            logger.info("QUANTUMTRADE TRADING ENGINE - PHASE 3")
            logger.info("=" * 60)
        else:
            logger.info("=" * 60)
            logger.info("🚀 QUANTUMTRADE TRADING ENGINE - PHASE 3")
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
        logger.info(f"AI Agents: {len(self.agents)} active 🤖")
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
        """Execute one trading cycle with AI agents"""
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
        
        # Check risk limits
        can_trade, risk_reason = self.risk_manager.can_trade(balance['total'])
        
        if not can_trade:
            logger.warning(f"🚨 Trading halted: {risk_reason}")
            try:
                await self.notifier.send_risk_alert("Trading Halted", risk_reason)
            except Exception as e:
                logger.warning(f"Failed to send risk alert: {e}")
            
            if self.risk_manager.circuit_breaker_triggered and has_position:
                logger.warning("⚠️  Circuit breaker active - closing all positions")
                for pos in positions:
                    await self.execute_sell(pos['symbol'], pos, force=True)
            
            return
        
        # Check position exits
        if has_position:
            await self.check_position_exits(positions, current_price)
        
        # Update strategy position state
        self.strategy.update_position_state(has_position)
        
        # Phase 3: Collect signals from all agents
        signals = await self.collect_agent_signals(candles, balance, positions, current_price)
        
        # Phase 3: Let HiveMind make final decision
        decision = await self.hivemind.analyze({"signals": signals})
        
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
        
        # Log agent signals
        logger.info(f"🤖 Agent Signals ({len(signals)}):")
        for signal in signals:
            logger.info(f"   {signal.agent_name}: {signal.action.upper()} @ {signal.confidence:.2%}")
        
        # Log HiveMind decision
        logger.info(
            f"🧠 HiveMind Decision: {decision['decision'].upper()} | "
            f"Confidence: {decision['confidence']:.2%} | "
            f"Consensus: {decision.get('consensus', 0):.2%}"
        )
        
        if positions:
            for pos in positions:
                stops = self.positions_with_stops.get(pos['symbol'], {})
                sl = stops.get('stop_loss', 'N/A')
                tp = stops.get('take_profit', 'N/A')
                
                if os.name == 'nt':  # Windows
                    logger.info(f"Position: {pos['quantity']:.6f} {pos['symbol']} @ ${pos['avg_price']:.2f} | Current: ${pos['current_price']:.2f} | P&L: ${pos['pnl']:.2f} ({pos['pnl_pct']:.2f}%) | SL: {sl if sl == 'N/A' else f'${sl:.2f}'} | TP: {tp if tp == 'N/A' else f'${tp:.2f}'}")
                else:
                    logger.info(f"📍 Position: {pos['quantity']:.6f} {pos['symbol']} @ ${pos['avg_price']:.2f} | Current: ${pos['current_price']:.2f} | P&L: ${pos['pnl']:.2f} ({pos['pnl_pct']:.2f}%) | SL: {sl if sl == 'N/A' else f'${sl:.2f}'} | TP: {tp if tp == 'N/A' else f'${tp:.2f}'}")
        
        # Execute HiveMind decision
        if decision['decision'] == "buy" and not has_position and can_trade:
            await self.execute_buy(symbol, current_price, balance['cash'])
        elif decision['decision'] == "sell" and has_position:
            await self.execute_sell(symbol, positions[0])
    
    async def collect_agent_signals(
        self, 
        candles, 
        balance, 
        positions, 
        current_price
    ) -> List[Signal]:
        """Collect signals from all AI agents"""
        signals = []
        
        # 1. Strategy signal
        strategy_signal = self.strategy.analyze(candles)
        signals.append(Signal(
            agent_name="Strategy",
            action=strategy_signal.action,
            confidence=strategy_signal.confidence,
            reason=strategy_signal.reason
        ))
        
        # 2. ML Signal
        ml_result = await self.ml_signal.analyze({"candles": candles})
        signals.append(Signal(
            agent_name="MLSignal",
            action=ml_result['action'],
            confidence=ml_result['confidence'],
            reason=ml_result['reason']
        ))
        
        # 3. Guard (Risk) signal
        guard_signal = self._get_guard_signal(balance, positions)
        if guard_signal:
            signals.append(guard_signal)
        
        # 4. Optima suggestions (if any)
        optima_result = await self.optima.analyze({
            "performance": {
                "win_rate": 0.5,  # TODO: Calculate actual
                "total_pnl": balance['pnl']
            },
            "parameters": {
                "sma_fast_period": self.settings.SMA_FAST_PERIOD,
                "sma_slow_period": self.settings.SMA_SLOW_PERIOD,
                "position_size": self.settings.MAX_POSITION_SIZE
            }
        })
        
        if optima_result.get('needs_optimization'):
            logger.info(f"💡 Optima: {len(optima_result['suggestions'])} optimization suggestions")
        
        return signals
    
    def _get_guard_signal(self, balance, positions) -> Optional[Signal]:
        """Get signal from Guard (risk management)"""
        can_trade, reason = self.risk_manager.can_trade(balance['total'])
        
        if not can_trade:
            return Signal(
                agent_name="Guard",
                action="sell" if positions else "hold",
                confidence=1.0,
                reason=f"Risk limit: {reason}"
            )
        
        # Check if positions need closing
        if positions:
            for pos in positions:
                stops = self.positions_with_stops.get(pos['symbol'], {})
                if stops:
                    should_close, close_reason = self.risk_manager.should_close_position(
                        entry_price=stops.get('entry_price', pos['avg_price']),
                        current_price=pos['current_price'],
                        side="buy",
                        stop_loss=stops.get('stop_loss'),
                        take_profit=stops.get('take_profit')
                    )
                    
                    if should_close:
                        return Signal(
                            agent_name="Guard",
                            action="sell",
                            confidence=1.0,
                            reason=close_reason
                        )
        
        return None
    
    async def check_position_exits(self, positions, current_price):
        """Check if any positions should be closed"""
        for pos in positions:
            symbol = pos['symbol']
            stops = self.positions_with_stops.get(symbol, {})
            
            if not stops:
                continue
            
            stop_loss = stops.get('stop_loss')
            take_profit = stops.get('take_profit')
            entry_price = stops.get('entry_price', pos['avg_price'])
            
            should_close, reason = self.risk_manager.should_close_position(
                entry_price=entry_price,
                current_price=current_price,
                side="buy",
                stop_loss=stop_loss,
                take_profit=take_profit
            )
            
            if should_close:
                logger.warning(f"🚨 Position exit triggered: {reason}")
                await self.execute_sell(symbol, pos, force=True, reason=reason)
    
    async def execute_buy(self, symbol: str, price: float, cash: float):
        """Execute buy order with AI optimization"""
        # Get execution plan from AgentX
        execution_plan = await self.agentx.analyze({
            "symbol": symbol,
            "side": "buy",
            "current_price": price,
            "order_type": "market",
            "quantity": 0,  # Will be calculated
            "avg_volume": 1000,  # TODO: Get actual
            "volatility": 0.02,  # TODO: Calculate actual
            "spread": 0.001
        })
        
        # Calculate position size with risk management
        quantity = self.risk_manager.calculate_position_size(
            available_capital=cash,
            current_price=price,
            volatility=0.02
        )
        
        quantity = round(quantity, 6)
        
        # Calculate stop-loss and take-profit
        stop_loss = self.risk_manager.calculate_stop_loss(price, "buy")
        take_profit = self.risk_manager.calculate_take_profit(price, "buy")
        
        if os.name == 'nt':  # Windows
            logger.info(f"Executing BUY order | {quantity} {symbol} @ ${price:.2f} | SL: ${stop_loss:.2f} | TP: ${take_profit:.2f} | Strategy: {execution_plan['execution_strategy']}")
        else:
            logger.info(f"🔵 Executing BUY order | {quantity} {symbol} @ ${price:.2f} | SL: ${stop_loss:.2f} | TP: ${take_profit:.2f} | Strategy: {execution_plan['execution_strategy']}")
        
        if self.settings.DRY_RUN:
            if os.name == 'nt':  # Windows
                logger.info("DRY RUN MODE - Order not sent to exchange")
            else:
                logger.info("🔸 DRY RUN MODE - Order not sent to exchange")
            return
        
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
                
                # Store position tracking
                self.positions_with_stops[symbol] = {
                    'entry_price': price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'quantity': quantity
                }
                
                # Record execution with AgentX
                self.agentx.record_execution({
                    "order_id": result.order_id,
                    "filled": True,
                    "actual_slippage": 0.0  # TODO: Calculate actual
                })
                
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
        
        if self.settings.DRY_RUN and not force:
            if os.name == 'nt':  # Windows
                logger.info("DRY RUN MODE - Order not sent to exchange")
            else:
                logger.info("🔸 DRY RUN MODE - Order not sent to exchange")
            return
        
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
                
                # Remove from tracking
                if symbol in self.positions_with_stops:
                    del self.positions_with_stops[symbol]
                
                # Record execution
                self.agentx.record_execution({
                    "order_id": result.order_id,
                    "filled": True,
                    "actual_slippage": 0.0
                })
                
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
        """Print trading summary with AI agent stats"""
        balance = await self.exchange.get_balance()
        risk_report = self.risk_manager.get_risk_report()
        
        if os.name == 'nt':  # Windows
            logger.info("=" * 60)
            logger.info("TRADING SUMMARY - PHASE 3")
            logger.info("=" * 60)
        else:
            logger.info("=" * 60)
            logger.info("📈 TRADING SUMMARY - PHASE 3")
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
        logger.info("-" * 60)
        logger.info("AI Agent Performance:")
        
        for agent_name, agent in self.agents.items():
            status = agent.get_status()
            logger.info(f"  {agent_name}:")
            logger.info(f"    Status: {'🟢 Active' if status['active'] else '🔴 Inactive'}")
            
            if agent_name == "AgentX":
                logger.info(f"    Executions: {status['total_executions']}")
                logger.info(f"    Avg Slippage: {status['avg_slippage']*100:.3f}%")
                logger.info(f"    Fill Rate: {status['fill_rate']*100:.1f}%")
            elif agent_name == "Optima":
                logger.info(f"    Optimization Cycles: {status['optimization_cycles']}")
                logger.info(f"    Parameter Tests: {status['parameter_tests']}")
            elif agent_name == "HiveMind":
                logger.info(f"    Decisions Made: {status['decisions_made']}")
                logger.info(f"    Consensus Threshold: {status['consensus_threshold']:.2%}")
        
        logger.info("=" * 60)