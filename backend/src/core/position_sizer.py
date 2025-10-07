"""
Position Sizer for QuantumTrade Platform
Handles position sizing calculations based on various risk management strategies
"""

import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PositionSizer:
    """Calculates optimal position sizes based on risk management strategies"""

    def __init__(self):
        # Default configuration
        self.default_config = {
            "risk_per_trade": 0.01,  # 1% of account per trade
            "max_position_size": 0.05,  # 5% of account per position
            "stop_loss_percent": 0.02,  # 2% stop loss
            "take_profit_ratio": 2.0,  # 2:1 reward:risk ratio
        }

    def calculate_position_size_fixed(
        self, account_balance: float, fixed_size: float
    ) -> float:
        """
        Calculate fixed position size

        Args:
            account_balance (float): Current account balance
            fixed_size (float): Fixed position size

        Returns:
            float: Position size
        """
        try:
            position_size = min(
                fixed_size, account_balance * self.default_config["max_position_size"]
            )
            logger.debug(f"Fixed position size calculated: {position_size}")
            return position_size

        except Exception as e:
            logger.error(f"Error calculating fixed position size: {e}")
            return 0.0

    def calculate_position_size_percent(
        self, account_balance: float, percent: float
    ) -> float:
        """
        Calculate position size as percentage of account

        Args:
            account_balance (float): Current account balance
            percent (float): Percentage of account to use

        Returns:
            float: Position size
        """
        try:
            max_size = account_balance * self.default_config["max_position_size"]
            position_size = min(account_balance * percent, max_size)
            logger.debug(f"Percent-based position size calculated: {position_size}")
            return position_size

        except Exception as e:
            logger.error(f"Error calculating percent-based position size: {e}")
            return 0.0

    def calculate_position_size_kelly(
        self,
        win_rate: float,
        win_loss_ratio: float,
        account_balance: float,
        max_risk: float = None,
    ) -> float:
        """
        Calculate position size using Kelly Criterion

        Args:
            win_rate (float): Historical win rate (0-1)
            win_loss_ratio (float): Average win/average loss ratio
            account_balance (float): Current account balance
            max_risk (float): Maximum risk percentage (optional)

        Returns:
            float: Position size
        """
        try:
            # Kelly Criterion formula: f* = (bp - q) / b
            # where f* = fraction of capital to bet
            # b = net odds received on bet (win_loss_ratio)
            # p = probability of winning (win_rate)
            # q = probability of losing (1 - win_rate)

            if win_loss_ratio <= 0:
                logger.warning("Invalid win/loss ratio for Kelly calculation")
                return 0.0

            kelly_fraction = (
                (win_rate * win_loss_ratio) - (1 - win_rate)
            ) / win_loss_ratio

            # Use fractional Kelly (half Kelly) to be more conservative
            kelly_fraction = max(0, kelly_fraction) * 0.5

            # Apply maximum risk limit if specified
            if max_risk:
                kelly_fraction = min(kelly_fraction, max_risk)
            else:
                kelly_fraction = min(
                    kelly_fraction, self.default_config["risk_per_trade"]
                )

            position_size = account_balance * kelly_fraction
            logger.debug(
                f"Kelly position size calculated: {position_size} (fraction: {kelly_fraction:.4f})"
            )
            return position_size

        except Exception as e:
            logger.error(f"Error calculating Kelly position size: {e}")
            return 0.0

    def calculate_position_size_volatility(
        self,
        account_balance: float,
        atr: float,
        entry_price: float,
        stop_loss_distance: float = None,
    ) -> float:
        """
        Calculate position size based on volatility (ATR-based)

        Args:
            account_balance (float): Current account balance
            atr (float): Average True Range
            entry_price (float): Entry price
            stop_loss_distance (float): Stop loss distance in price terms

        Returns:
            float: Position size
        """
        try:
            # If stop loss distance not provided, use default
            if stop_loss_distance is None:
                stop_loss_distance = (
                    entry_price * self.default_config["stop_loss_percent"]
                )

            # Calculate risk per position
            risk_amount = account_balance * self.default_config["risk_per_trade"]

            # Position size = risk_amount / stop_loss_distance
            if stop_loss_distance > 0:
                position_size = risk_amount / stop_loss_distance
            else:
                position_size = 0.0

            # Apply maximum position size limit
            max_position = account_balance * self.default_config["max_position_size"]
            position_size = min(position_size, max_position)

            logger.debug(f"Volatility-based position size calculated: {position_size}")
            return position_size

        except Exception as e:
            logger.error(f"Error calculating volatility-based position size: {e}")
            return 0.0

    def calculate_risk_metrics(
        self,
        entry_price: float,
        position_size: float,
        stop_loss: float = None,
        take_profit: float = None,
    ) -> Dict:
        """
        Calculate risk metrics for a position

        Args:
            entry_price (float): Entry price
            position_size (float): Position size
            stop_loss (float): Stop loss price
            take_profit (float): Take profit price

        Returns:
            Dict: Risk metrics
        """
        try:
            # If stop loss not provided, calculate using default
            if stop_loss is None:
                stop_loss = entry_price * (1 - self.default_config["stop_loss_percent"])

            # If take profit not provided, calculate using default ratio
            if take_profit is None:
                risk_per_unit = entry_price - stop_loss
                take_profit = entry_price + (
                    risk_per_unit * self.default_config["take_profit_ratio"]
                )

            # Calculate metrics
            risk_amount = abs(entry_price - stop_loss) * position_size
            reward_amount = abs(take_profit - entry_price) * position_size
            reward_risk_ratio = reward_amount / risk_amount if risk_amount > 0 else 0

            metrics = {
                "position_value": entry_price * position_size,
                "risk_amount": risk_amount,
                "reward_amount": reward_amount,
                "reward_risk_ratio": reward_risk_ratio,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "risk_percent": (
                    (risk_amount / (entry_price * position_size)) * 100
                    if (entry_price * position_size) > 0
                    else 0
                ),
            }

            logger.debug(f"Risk metrics calculated: {metrics}")
            return metrics

        except Exception as e:
            logger.error(f"Error calculating risk metrics: {e}")
            return {}

    def adjust_position_size_for_correlation(
        self, position_size: float, correlation_factor: float
    ) -> float:
        """
        Adjust position size based on correlation with existing positions

        Args:
            position_size (float): Original position size
            correlation_factor (float): Correlation factor (0-1, where 1 is perfectly correlated)

        Returns:
            float: Adjusted position size
        """
        try:
            # Reduce position size for highly correlated assets
            adjusted_size = position_size * (1 - correlation_factor * 0.5)
            logger.debug(
                f"Position size adjusted for correlation: {position_size} -> {adjusted_size}"
            )
            return max(0, adjusted_size)

        except Exception as e:
            logger.error(f"Error adjusting position size for correlation: {e}")
            return position_size

    def get_position_sizing_config(self) -> Dict:
        """
        Get current position sizing configuration

        Returns:
            Dict: Configuration parameters
        """
        return self.default_config.copy()

    def update_position_sizing_config(self, config: Dict) -> None:
        """
        Update position sizing configuration

        Args:
            config (Dict): New configuration parameters
        """
        try:
            self.default_config.update(config)
            logger.info("Position sizing configuration updated")
        except Exception as e:
            logger.error(f"Error updating position sizing configuration: {e}")
