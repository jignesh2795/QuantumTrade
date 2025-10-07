"""
Supabase Trades API Routes for QuantumTrade Platform
Provides endpoints for trade history and trade execution using Supabase
"""

from fastapi import APIRouter, HTTPException, Query, Body, Header
from typing import List, Optional
from datetime import datetime, timedelta
import logging
import uuid

from ...database.supabase_crud import SupabaseCRUD

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trades", tags=["trades"])

# Initialize Supabase CRUD
supabase_crud = SupabaseCRUD()


@router.get("/history")
async def get_trade_history(
    user_id: str = Header(..., description="User ID"),
    symbol: Optional[str] = Query(None, description="Filter by trading symbol"),
    days: int = Query(30, description="Number of days of history", ge=1, le=365),
    limit: int = Query(
        100, description="Maximum number of trades to return", ge=1, le=1000
    ),
):
    """
    Get trade history for a user

    Args:
        user_id: User ID (from header)
        symbol: Filter by trading symbol (optional)
        days: Number of days of history (1-365)
        limit: Maximum number of trades to return (1-1000)

    Returns:
        List of recent trades
    """
    try:
        # Get trades from Supabase
        trades = supabase_crud.get_trades(user_id, limit)

        # Filter by symbol if provided
        if symbol:
            trades = [trade for trade in trades if trade.get("asset") == symbol]

        # Filter by date range
        if trades:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            trades = [
                trade
                for trade in trades
                if datetime.fromisoformat(
                    trade.get("timestamp", "").replace("Z", "+00:00")
                )
                >= cutoff_date
            ]

        return {
            "status": "success",
            "trades": trades,
            "count": len(trades),
            "filters": {"symbol": symbol, "days": days, "limit": limit},
        }
    except Exception as e:
        logger.error(f"Error fetching trade history: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{trade_id}")
async def get_trade_by_id(
    trade_id: str, user_id: str = Header(..., description="User ID")
):
    """
    Get a specific trade by ID

    Args:
        trade_id: Trade ID
        user_id: User ID (from header)

    Returns:
        Trade details
    """
    try:
        # Get trade from Supabase
        trades = supabase_crud.get_trades(user_id)
        trade = next((t for t in trades if t.get("id") == trade_id), None)

        if not trade:
            raise HTTPException(
                status_code=404, detail=f"Trade not found with ID {trade_id}"
            )

        return {
            "status": "success",
            "data": trade,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching trade {trade_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/execute")
async def execute_trade(
    user_id: str = Header(..., description="User ID"),
    symbol: str = Body(..., description="Trading symbol"),
    action: str = Body(..., description="Trade action (BUY/SELL)"),
    amount: float = Body(..., description="Trade amount"),
    price: Optional[float] = Body(
        None,
        description="Execution price (if not provided, current market price will be used)",
    ),
):
    """
    Execute a trade and store in Supabase

    Args:
        user_id: User ID (from header)
        symbol: Trading symbol
        action: Trade action (BUY/SELL)
        amount: Trade amount
        price: Execution price (optional)

    Returns:
        Trade execution result
    """
    try:
        # Validate action
        if action.upper() not in ["BUY", "SELL"]:
            raise HTTPException(status_code=400, detail="Action must be BUY or SELL")

        # If price not provided, use a default value for simulation
        if price is None:
            price = 100.0  # Default price for simulation

        # Create trade in Supabase
        trade = supabase_crud.create_trade(
            user_id=user_id,
            asset=symbol,
            trade_type=action.upper(),
            amount=amount,
            price=price,
        )

        if not trade:
            raise HTTPException(
                status_code=500, detail="Error saving trade to Supabase"
            )

        logger.info(f"Executed trade: {symbol} {action} {amount} @ {price}")

        return {
            "status": "success",
            "message": f"Trade executed successfully",
            "trade": trade,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing trade: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats")
async def get_trading_statistics(
    user_id: str = Header(..., description="User ID"),
    symbol: Optional[str] = Query(None, description="Filter by trading symbol"),
    days: int = Query(30, description="Number of days for statistics", ge=1, le=365),
):
    """
    Get trading statistics for a user

    Args:
        user_id: User ID (from header)
        symbol: Filter by trading symbol (optional)
        days: Number of days for statistics (1-365)

    Returns:
        Trading statistics including win rate, average win/loss, etc.
    """
    try:
        # Get trades from Supabase
        trades = supabase_crud.get_trades(user_id)

        # Filter by symbol if provided
        if symbol:
            trades = [trade for trade in trades if trade.get("asset") == symbol]

        # Filter by date range
        if trades:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            trades = [
                trade
                for trade in trades
                if datetime.fromisoformat(
                    trade.get("timestamp", "").replace("Z", "+00:00")
                )
                >= cutoff_date
            ]

        if not trades:
            return {
                "status": "success",
                "data": {
                    "total_trades": 0,
                    "winning_trades": 0,
                    "losing_trades": 0,
                    "win_rate": 0.0,
                    "avg_win": 0.0,
                    "avg_loss": 0.0,
                    "total_pnl": 0.0,
                    "profit_factor": 0.0,
                },
            }

        # Calculate statistics
        total_trades = len(trades)
        winning_trades = 0
        losing_trades = 0
        total_pnl = 0.0
        total_wins = 0.0
        total_losses = 0.0

        for trade in trades:
            # Calculate PnL for this trade (simplified)
            amount = trade.get("amount", 0)
            price = trade.get("price", 0)
            trade_type = trade.get("trade_type", "")

            # Simple calculation
            pnl = amount * price * (1 if trade_type == "SELL" else -1)

            total_pnl += pnl

            if pnl > 0:
                winning_trades += 1
                total_wins += pnl
            elif pnl < 0:
                losing_trades += 1
                total_losses += abs(pnl)

        # Calculate derived statistics
        win_rate = winning_trades / total_trades if total_trades > 0 else 0.0
        avg_win = total_wins / winning_trades if winning_trades > 0 else 0.0
        avg_loss = total_losses / losing_trades if losing_trades > 0 else 0.0
        profit_factor = total_wins / total_losses if total_losses > 0 else float("inf")

        stats = {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": round(win_rate, 4),
            "avg_win": round(avg_win, 2),
            "avg_loss": round(avg_loss, 2),
            "total_pnl": round(total_pnl, 2),
            "profit_factor": (
                round(profit_factor, 2)
                if profit_factor != float("inf")
                else profit_factor
            ),
        }

        return {
            "status": "success",
            "data": stats,
            "filters": {"symbol": symbol, "days": days},
        }
    except Exception as e:
        logger.error(f"Error calculating trading statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
