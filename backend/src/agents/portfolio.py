"""
Portfolio Agent for QuantumTrade Platform
Tracks open positions, PnL, and unrealized gains
"""

import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class PortfolioAgent:
    """
    Tracks open positions, PnL, and unrealized gains
    """

    def __init__(self, initial_balance: float = 10000.0):
        """
        Initialize PortfolioAgent

        Args:
            initial_balance: Initial account balance
        """
        self.initial_balance = initial_balance
        self.cash_balance = initial_balance
        self.positions = {}  # symbol -> position details
        self.trade_history = []  # List of all trades
        self.pnl_history = []  # List of PnL values over time

    def add_position(self, symbol: str, size: float, price: float) -> Dict:
        """
        Add or update a position in the portfolio

        Args:
            symbol: Trading symbol
            size: Position size (positive for long, negative for short)
            price: Entry price

        Returns:
            Dictionary with position details
        """
        try:
            # Calculate cost
            cost = size * price

            # Check if we have enough cash
            if cost > self.cash_balance and size > 0:
                return {
                    "status": "error",
                    "message": "Insufficient funds",
                    "cash_balance": self.cash_balance,
                }

            # Update cash balance
            self.cash_balance -= cost

            # Update or create position
            if symbol in self.positions:
                # Update existing position
                existing_position = self.positions[symbol]
                new_size = existing_position["size"] + size
                new_avg_price = (
                    (
                        (existing_position["size"] * existing_position["avg_price"])
                        + (size * price)
                    )
                    / new_size
                    if new_size != 0
                    else 0
                )

                self.positions[symbol] = {
                    "symbol": symbol,
                    "size": new_size,
                    "avg_price": new_avg_price,
                    "current_price": price,  # Initially same as entry price
                    "timestamp": datetime.utcnow().isoformat(),
                }
            else:
                # Create new position
                self.positions[symbol] = {
                    "symbol": symbol,
                    "size": size,
                    "avg_price": price,
                    "current_price": price,
                    "timestamp": datetime.utcnow().isoformat(),
                }

            # Record trade
            trade = {
                "symbol": symbol,
                "size": size,
                "price": price,
                "cost": cost,
                "timestamp": datetime.utcnow().isoformat(),
                "action": "BUY" if size > 0 else "SELL",
            }
            self.trade_history.append(trade)

            # Update PnL history
            self._update_pnl_history()

            logger.info(f"Position added/updated for {symbol}: {size} @ {price}")

            return {
                "status": "success",
                "message": "Position added/updated",
                "position": self.positions[symbol],
                "cash_balance": self.cash_balance,
            }

        except Exception as e:
            logger.error(f"Error adding position for {symbol}: {e}")
            return {"status": "error", "message": f"Error adding position: {str(e)}"}

    def close_position(self, symbol: str, price: float) -> Dict:
        """
        Close a position in the portfolio

        Args:
            symbol: Trading symbol
            price: Exit price

        Returns:
            Dictionary with trade details
        """
        try:
            if symbol not in self.positions:
                return {"status": "error", "message": f"No position found for {symbol}"}

            # Get position details
            position = self.positions[symbol]
            size = -position["size"]  # Close entire position (opposite size)
            avg_price = position["avg_price"]

            # Calculate proceeds
            proceeds = size * price

            # Update cash balance
            self.cash_balance += proceeds

            # Calculate PnL
            pnl = proceeds - (position["size"] * avg_price)

            # Remove position
            del self.positions[symbol]

            # Record trade
            trade = {
                "symbol": symbol,
                "size": size,
                "price": price,
                "proceeds": proceeds,
                "pnl": pnl,
                "timestamp": datetime.utcnow().isoformat(),
                "action": "SELL" if size > 0 else "BUY",
            }
            self.trade_history.append(trade)

            # Update PnL history
            self._update_pnl_history()

            logger.info(f"Position closed for {symbol}: {size} @ {price}, PnL: {pnl}")

            return {
                "status": "success",
                "message": "Position closed",
                "trade": trade,
                "cash_balance": self.cash_balance,
            }

        except Exception as e:
            logger.error(f"Error closing position for {symbol}: {e}")
            return {"status": "error", "message": f"Error closing position: {str(e)}"}

    def update_position_prices(self, prices: Dict[str, float]) -> None:
        """
        Update current prices for positions

        Args:
            prices: Dictionary mapping symbols to current prices
        """
        try:
            for symbol, price in prices.items():
                if symbol in self.positions:
                    self.positions[symbol]["current_price"] = price

            # Update PnL history with new prices
            self._update_pnl_history()

        except Exception as e:
            logger.error(f"Error updating position prices: {e}")

    def get_position(self, symbol: str) -> Dict:
        """
        Get details for a specific position

        Args:
            symbol: Trading symbol

        Returns:
            Dictionary with position details
        """
        try:
            if symbol in self.positions:
                position = self.positions[symbol].copy()
                # Calculate unrealized PnL
                position["unrealized_pnl"] = self._calculate_unrealized_pnl(symbol)
                position["unrealized_pnl_percent"] = (
                    self._calculate_unrealized_pnl_percent(symbol)
                )
                return position
            else:
                return {"status": "error", "message": f"No position found for {symbol}"}
        except Exception as e:
            logger.error(f"Error getting position {symbol}: {e}")
            return {"status": "error", "message": f"Error getting position: {str(e)}"}

    def list_positions(self) -> Dict:
        """
        List all positions in the portfolio

        Returns:
            Dictionary with positions and summary
        """
        try:
            positions_with_pnl = []
            total_unrealized_pnl = 0.0

            for symbol, position in self.positions.items():
                position_copy = position.copy()
                # Calculate unrealized PnL for each position
                unrealized_pnl = self._calculate_unrealized_pnl(symbol)
                unrealized_pnl_percent = self._calculate_unrealized_pnl_percent(symbol)

                position_copy["unrealized_pnl"] = unrealized_pnl
                position_copy["unrealized_pnl_percent"] = unrealized_pnl_percent

                positions_with_pnl.append(position_copy)
                total_unrealized_pnl += unrealized_pnl

            total_portfolio_value = self.cash_balance + sum(
                pos["current_price"] * abs(pos["size"]) for pos in positions_with_pnl
            )

            return {
                "positions": positions_with_pnl,
                "count": len(positions_with_pnl),
                "cash_balance": self.cash_balance,
                "total_unrealized_pnl": total_unrealized_pnl,
                "total_portfolio_value": total_portfolio_value,
                "total_pnl": total_unrealized_pnl
                + sum(trade.get("pnl", 0) for trade in self.trade_history),
            }
        except Exception as e:
            logger.error(f"Error listing positions: {e}")
            return {
                "positions": [],
                "count": 0,
                "error": f"Error listing positions: {str(e)}",
            }

    def get_portfolio_summary(self) -> Dict:
        """
        Get portfolio summary including PnL and risk metrics

        Returns:
            Dictionary with portfolio summary
        """
        try:
            positions_data = self.list_positions()

            if "error" in positions_data:
                return positions_data

            total_value = positions_data["total_portfolio_value"]
            cash_balance = positions_data["cash_balance"]
            unrealized_pnl = positions_data["total_unrealized_pnl"]
            total_pnl = positions_data["total_pnl"]

            # Calculate return percentages
            total_return_percent = (
                ((total_value - self.initial_balance) / self.initial_balance * 100)
                if self.initial_balance > 0
                else 0
            )
            unrealized_return_percent = (
                (unrealized_pnl / self.initial_balance * 100)
                if self.initial_balance > 0
                else 0
            )

            return {
                "initial_balance": self.initial_balance,
                "cash_balance": cash_balance,
                "total_portfolio_value": total_value,
                "total_unrealized_pnl": unrealized_pnl,
                "total_unrealized_pnl_percent": unrealized_return_percent,
                "total_pnl": total_pnl,
                "total_return_percent": total_return_percent,
                "positions_count": positions_data["count"],
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting portfolio summary: {e}")
            return {"error": f"Error getting portfolio summary: {str(e)}"}

    def get_trade_history(self, limit: int = 50) -> List[Dict]:
        """
        Get recent trade history

        Args:
            limit: Maximum number of trades to return

        Returns:
            List of recent trades
        """
        try:
            return self.trade_history[-limit:]
        except Exception as e:
            logger.error(f"Error getting trade history: {e}")
            return []

    def _calculate_unrealized_pnl(self, symbol: str) -> float:
        """
        Calculate unrealized PnL for a position

        Args:
            symbol: Trading symbol

        Returns:
            Unrealized PnL
        """
        try:
            if symbol not in self.positions:
                return 0.0

            position = self.positions[symbol]
            size = position["size"]
            avg_price = position["avg_price"]
            current_price = position["current_price"]

            # For long positions: (current_price - avg_price) * size
            # For short positions: (avg_price - current_price) * abs(size)
            if size > 0:  # Long position
                return (current_price - avg_price) * size
            elif size < 0:  # Short position
                return (avg_price - current_price) * abs(size)
            else:
                return 0.0
        except Exception as e:
            logger.error(f"Error calculating unrealized PnL for {symbol}: {e}")
            return 0.0

    def _calculate_unrealized_pnl_percent(self, symbol: str) -> float:
        """
        Calculate unrealized PnL percentage for a position

        Args:
            symbol: Trading symbol

        Returns:
            Unrealized PnL percentage
        """
        try:
            if symbol not in self.positions:
                return 0.0

            position = self.positions[symbol]
            size = position["size"]
            avg_price = position["avg_price"]
            current_price = position["current_price"]

            if avg_price <= 0:
                return 0.0

            # Calculate percentage change
            if size > 0:  # Long position
                return ((current_price - avg_price) / avg_price) * 100
            elif size < 0:  # Short position
                return ((avg_price - current_price) / avg_price) * 100
            else:
                return 0.0
        except Exception as e:
            logger.error(f"Error calculating unrealized PnL percent for {symbol}: {e}")
            return 0.0

    def _update_pnl_history(self) -> None:
        """Update PnL history with current portfolio value"""
        try:
            summary = self.get_portfolio_summary()
            if "error" not in summary:
                self.pnl_history.append(
                    {
                        "timestamp": datetime.utcnow().isoformat(),
                        "total_value": summary["total_portfolio_value"],
                        "unrealized_pnl": summary["total_unrealized_pnl"],
                        "total_pnl": summary["total_pnl"],
                    }
                )

                # Keep only last 1000 data points
                if len(self.pnl_history) > 1000:
                    self.pnl_history = self.pnl_history[-1000:]
        except Exception as e:
            logger.error(f"Error updating PnL history: {e}")
