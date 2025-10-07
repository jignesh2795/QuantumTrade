"""
Performance Agent for QuantumTrade Platform
Computes trading performance metrics including Sharpe ratio, win/loss statistics, and other key performance indicators
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import math
import statistics

# Use absolute imports instead of relative imports
from database.models import Trade
from database.repositories import TradeRepository

logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """Container for performance metrics"""

    def __init__(self):
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0.0
        self.total_commission = 0.0
        self.win_rate = 0.0
        self.avg_win = 0.0
        self.avg_loss = 0.0
        self.max_win = 0.0
        self.max_loss = 0.0
        self.profit_factor = 0.0
        self.sharpe_ratio = 0.0
        self.max_drawdown = 0.0
        self.total_return = 0.0
        self.annualized_return = 0.0
        self.volatility = 0.0


class PerformanceAgent:
    """
    Computes trading performance metrics and statistics
    """

    def __init__(self, initial_capital: float = 10000.0):
        self.initial_capital = initial_capital
        self.trade_history: List[Dict] = []
        self.daily_returns: List[float] = []
        self.metrics = PerformanceMetrics()
        self.last_update = None

    def update_metrics(self, trade: Trade) -> None:
        """
        Update performance metrics with a new trade

        Args:
            trade: Trade object to include in metrics calculation
        """
        try:
            # Convert trade to dictionary if it's a Trade object
            if isinstance(trade, Trade):
                trade_dict = {
                    "symbol": trade.symbol,
                    "action": trade.action,
                    "size": trade.size,
                    "price": trade.price,
                    "timestamp": trade.timestamp,
                    "pnl": getattr(
                        trade, "pnl", 0.0
                    ),  # PnL might be calculated elsewhere
                    "commission": getattr(trade, "commission", 0.0),
                }
            else:
                trade_dict = trade

            # Add to trade history
            self.trade_history.append(trade_dict)

            # Update basic metrics
            self.metrics.total_trades += 1
            self.metrics.total_commission += trade_dict.get("commission", 0.0)

            # Calculate PnL if not provided
            pnl = trade_dict.get("pnl", 0.0)
            if pnl == 0 and "price" in trade_dict:
                # Simple PnL calculation (in a real system, this would be more complex)
                pnl = (
                    trade_dict["size"]
                    * trade_dict["price"]
                    * (1 if trade_dict["action"] == "SELL" else -1)
                )
                trade_dict["pnl"] = pnl

            self.metrics.total_pnl += pnl

            # Update win/loss statistics
            if pnl > 0:
                self.metrics.winning_trades += 1
                self.metrics.avg_win = (
                    (self.metrics.avg_win * (self.metrics.winning_trades - 1)) + pnl
                ) / self.metrics.winning_trades
                self.metrics.max_win = max(self.metrics.max_win, pnl)
            elif pnl < 0:
                self.metrics.losing_trades += 1
                self.metrics.avg_loss = (
                    (self.metrics.avg_loss * (self.metrics.losing_trades - 1))
                    + abs(pnl)
                ) / self.metrics.losing_trades
                self.metrics.max_loss = max(self.metrics.max_loss, abs(pnl))

            # Recalculate derived metrics
            self._calculate_derived_metrics()

            self.last_update = datetime.utcnow()
            logger.debug(
                f"Performance metrics updated with trade: {trade_dict['symbol']} {trade_dict['action']}"
            )

        except Exception as e:
            logger.error(f"Error updating performance metrics: {e}")

    def _calculate_derived_metrics(self) -> None:
        """Calculate derived performance metrics"""
        try:
            # Win rate
            if self.metrics.total_trades > 0:
                self.metrics.win_rate = (
                    self.metrics.winning_trades / self.metrics.total_trades
                )

            # Profit factor
            total_wins = (
                self.metrics.avg_win * self.metrics.winning_trades
                if self.metrics.winning_trades > 0
                else 0
            )
            total_losses = (
                self.metrics.avg_loss * self.metrics.losing_trades
                if self.metrics.losing_trades > 0
                else 0
            )
            self.metrics.profit_factor = (
                total_wins / total_losses if total_losses > 0 else float("inf")
            )

            # Total return
            if self.initial_capital > 0:
                self.metrics.total_return = (
                    self.metrics.total_pnl / self.initial_capital
                )

            # Sharpe ratio (simplified - would need risk-free rate in real implementation)
            if len(self.daily_returns) > 1:
                avg_return = statistics.mean(self.daily_returns)
                std_dev = (
                    statistics.stdev(self.daily_returns)
                    if len(self.daily_returns) > 1
                    else 0
                )
                self.metrics.sharpe_ratio = (
                    (avg_return / std_dev) * math.sqrt(252) if std_dev > 0 else 0
                )  # Annualized

        except Exception as e:
            logger.error(f"Error calculating derived metrics: {e}")

    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe ratio

        Args:
            risk_free_rate: Annual risk-free rate

        Returns:
            Sharpe ratio
        """
        try:
            if len(self.daily_returns) < 2:
                return 0.0

            # Calculate excess returns
            excess_returns = [
                r - (risk_free_rate / 252) for r in self.daily_returns
            ]  # Daily risk-free rate

            # Calculate Sharpe ratio
            avg_excess_return = statistics.mean(excess_returns)
            std_dev = statistics.stdev(excess_returns)

            if std_dev == 0:
                return 0.0

            # Annualized Sharpe ratio
            sharpe = (avg_excess_return / std_dev) * math.sqrt(252)
            self.metrics.sharpe_ratio = sharpe

            return sharpe

        except Exception as e:
            logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0.0

    def calculate_max_drawdown(self) -> float:
        """
        Calculate maximum drawdown

        Returns:
            Maximum drawdown as percentage
        """
        try:
            if not self.trade_history:
                return 0.0

            # Calculate equity curve
            equity_curve = [self.initial_capital]
            for trade in self.trade_history:
                pnl = trade.get("pnl", 0.0)
                equity_curve.append(equity_curve[-1] + pnl)

            # Calculate drawdowns
            peak = equity_curve[0]
            max_drawdown = 0.0

            for equity in equity_curve:
                if equity > peak:
                    peak = equity
                drawdown = (peak - equity) / peak if peak > 0 else 0
                max_drawdown = max(max_drawdown, drawdown)

            self.metrics.max_drawdown = max_drawdown
            return max_drawdown

        except Exception as e:
            logger.error(f"Error calculating max drawdown: {e}")
            return 0.0

    def calculate_win_loss_stats(self) -> Dict:
        """
        Calculate detailed win/loss statistics

        Returns:
            Dictionary with win/loss statistics
        """
        try:
            if self.metrics.total_trades == 0:
                return {}

            # Calculate additional statistics
            win_loss_ratio = (
                self.metrics.winning_trades / self.metrics.losing_trades
                if self.metrics.losing_trades > 0
                else float("inf")
            )
            expectancy = (
                (self.metrics.win_rate * self.metrics.avg_win)
                - ((1 - self.metrics.win_rate) * self.metrics.avg_loss)
                if self.metrics.avg_loss > 0
                else 0
            )

            stats = {
                "total_trades": self.metrics.total_trades,
                "winning_trades": self.metrics.winning_trades,
                "losing_trades": self.metrics.losing_trades,
                "win_rate": self.metrics.win_rate,
                "win_loss_ratio": win_loss_ratio,
                "avg_win": self.metrics.avg_win,
                "avg_loss": self.metrics.avg_loss,
                "max_win": self.metrics.max_win,
                "max_loss": self.metrics.max_loss,
                "profit_factor": self.metrics.profit_factor,
                "expectancy": expectancy,
            }

            return stats

        except Exception as e:
            logger.error(f"Error calculating win/loss stats: {e}")
            return {}

    def add_daily_return(self, daily_return: float) -> None:
        """
        Add daily return for volatility and Sharpe ratio calculations

        Args:
            daily_return: Daily return as decimal (e.g., 0.01 for 1%)
        """
        try:
            self.daily_returns.append(daily_return)

            # Keep only last 252 days (trading days in a year)
            if len(self.daily_returns) > 252:
                self.daily_returns = self.daily_returns[-252:]

            # Recalculate metrics that depend on daily returns
            self._calculate_derived_metrics()

        except Exception as e:
            logger.error(f"Error adding daily return: {e}")

    def get_performance_summary(self) -> Dict:
        """
        Get comprehensive performance summary

        Returns:
            Dictionary with all performance metrics
        """
        try:
            summary = {
                "timestamp": datetime.utcnow().isoformat(),
                "initial_capital": self.initial_capital,
                "total_trades": self.metrics.total_trades,
                "winning_trades": self.metrics.winning_trades,
                "losing_trades": self.metrics.losing_trades,
                "win_rate": self.metrics.win_rate,
                "total_pnl": self.metrics.total_pnl,
                "total_commission": self.metrics.total_commission,
                "total_return": self.metrics.total_return,
                "avg_win": self.metrics.avg_win,
                "avg_loss": self.metrics.avg_loss,
                "max_win": self.metrics.max_win,
                "max_loss": self.metrics.max_loss,
                "profit_factor": self.metrics.profit_factor,
                "sharpe_ratio": self.metrics.sharpe_ratio,
                "max_drawdown": self.metrics.max_drawdown,
                "annualized_return": self.metrics.annualized_return,
                "volatility": self.metrics.volatility,
                "last_update": (
                    self.last_update.isoformat() if self.last_update else None
                ),
            }

            return summary

        except Exception as e:
            logger.error(f"Error generating performance summary: {e}")
            return {}

    def reset_metrics(self) -> None:
        """Reset all performance metrics"""
        try:
            self.trade_history = []
            self.daily_returns = []
            self.metrics = PerformanceMetrics()
            self.last_update = None
            logger.info("Performance metrics reset")
        except Exception as e:
            logger.error(f"Error resetting performance metrics: {e}")

    def load_historical_trades(self, trades: List[Dict]) -> None:
        """
        Load historical trades for performance calculation

        Args:
            trades: List of trade dictionaries
        """
        try:
            for trade in trades:
                self.update_metrics(trade)
            logger.info(
                f"Loaded {len(trades)} historical trades for performance calculation"
            )
        except Exception as e:
            logger.error(f"Error loading historical trades: {e}")
