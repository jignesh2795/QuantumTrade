"""
Risk Manager for QuantumTrade Platform
Handles risk assessment and management for trading positions
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
import math

logger = logging.getLogger(__name__)


class RiskManager:
    """Manages risk assessment and control for the trading system"""

    def __init__(self):
        # Default risk configuration
        self.config = {
            "max_drawdown_limit": 0.20,  # 20% maximum drawdown
            "max_daily_loss_limit": 0.05,  # 5% maximum daily loss
            "max_position_concentration": 0.25,  # 25% max in single position
            "max_correlation_exposure": 0.50,  # 50% max correlation exposure
            "value_at_risk_confidence": 0.95,  # 95% VaR confidence level
            "max_leverage": 2.0,  # Maximum leverage allowed
            "stop_loss_default": 0.02,  # 2% default stop loss
        }

        # Tracking variables
        self.daily_losses = 0.0
        self.max_equity = 0.0
        self.current_equity = 0.0
        self.positions = {}  # symbol -> position data
        self.correlation_matrix = {}  # symbol pairs -> correlation

    def assess_position_risk(
        self,
        symbol: str,
        position_size: float,
        entry_price: float,
        account_balance: float,
    ) -> Dict:
        """
        Assess risk for a proposed position

        Args:
            symbol (str): Trading symbol
            position_size (float): Proposed position size
            entry_price (float): Entry price
            account_balance (float): Current account balance

        Returns:
            Dict: Risk assessment results
        """
        try:
            # Calculate position value
            position_value = position_size * entry_price

            # Check position concentration
            concentration = (
                position_value / account_balance if account_balance > 0 else 0
            )
            concentration_ok = (
                concentration <= self.config["max_position_concentration"]
            )

            # Check overall leverage
            total_exposure = sum(pos.get("value", 0) for pos in self.positions.values())
            total_exposure += position_value
            leverage = total_exposure / account_balance if account_balance > 0 else 0
            leverage_ok = leverage <= self.config["max_leverage"]

            # Check correlation with existing positions
            correlation_risk = self._check_correlation_risk(symbol, position_value)
            correlation_ok = correlation_risk <= self.config["max_correlation_exposure"]

            # Overall risk assessment
            is_approved = concentration_ok and leverage_ok and correlation_ok

            assessment = {
                "approved": is_approved,
                "concentration": concentration,
                "concentration_ok": concentration_ok,
                "leverage": leverage,
                "leverage_ok": leverage_ok,
                "correlation_risk": correlation_risk,
                "correlation_ok": correlation_ok,
                "position_value": position_value,
                "reasons": [],
            }

            # Add reasons for rejection if not approved
            if not concentration_ok:
                assessment["reasons"].append("Position concentration too high")
            if not leverage_ok:
                assessment["reasons"].append("Leverage limit exceeded")
            if not correlation_ok:
                assessment["reasons"].append("Correlation risk too high")

            if is_approved:
                assessment["reasons"].append("All risk checks passed")

            logger.debug(
                f"Position risk assessment for {symbol}: {'APPROVED' if is_approved else 'REJECTED'}"
            )
            return assessment

        except Exception as e:
            logger.error(f"Error assessing position risk for {symbol}: {e}")
            return {
                "approved": False,
                "reasons": [f"Error in risk assessment: {str(e)}"],
            }

    def calculate_value_at_risk(
        self, returns: List[float], confidence_level: float = None
    ) -> float:
        """
        Calculate Value at Risk (VaR) using historical simulation method

        Args:
            returns (List[float]): Historical returns data
            confidence_level (float): Confidence level (default from config)

        Returns:
            float: Value at Risk
        """
        try:
            if not returns:
                return 0.0

            if confidence_level is None:
                confidence_level = self.config["value_at_risk_confidence"]

            # Sort returns
            sorted_returns = sorted(returns)

            # Calculate percentile index
            percentile_index = int((1 - confidence_level) * len(sorted_returns))

            # VaR is the negative of the percentile return
            var = (
                -sorted_returns[percentile_index]
                if percentile_index < len(sorted_returns)
                else 0.0
            )

            logger.debug(
                f"Calculated VaR: {var:.4f} at {confidence_level*100}% confidence"
            )
            return var

        except Exception as e:
            logger.error(f"Error calculating VaR: {e}")
            return 0.0

    def check_drawdown_limits(
        self, current_equity: float, starting_equity: float
    ) -> Dict:
        """
        Check if drawdown limits are exceeded

        Args:
            current_equity (float): Current equity value
            starting_equity (float): Starting equity value

        Returns:
            Dict: Drawdown check results
        """
        try:
            # Update equity tracking
            self.current_equity = current_equity
            self.max_equity = max(self.max_equity, current_equity)

            # Calculate drawdown
            if self.max_equity > 0:
                drawdown = (self.max_equity - current_equity) / self.max_equity
            else:
                drawdown = 0.0

            # Check against limit
            drawdown_ok = drawdown <= self.config["max_drawdown_limit"]

            result = {
                "drawdown": drawdown,
                "drawdown_percent": drawdown * 100,
                "limit_exceeded": not drawdown_ok,
                "max_drawdown_limit": self.config["max_drawdown_limit"],
                "max_equity": self.max_equity,
                "current_equity": current_equity,
            }

            if not drawdown_ok:
                logger.warning(f"Drawdown limit exceeded: {drawdown*100:.2f}%")

            return result

        except Exception as e:
            logger.error(f"Error checking drawdown limits: {e}")
            return {"drawdown": 0.0, "limit_exceeded": False, "error": str(e)}

    def check_daily_loss_limits(self) -> Dict:
        """
        Check if daily loss limits are exceeded

        Returns:
            Dict: Daily loss check results
        """
        try:
            # Check against daily limit
            daily_loss_ok = self.daily_losses <= self.config["max_daily_loss_limit"]

            result = {
                "daily_losses": self.daily_losses,
                "daily_loss_percent": self.daily_losses * 100,
                "limit_exceeded": not daily_loss_ok,
                "max_daily_loss_limit": self.config["max_daily_loss_limit"],
            }

            if not daily_loss_ok:
                logger.warning(
                    f"Daily loss limit exceeded: {self.daily_losses*100:.2f}%"
                )

            return result

        except Exception as e:
            logger.error(f"Error checking daily loss limits: {e}")
            return {"daily_losses": 0.0, "limit_exceeded": False, "error": str(e)}

    def update_position_tracking(self, symbol: str, position_data: Dict) -> None:
        """
        Update position tracking data

        Args:
            symbol (str): Trading symbol
            position_data (Dict): Position data to track
        """
        try:
            self.positions[symbol] = position_data
            logger.debug(f"Updated position tracking for {symbol}")
        except Exception as e:
            logger.error(f"Error updating position tracking for {symbol}: {e}")

    def update_correlation_data(self, symbol_pairs: Dict[str, float]) -> None:
        """
        Update correlation matrix data

        Args:
            symbol_pairs (Dict[str, float]): Dictionary of symbol pairs and their correlations
        """
        try:
            self.correlation_matrix.update(symbol_pairs)
            logger.debug(f"Updated correlation data for {len(symbol_pairs)} pairs")
        except Exception as e:
            logger.error(f"Error updating correlation data: {e}")

    def _check_correlation_risk(self, symbol: str, position_value: float) -> float:
        """
        Check correlation risk with existing positions

        Args:
            symbol (str): Trading symbol
            position_value (float): Proposed position value

        Returns:
            float: Correlation risk score (0-1)
        """
        try:
            if not self.positions or not self.correlation_matrix:
                return 0.0

            # Calculate weighted correlation with existing positions
            total_correlation_risk = 0.0
            total_weight = 0.0

            for existing_symbol, existing_pos in self.positions.items():
                # Get correlation between symbols
                pair_key1 = f"{symbol}:{existing_symbol}"
                pair_key2 = f"{existing_symbol}:{symbol}"

                correlation = (
                    self.correlation_matrix.get(pair_key1)
                    or self.correlation_matrix.get(pair_key2)
                    or 0.0
                )

                # Weight by position size
                existing_value = existing_pos.get("value", 0)
                weight = (
                    existing_value / (existing_value + position_value)
                    if (existing_value + position_value) > 0
                    else 0
                )

                total_correlation_risk += correlation * weight
                total_weight += weight

            correlation_score = (
                total_correlation_risk / total_weight if total_weight > 0 else 0.0
            )
            return min(1.0, max(0.0, correlation_score))

        except Exception as e:
            logger.error(f"Error checking correlation risk for {symbol}: {e}")
            return 0.0

    def calculate_stop_loss(
        self, entry_price: float, volatility: float = None, atr: float = None
    ) -> float:
        """
        Calculate appropriate stop loss level

        Args:
            entry_price (float): Entry price
            volatility (float): Price volatility (optional)
            atr (float): Average True Range (optional)

        Returns:
            float: Stop loss price
        """
        try:
            # If ATR provided, use it for dynamic stop loss
            if atr and atr > 0:
                stop_loss_distance = atr * 2  # 2x ATR stop loss
            # If volatility provided, use it
            elif volatility and volatility > 0:
                stop_loss_distance = entry_price * volatility * 2
            # Otherwise use default
            else:
                stop_loss_distance = entry_price * self.config["stop_loss_default"]

            stop_loss = entry_price - stop_loss_distance
            logger.debug(
                f"Calculated stop loss: {stop_loss} (distance: {stop_loss_distance})"
            )
            return max(0, stop_loss)

        except Exception as e:
            logger.error(f"Error calculating stop loss: {e}")
            # Return default stop loss
            return entry_price * (1 - self.config["stop_loss_default"])

    def reset_daily_tracking(self) -> None:
        """Reset daily tracking counters"""
        try:
            self.daily_losses = 0.0
            logger.info("Daily tracking counters reset")
        except Exception as e:
            logger.error(f"Error resetting daily tracking: {e}")

    def update_after_trade(self, trade_result: Dict) -> None:
        """
        Update risk tracking after a trade

        Args:
            trade_result (Dict): Trade execution results
        """
        try:
            pnl = trade_result.get("pnl", 0.0)
            if pnl < 0:
                self.daily_losses += (
                    abs(pnl) / self.current_equity if self.current_equity > 0 else 0
                )

            logger.debug(
                f"Updated risk tracking after trade, daily losses: {self.daily_losses}"
            )
        except Exception as e:
            logger.error(f"Error updating risk tracking after trade: {e}")

    def get_risk_configuration(self) -> Dict:
        """
        Get current risk configuration

        Returns:
            Dict: Current risk configuration
        """
        return self.config.copy()

    def update_risk_configuration(self, config: Dict) -> None:
        """
        Update risk configuration

        Args:
            config (Dict): New configuration parameters
        """
        try:
            self.config.update(config)
            logger.info("Risk configuration updated")
        except Exception as e:
            logger.error(f"Error updating risk configuration: {e}")
