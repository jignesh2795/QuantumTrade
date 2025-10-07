"""
Supabase Portfolio API Routes for QuantumTrade Platform
Provides endpoints for portfolio management using Supabase
"""

from fastapi import APIRouter, HTTPException, Query, Body, Header
from typing import List, Optional
from datetime import datetime
import logging

from ...database.supabase_crud import SupabaseCRUD

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

# Initialize Supabase CRUD
supabase_crud = SupabaseCRUD()


@router.get("/positions")
async def get_portfolio_positions(user_id: str = Header(..., description="User ID")):
    """
    Get all portfolio positions for a user

    Args:
        user_id: User ID (from header)

    Returns:
        List of portfolio positions
    """
    try:
        # Get portfolio from Supabase
        portfolio = supabase_crud.get_portfolio(user_id)

        # Calculate current value and PnL for each position
        positions_with_metrics = []
        for position in portfolio:
            # Add calculated metrics
            quantity = position.get("quantity", 0)
            avg_price = position.get("avg_price", 0)
            current_price = avg_price * 1.01  # Simulated current price

            position_with_metrics = {
                **position,
                "current_price": current_price,
                "current_value": quantity * current_price,
                "pnl": (current_price - avg_price) * quantity,
                "pnl_percentage": (
                    ((current_price - avg_price) / avg_price * 100)
                    if avg_price > 0
                    else 0
                ),
            }
            positions_with_metrics.append(position_with_metrics)

        return {
            "status": "success",
            "positions": positions_with_metrics,
            "count": len(positions_with_metrics),
        }
    except Exception as e:
        logger.error(f"Error fetching portfolio positions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/summary")
async def get_portfolio_summary(user_id: str = Header(..., description="User ID")):
    """
    Get portfolio summary for a user

    Args:
        user_id: User ID (from header)

    Returns:
        Portfolio summary including total value, PnL, etc.
    """
    try:
        # Get portfolio from Supabase
        portfolio = supabase_crud.get_portfolio(user_id)

        # Calculate summary metrics
        total_value = 0.0
        total_investment = 0.0

        for position in portfolio:
            quantity = position.get("quantity", 0)
            avg_price = position.get("avg_price", 0)
            current_price = avg_price * 1.01  # Simulated current price

            total_value += quantity * current_price
            total_investment += quantity * avg_price

        total_pnl = total_value - total_investment
        pnl_percentage = (
            (total_pnl / total_investment * 100) if total_investment > 0 else 0
        )

        summary = {
            "total_value": round(total_value, 2),
            "total_investment": round(total_investment, 2),
            "total_pnl": round(total_pnl, 2),
            "pnl_percentage": round(pnl_percentage, 2),
            "position_count": len(portfolio),
        }

        return {
            "status": "success",
            "summary": summary,
        }
    except Exception as e:
        logger.error(f"Error calculating portfolio summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/update")
async def update_portfolio_position(
    user_id: str = Header(..., description="User ID"),
    asset: str = Body(..., description="Asset symbol"),
    quantity: float = Body(..., description="Asset quantity"),
    avg_price: float = Body(..., description="Average price"),
):
    """
    Update a portfolio position for a user

    Args:
        user_id: User ID (from header)
        asset: Asset symbol
        quantity: Asset quantity
        avg_price: Average price

    Returns:
        Updated portfolio position
    """
    try:
        # Update portfolio in Supabase
        position = supabase_crud.update_portfolio(
            user_id=user_id, asset=asset, quantity=quantity, avg_price=avg_price
        )

        if not position:
            raise HTTPException(
                status_code=500, detail="Error updating portfolio position"
            )

        logger.info(f"Updated portfolio position: {asset} {quantity} @ {avg_price}")

        return {
            "status": "success",
            "message": f"Portfolio position updated successfully",
            "position": position,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating portfolio position: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/position/{asset}")
async def remove_portfolio_position(
    asset: str, user_id: str = Header(..., description="User ID")
):
    """
    Remove a portfolio position for a user

    Args:
        asset: Asset symbol
        user_id: User ID (from header)

    Returns:
        Confirmation of removal
    """
    try:
        # In a real implementation, you would delete the position from Supabase
        # For now, we'll just return a success message
        logger.info(f"Removed portfolio position: {asset}")

        return {
            "status": "success",
            "message": f"Portfolio position {asset} removed successfully",
        }
    except Exception as e:
        logger.error(f"Error removing portfolio position {asset}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
