"""
Enhanced Trading Engine for QuantumTrade Platform
Handles live data processing, signal generation, order execution, and position management
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import json

# Local imports
from .market_data import MarketDataHandler
from .portfolio import PortfolioManager
from .risk_manager import RiskManager
from ..agents.data_agent import DataAgent
from ..agents.strategy_agent import StrategyAgent
from ..agents.risk_agent import RiskAgent
from ..agents.execution_agent import ExecutionAgent
from ..agents.performance_agent import PerformanceAgent
from ..database.models import Trade, Position
from ..database.repositories import TradeRepository, PositionRepository

logger = logging.getLogger(__name__)


class TradingEngine:
    """Main trading engine that coordinates all trading activities"""

    def __init__(self, initial_cash: float = 10000.0):
        # Initialize core components
        self.market_data_handler = MarketDataHandler()
        self.portfolio_manager = PortfolioManager(initial_cash)
        self.risk_manager = RiskManager()
        self.performance_agent = PerformanceAgent()

        # Initialize agents
        self.data_agent = DataAgent()
        self.strategy_agent = StrategyAgent()
        self.risk_agent = RiskAgent()
        self.execution_agent = ExecutionAgent()

        # Initialize repositories
        self.trade_repository = TradeRepository()
        self.position_repository = PositionRepository()

        # Trading state
        self.is_running = False
        self.active_symbols = ["BTC-USD", "ETH-USD", "AAPL", "GOOGL", "TSLA"]
        self.trading_interval = 60  # seconds

    def load_live_market_data(self, symbol: str) -> Optional[Dict]:
        """Load live market data for a symbol"""
        try:
            # Get live price data
            price_data = self.market_data_handler.get_live_price(symbol)
            if not price_data:
                logger.warning(f"Failed to get live price data for {symbol}")
                return None

            logger.info(f"Loaded live data for {symbol}: ${price_data['price']}")
            return price_data
        except Exception as e:
            logger.error(f"Error loading live market data for {symbol}: {e}")
            return None

    def generate_trading_signals(self, symbol: str, price_data: Dict) -> Dict:
        """Generate trading signals from multiple agents"""
        try:
            # Get signals from strategy agent
            signal = self.strategy_agent.generate_signal(price_data)

            # Add risk assessment to signal
            risk_assessment = self.risk_agent.assess_risk(
                position_size=signal.get("size", 0) * price_data.get("price", 0),
                account_balance=self.portfolio_manager.cash_balance,
                entry_price=price_data.get("price", 0),
                symbol=symbol,
            )

            signal["risk_assessment"] = risk_assessment
            logger.info(
                f"Generated signal for {symbol}: {signal['action']} (confidence: {signal['confidence']:.2f})"
            )

            return signal
        except Exception as e:
            logger.error(f"Error generating trading signals for {symbol}: {e}")
            return {
                "action": "HOLD",
                "confidence": 0.0,
                "risk_assessment": {"status": "RISKY"},
            }

    def assess_position_risk(self, symbol: str, signal: Dict) -> bool:
        """Assess risk for proposed position"""
        try:
            # Check if trade passes risk checks
            position_size = signal.get("size", 0)
            account_balance = self.portfolio_manager.cash_balance

            risk_result = self.risk_agent.assess_risk(
                position_size=position_size,
                account_balance=account_balance,
                entry_price=signal.get("price", 0),
                symbol=symbol,
            )

            is_risk_approved = risk_result.get("status") == "OK"
            logger.info(
                f"Risk assessment for {symbol}: {'APPROVED' if is_risk_approved else 'REJECTED'}"
            )

            return is_risk_approved
        except Exception as e:
            logger.error(f"Error in position risk assessment for {symbol}: {e}")
            return False

    def execute_trading_signal(self, symbol: str, signal: Dict) -> Optional[Trade]:
        """Execute trade based on trading signal"""
        try:
            # Skip if no action or risk not approved
            if signal["action"] == "HOLD":
                logger.info(f"Hold signal for {symbol}, no trade executed")
                return None

            if signal["risk_assessment"]["status"] != "OK":
                logger.warning(
                    f"Risk assessment failed for {symbol}, trade not executed"
                )
                return None

            # Execute the trade
            execution_result = self.execution_agent.execute_trade(
                symbol=symbol, action=signal["action"], size=signal["size"]
            )

            if execution_result and execution_result.get("status") == "filled":
                # Create trade record
                trade = Trade()
                trade.symbol = symbol
                trade.action = signal["action"]
                trade.size = signal["size"]
                trade.price = execution_result["price"]
                trade.timestamp = datetime.utcnow()
                trade.strategy_id = signal.get("strategy", "default")
                trade.commission = execution_result.get("commission", 0.0)
                trade.slippage = execution_result.get("slippage", 0.0)

                # Save trade to database
                saved_trade = self.trade_repository.create_trade(trade)
                logger.info(
                    f"Executed trade: {saved_trade.symbol} {saved_trade.action} {saved_trade.size} @ ${saved_trade.price}"
                )

                # Update performance metrics
                self.performance_agent.update_metrics(saved_trade)

                return saved_trade
            else:
                logger.warning(f"Trade not executed for {symbol}")
                return None

        except Exception as e:
            logger.error(f"Error executing trade for {symbol}: {e}")
            return None

    def update_portfolio_positions(self, trade: Trade) -> Optional[Position]:
        """Update portfolio positions based on executed trade"""
        try:
            # Update portfolio manager
            if trade.action == "BUY":
                position = self.portfolio_manager.add_position(
                    symbol=trade.symbol, size=trade.size, price=trade.price
                )
            else:  # SELL
                # For simplicity, we're closing the entire position
                # In a real implementation, you might want partial closes
                position = self.portfolio_manager.close_position(
                    symbol=trade.symbol, price=trade.price
                )

            if position:
                logger.info(
                    f"Updated portfolio position for {trade.symbol}: {position.size}"
                )
                return position
            else:
                logger.warning(
                    f"Failed to update portfolio position for {trade.symbol}"
                )
                return None

        except Exception as e:
            logger.error(f"Error updating portfolio positions for {trade.symbol}: {e}")
            return None

    def update_position_prices(self) -> None:
        """Update current prices for all positions"""
        try:
            positions = self.portfolio_manager.get_all_positions()
            if not positions:
                return

            # Get current prices for all positions
            symbols = [pos.symbol for pos in positions]
            current_prices = {}

            for symbol in symbols:
                price_data = self.market_data_handler.get_live_price(symbol)
                if price_data:
                    current_prices[symbol] = price_data["price"]

            # Update portfolio with current prices
            self.portfolio_manager.update_position_prices(current_prices)
            logger.info(f"Updated prices for {len(current_prices)} positions")

        except Exception as e:
            logger.error(f"Error updating position prices: {e}")

    def run_single_trading_cycle(self, symbol: str) -> Dict:
        """Run a complete trading cycle for a single symbol"""
        try:
            logger.info(f"Starting trading cycle for {symbol}")

            # 1. Load live market data
            price_data = self.load_live_market_data(symbol)
            if not price_data:
                return {"status": "error", "message": "Failed to retrieve market data"}

            # 2. Generate trading signals
            signal = self.generate_trading_signals(symbol, price_data)
            if signal["action"] == "HOLD":
                return {"status": "no_action", "message": "Hold signal generated"}

            # 3. Assess position risk
            if not self.assess_position_risk(symbol, signal):
                return {
                    "status": "risk_rejected",
                    "message": "Trade rejected by risk management",
                }

            # 4. Execute trade
            trade = self.execute_trading_signal(symbol, signal)
            if not trade:
                return {
                    "status": "execution_failed",
                    "message": "Trade execution failed",
                }

            # 5. Update portfolio positions
            position = self.update_portfolio_positions(trade)
            if not position:
                return {
                    "status": "position_update_failed",
                    "message": "Failed to update position",
                }

            # 6. Update performance metrics (already done in execute_trading_signal)

            return {
                "status": "success",
                "symbol": symbol,
                "trade": trade.to_dict() if trade else None,
                "position": position.to_dict() if position else None,
            }

        except Exception as e:
            logger.error(f"Error in trading cycle for {symbol}: {e}")
            return {"status": "error", "message": str(e)}

    def run_trading_cycle_for_all_symbols(self) -> List[Dict]:
        """Run trading cycles for all active symbols"""
        results = []

        for symbol in self.active_symbols:
            result = self.run_single_trading_cycle(symbol)
            results.append({"symbol": symbol, "result": result})

        return results

    def get_portfolio_summary(self) -> Dict:
        """Get current portfolio summary"""
        try:
            # Update position prices first
            self.update_position_prices()

            # Get portfolio summary
            summary = self.portfolio_manager.get_portfolio_summary()
            return summary.to_dict() if summary else {}
        except Exception as e:
            logger.error(f"Error getting portfolio summary: {e}")
            return {}

    def get_recent_trades(self, limit: int = 50) -> List[Dict]:
        """Get recent trades from database"""
        try:
            trades = self.trade_repository.get_trades_history(days=7)  # Last 7 days
            return [trade.to_dict() for trade in trades[:limit]]
        except Exception as e:
            logger.error(f"Error getting recent trades: {e}")
            return []

    def start_trading(self) -> None:
        """Start continuous trading (simplified version)"""
        try:
            self.is_running = True
            logger.info("Trading engine started")

            # Run one cycle for all symbols
            results = self.run_trading_cycle_for_all_symbols()

            for result in results:
                logger.info(
                    f"Trading result for {result['symbol']}: {result['result']['status']}"
                )

            self.is_running = False
            logger.info("Trading cycle completed")

        except Exception as e:
            logger.error(f"Error in trading engine: {e}")
            self.is_running = False

    def stop_trading(self) -> None:
        """Stop continuous trading"""
        self.is_running = False
        logger.info("Trading engine stopped")

    def add_symbol(self, symbol: str) -> None:
        """Add a symbol to the active symbols list"""
        if symbol not in self.active_symbols:
            self.active_symbols.append(symbol)
            logger.info(f"Added {symbol} to active symbols")

    def remove_symbol(self, symbol: str) -> None:
        """Remove a symbol from the active symbols list"""
        if symbol in self.active_symbols:
            self.active_symbols.remove(symbol)
            logger.info(f"Removed {symbol} from active symbols")

    def set_trading_interval(self, interval_seconds: int) -> None:
        """Set the trading interval in seconds"""
        self.trading_interval = interval_seconds
        logger.info(f"Set trading interval to {interval_seconds} seconds")

    def get_engine_status(self) -> Dict:
        """Get current engine status"""
        return {
            "is_running": self.is_running,
            "active_symbols": self.active_symbols,
            "trading_interval": self.trading_interval,
            "cash_balance": self.portfolio_manager.cash_balance,
            "positions_count": len(self.portfolio_manager.get_all_positions()),
        }
