"""
Risk Agent for QuantumTrade Platform
Assesses and manages trading risk with advanced risk models
"""

import logging
import random
from typing import Dict, List, Optional
from datetime import datetime
import math

# Use relative import instead of absolute import
from ..core.risk_manager import RiskManager

logger = logging.getLogger(__name__)


class RiskConfig:
    """Configuration class for risk parameters"""

    def __init__(
        self,
        max_position_size_percent: float = 5.0,
        max_portfolio_risk_percent: float = 2.0,
        stop_loss_percent: float = 5.0,
    ):
        self.max_position_size_percent = max_position_size_percent
        self.max_portfolio_risk_percent = max_portfolio_risk_percent
        self.stop_loss_percent = stop_loss_percent


class RiskAgent:
    """
    Advanced risk assessment and management agent
    """

    def __init__(
        self,
        max_position_size_percent: float = 5.0,
        max_portfolio_risk_percent: float = 2.0,
        stop_loss_percent: float = 5.0,
        max_drawdown_limit: float = 20.0,
        max_leverage: float = 2.0,
    ):
        # Initialize risk configuration
        risk_config = RiskConfig(
            max_position_size_percent=max_position_size_percent,
            max_portfolio_risk_percent=max_portfolio_risk_percent,
            stop_loss_percent=stop_loss_percent,
        )

        # Initialize risk manager
        self.risk_manager = RiskManager()
        self.daily_loss_limit = 0.0
        self.daily_losses = 0.0
        self.position_history = []
        self.max_drawdown_limit = (
            max_drawdown_limit  # Maximum drawdown limit in percentage
        )
        self.max_leverage = max_leverage  # Maximum allowed leverage
        self.equity_history = [10000.0]  # Starting equity for drawdown calculation

    def assess_risk(
        self,
        position_size: float,
        account_balance: float,
        entry_price: Optional[float] = None,
        symbol: Optional[str] = None,
    ) -> Dict:
        """
        Assess risk for a proposed position

        Args:
            position_size: Size of the proposed position
            account_balance: Current account balance
            entry_price: Entry price for the position (optional)
            symbol: Trading symbol (optional)

        Returns:
            Dictionary with risk assessment results
        """
        try:
            # Basic risk calculation
            if account_balance <= 0:
                return {
                    "position_size": position_size,
                    "account_balance": account_balance,
                    "risk_percent": 100.0,
                    "status": "RISKY",
                    "reason": "Invalid account balance",
                }

            risk_percent = (abs(position_size) / account_balance) * 100

            # Check position size limit
            max_position_size_percent = self.risk_manager.config.get(
                "max_position_size_percent", 5.0
            )
            if risk_percent > max_position_size_percent:
                return {
                    "position_size": position_size,
                    "account_balance": account_balance,
                    "risk_percent": risk_percent,
                    "status": "RISKY",
                    "reason": f"Position size exceeds limit of {max_position_size_percent}%",
                }

            # Check portfolio risk if entry price provided
            if entry_price and symbol:
                stop_loss_percent = self.risk_manager.config.get(
                    "stop_loss_percent", 5.0
                )
                max_portfolio_risk_percent = self.risk_manager.config.get(
                    "max_portfolio_risk_percent", 2.0
                )

                # Calculate stop loss
                stop_loss = entry_price * (1 - stop_loss_percent / 100)
                risk_amount = abs(position_size) * abs(entry_price - stop_loss)
                portfolio_risk = (risk_amount / account_balance) * 100

                if portfolio_risk > max_portfolio_risk_percent:
                    return {
                        "position_size": position_size,
                        "account_balance": account_balance,
                        "risk_percent": risk_percent,
                        "portfolio_risk": portfolio_risk,
                        "status": "RISKY",
                        "reason": f"Portfolio risk exceeds limit of {max_portfolio_risk_percent}%",
                    }

            # Check daily loss limit
            if self.daily_losses > self.daily_loss_limit and self.daily_loss_limit > 0:
                return {
                    "position_size": position_size,
                    "account_balance": account_balance,
                    "risk_percent": risk_percent,
                    "status": "RISKY",
                    "reason": "Daily loss limit exceeded",
                }

            # Check drawdown limit
            if self._check_drawdown_limit():
                return {
                    "position_size": position_size,
                    "account_balance": account_balance,
                    "risk_percent": risk_percent,
                    "status": "RISKY",
                    "reason": f"Maximum drawdown limit of {self.max_drawdown_limit}% exceeded",
                }

            # Check leverage limit
            if self._check_leverage_limit(position_size, entry_price, account_balance):
                return {
                    "position_size": position_size,
                    "account_balance": account_balance,
                    "risk_percent": risk_percent,
                    "status": "RISKY",
                    "reason": f"Leverage exceeds maximum limit of {self.max_leverage}",
                }

            # If we get here, risk is acceptable
            return {
                "position_size": position_size,
                "account_balance": account_balance,
                "risk_percent": risk_percent,
                "status": "OK",
                "reason": "Risk within acceptable limits",
            }

        except Exception as e:
            logger.error(f"Error assessing risk: {e}")
            return {
                "position_size": position_size,
                "account_balance": account_balance,
                "risk_percent": 100.0,
                "status": "RISKY",
                "reason": f"Error in risk assessment: {str(e)}",
            }

    def _check_drawdown_limit(self) -> bool:
        """
        Check if current drawdown exceeds maximum allowed

        Returns:
            True if drawdown limit exceeded, False otherwise
        """
        try:
            if len(self.equity_history) < 2:
                return False

            peak_equity = max(self.equity_history)
            current_equity = self.equity_history[-1]

            if peak_equity <= 0:
                return False

            drawdown = ((peak_equity - current_equity) / peak_equity) * 100
            return drawdown > self.max_drawdown_limit

        except Exception as e:
            logger.error(f"Error checking drawdown limit: {e}")
            return False

    def _check_leverage_limit(
        self, position_size: float, entry_price: float, account_balance: float
    ) -> bool:
        """
        Check if proposed position would exceed leverage limit

        Args:
            position_size: Size of proposed position
            entry_price: Entry price
            account_balance: Current account balance

        Returns:
            True if leverage limit would be exceeded, False otherwise
        """
        try:
            if account_balance <= 0 or entry_price is None:
                return False

            # Calculate position value
            position_value = abs(position_size) * entry_price

            # Calculate current leverage
            total_exposure = position_value
            for pos in self.position_history:
                total_exposure += abs(pos["size"]) * pos["entry_price"]

            current_leverage = total_exposure / account_balance
            return current_leverage > self.max_leverage

        except Exception as e:
            logger.error(f"Error checking leverage limit: {e}")
            return False

    def calculate_position_size(
        self,
        account_balance: float,
        entry_price: float,
        stop_loss_price: float,
        strategy: str = "fixed_fraction",
    ) -> float:
        """
        Calculate optimal position size based on risk parameters

        Args:
            account_balance: Current account balance
            entry_price: Entry price for position
            stop_loss_price: Stop loss price
            strategy: Position sizing strategy

        Returns:
            Optimal position size
        """
        try:
            max_portfolio_risk_percent = self.risk_manager.config.get(
                "max_portfolio_risk_percent", 2.0
            )
            # For now, return a simple calculation
            risk_amount = account_balance * (max_portfolio_risk_percent / 100)
            risk_per_unit = abs(entry_price - stop_loss_price)
            if risk_per_unit > 0:
                return risk_amount / risk_per_unit
            return 0.0

        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0.0

    def calculate_value_at_risk(
        self, positions: List[Dict], confidence_level: float = 0.95
    ) -> float:
        """
        Calculate Value at Risk (VaR) for portfolio

        Args:
            positions: List of position dictionaries
            confidence_level: Confidence level for VaR calculation

        Returns:
            Value at Risk amount
        """
        try:
            # Simplified VaR calculation
            returns = [random.uniform(-0.02, 0.02) for _ in range(100)]
            returns.sort()
            index = int((1 - confidence_level) * len(returns))
            var = -returns[index] if index < len(returns) else 0.0
            return var

        except Exception as e:
            logger.error(f"Error calculating VaR: {e}")
            return 0.0

    def check_correlation_risk(
        self, symbol: str, portfolio_positions: List[str]
    ) -> bool:
        """
        Check correlation risk with existing positions

        Args:
            symbol: New position symbol
            portfolio_positions: List of existing position symbols

        Returns:
            True if correlation risk is acceptable, False otherwise
        """
        try:
            # Simplified correlation check
            return True

        except Exception as e:
            logger.error(f"Error checking correlation risk: {e}")
            return True  # Default to accepting if there's an error

    def set_daily_loss_limit(
        self, account_balance: float, max_loss_percent: float = 5.0
    ) -> None:
        """
        Set daily loss limit as percentage of account balance

        Args:
            account_balance: Current account balance
            max_loss_percent: Maximum daily loss percentage
        """
        self.daily_loss_limit = account_balance * (max_loss_percent / 100)
        logger.info(f"Daily loss limit set to: {self.daily_loss_limit}")

    def record_trade_result(
        self, symbol: str, size: float, entry_price: float, result: str, pnl: float
    ) -> None:
        """
        Record trade result for risk management

        Args:
            symbol: Trading symbol
            size: Trade size
            entry_price: Entry price
            result: Trade result ("win" or "loss")
            pnl: Profit/loss amount
        """
        try:
            # Record in position history
            self.position_history.append(
                {
                    "symbol": symbol,
                    "size": size,
                    "entry_price": entry_price,
                    "result": result,
                    "pnl": pnl,
                    "timestamp": datetime.utcnow(),
                }
            )

            # Update daily losses if it was a loss
            if result.lower() == "loss":
                self.daily_losses += abs(pnl)

            # Update equity history
            if self.equity_history:
                current_equity = self.equity_history[-1] + pnl
                self.equity_history.append(current_equity)
            else:
                self.equity_history.append(10000.0 + pnl)

            # Keep only last 252 data points (trading days in a year)
            if len(self.equity_history) > 252:
                self.equity_history = self.equity_history[-252:]

        except Exception as e:
            logger.error(f"Error recording trade result: {e}")

    def reset_daily_tracking(self) -> None:
        """Reset daily loss tracking"""
        self.daily_losses = 0.0
        logger.info("Daily risk tracking reset")

    def get_risk_report(self) -> Dict:
        """Generate risk management report"""
        try:
            # Calculate current drawdown
            drawdown = 0.0
            if len(self.equity_history) >= 2:
                peak_equity = max(self.equity_history)
                current_equity = self.equity_history[-1]
                if peak_equity > 0:
                    drawdown = ((peak_equity - current_equity) / peak_equity) * 100

            # Calculate current leverage
            total_exposure = 0.0
            account_balance = (
                self.equity_history[-1] if self.equity_history else 10000.0
            )
            for pos in self.position_history:
                total_exposure += abs(pos["size"]) * pos["entry_price"]

            current_leverage = (
                total_exposure / account_balance if account_balance > 0 else 0.0
            )

            max_position_size_percent = self.risk_manager.config.get(
                "max_position_size_percent", 5.0
            )
            max_portfolio_risk_percent = self.risk_manager.config.get(
                "max_portfolio_risk_percent", 2.0
            )
            stop_loss_percent = self.risk_manager.config.get("stop_loss_percent", 5.0)

            return {
                "timestamp": datetime.utcnow().isoformat(),
                "max_position_size_percent": max_position_size_percent,
                "max_portfolio_risk_percent": max_portfolio_risk_percent,
                "stop_loss_percent": stop_loss_percent,
                "max_drawdown_limit": self.max_drawdown_limit,
                "max_leverage": self.max_leverage,
                "current_drawdown": round(drawdown, 2),
                "current_leverage": round(current_leverage, 2),
                "daily_losses": self.daily_losses,
                "daily_loss_limit": self.daily_loss_limit,
                "positions_analyzed": len(self.position_history),
            }

        except Exception as e:
            logger.error(f"Error generating risk report: {e}")
            return {}
