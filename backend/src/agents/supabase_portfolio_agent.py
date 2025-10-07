"""
Supabase Portfolio Agent for QuantumTrade Platform
Manages portfolio positions and integrates with Supabase for data persistence
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from ..database.supabase_client import get_supabase_client
from ..database.supabase_models import Portfolio

logger = logging.getLogger(__name__)
supabase = get_supabase_client()


class SupabasePortfolioAgent:
    """
    Manages portfolio positions and integrates with Supabase for data persistence
    """

    def __init__(self, user_id: str):
        self.user_id = user_id

    def add_position(self, asset: str, quantity: float, avg_price: float) -> Dict:
        """
        Add or update a position in the portfolio

        Args:
            asset: Asset symbol
            quantity: Asset quantity
            avg_price: Average price

        Returns:
            Dictionary with operation result
        """
        try:
            # First, try to update existing position
            response = (
                supabase.table("portfolio")
                .update(
                    {
                        "quantity": quantity,
                        "avg_price": avg_price,
                        "updated_at": datetime.utcnow().isoformat(),
                    }
                )
                .eq("user_id", self.user_id)
                .eq("asset", asset)
                .execute()
            )

            # If no record was updated, create a new one
            if not response.data:
                portfolio_data = {
                    "user_id": self.user_id,
                    "asset": asset,
                    "quantity": quantity,
                    "avg_price": avg_price,
                }
                response = supabase.table("portfolio").insert(portfolio_data).execute()

            if response.data and len(response.data) > 0:
                position = response.data[0]
                logger.info(f"Position updated: {asset} {quantity} @ {avg_price}")

                return {
                    "status": "success",
                    "position_id": position.get("id"),
                    "asset": asset,
                    "quantity": quantity,
                    "avg_price": avg_price,
                    "message": f"Position updated successfully",
                }
            else:
                raise Exception("Failed to update portfolio position")

        except Exception as e:
            logger.error(f"Error updating position: {e}")
            return {
                "status": "error",
                "message": str(e),
                "asset": asset,
                "quantity": quantity,
                "avg_price": avg_price,
            }

    def remove_position(self, asset: str) -> bool:
        """
        Remove a position from the portfolio

        Args:
            asset: Asset symbol

        Returns:
            True if successful, False otherwise
        """
        try:
            response = (
                supabase.table("portfolio")
                .delete()
                .eq("user_id", self.user_id)
                .eq("asset", asset)
                .execute()
            )

            if response.data and len(response.data) > 0:
                logger.info(f"Position removed: {asset}")
                return True
            else:
                logger.warning(f"Position not found for removal: {asset}")
                return False
        except Exception as e:
            logger.error(f"Error removing position {asset}: {e}")
            return False

    def get_position(self, asset: str) -> Optional[Dict]:
        """
        Get a specific position

        Args:
            asset: Asset symbol

        Returns:
            Position data or None if not found
        """
        try:
            response = (
                supabase.table("portfolio")
                .select("*")
                .eq("user_id", self.user_id)
                .eq("asset", asset)
                .execute()
            )

            return (
                response.data[0] if response.data and len(response.data) > 0 else None
            )
        except Exception as e:
            logger.error(f"Error fetching position {asset}: {e}")
            return None

    def list_positions(self) -> List[Dict]:
        """
        List all positions in the portfolio

        Returns:
            List of position data
        """
        try:
            response = (
                supabase.table("portfolio")
                .select("*")
                .eq("user_id", self.user_id)
                .execute()
            )

            positions = response.data if response.data else []

            # Add calculated metrics
            for position in positions:
                quantity = position.get("quantity", 0)
                avg_price = position.get("avg_price", 0)
                current_price = self._get_current_price(position.get("asset"))

                position["current_price"] = current_price
                position["current_value"] = quantity * current_price
                position["pnl"] = (current_price - avg_price) * quantity
                position["pnl_percentage"] = (
                    ((current_price - avg_price) / avg_price * 100)
                    if avg_price > 0
                    else 0
                )

            return positions
        except Exception as e:
            logger.error(f"Error listing positions: {e}")
            return []

    def get_portfolio_summary(self) -> Dict:
        """
        Get portfolio summary

        Returns:
            Portfolio summary data
        """
        try:
            positions = self.list_positions()

            total_value = 0.0
            total_investment = 0.0

            for position in positions:
                total_value += position.get("current_value", 0)
                total_investment += position.get("quantity", 0) * position.get(
                    "avg_price", 0
                )

            total_pnl = total_value - total_investment
            pnl_percentage = (
                (total_pnl / total_investment * 100) if total_investment > 0 else 0
            )

            return {
                "total_value": round(total_value, 2),
                "total_investment": round(total_investment, 2),
                "total_pnl": round(total_pnl, 2),
                "pnl_percentage": round(pnl_percentage, 2),
                "position_count": len(positions),
                "positions": positions,
            }
        except Exception as e:
            logger.error(f"Error calculating portfolio summary: {e}")
            return {
                "total_value": 0,
                "total_investment": 0,
                "total_pnl": 0,
                "pnl_percentage": 0,
                "position_count": 0,
                "positions": [],
            }

    def _get_current_price(self, asset: str) -> float:
        """
        Get current price for an asset (simulated)

        Args:
            asset: Asset symbol

        Returns:
            Simulated current price
        """
        # In a real implementation, this would fetch from a market data provider
        # For now, we'll return a simulated price
        import random

        base_prices = {
            "BTC-USD": 45000,
            "ETH-USD": 3000,
            "AAPL": 150,
            "GOOGL": 2500,
            "TSLA": 200,
        }
        base_price = base_prices.get(asset, 100)
        # Add some random volatility for simulation
        volatility = 0.01  # 1% volatility
        return base_price * (1 + random.uniform(-volatility, volatility))

    def update_position_size(self, asset: str, delta_quantity: float) -> Dict:
        """
        Update position size by adding/subtracting quantity

        Args:
            asset: Asset symbol
            delta_quantity: Change in quantity (positive to add, negative to subtract)

        Returns:
            Dictionary with operation result
        """
        try:
            # Get current position
            current_position = self.get_position(asset)

            if current_position:
                current_quantity = current_position.get("quantity", 0)
                current_avg_price = current_position.get("avg_price", 0)

                new_quantity = current_quantity + delta_quantity

                # If new quantity is zero or negative, remove the position
                if new_quantity <= 0:
                    self.remove_position(asset)
                    return {
                        "status": "success",
                        "message": f"Position {asset} removed (quantity became zero or negative)",
                    }
                else:
                    # Update the position with new quantity
                    # For simplicity, we'll keep the same average price
                    # In a real implementation, you might want to recalculate the average price
                    return self.add_position(asset, new_quantity, current_avg_price)
            else:
                # If position doesn't exist and we're adding, create it
                if delta_quantity > 0:
                    current_price = self._get_current_price(asset)
                    return self.add_position(asset, delta_quantity, current_price)
                else:
                    return {
                        "status": "error",
                        "message": f"Cannot subtract from non-existent position {asset}",
                    }
        except Exception as e:
            logger.error(f"Error updating position size for {asset}: {e}")
            return {"status": "error", "message": str(e)}
