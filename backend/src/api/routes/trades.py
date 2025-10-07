"""
Trades API Routes for QuantumTrade Platform
Provides endpoints for trade history and trade execution
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from ...database.models import Trade
from ...database.repositories import TradeRepository
from ...core.market_data import MarketDataHandler

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trades", tags=["trades"])

# Initialize repositories and handlers
trade_repository = TradeRepository()
market_data_handler = MarketDataHandler()


@router.get("/history")
async def get_trade_history(
    symbol: Optional[str] = Query(None, description="Filter by trading symbol"),
    days: int = Query(30, description="Number of days of history", ge=1, le=365),
    limit: int = Query(
        100, description="Maximum number of trades to return", ge=1, le=1000
    ),
):
    """
    Get trade history

    Args:
        symbol: Filter by trading symbol (optional)
        days: Number of days of history (1-365)
        limit: Maximum number of trades to return (1-1000)

    Returns:
        List of recent trades
    """
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Get trades from repository
        if symbol:
            trades = trade_repository.get_trades_by_symbol(symbol, start_date, end_date)
        else:
            trades = trade_repository.get_trades_history(days)

        # Apply limit
        trades = trades[:limit] if trades else []

        # Convert to dictionary format
        trades_data = []
        for trade in trades:
            if hasattr(trade, "to_dict"):
                trades_data.append(trade.to_dict())
            else:
                # Handle case where to_dict method doesn't exist
                trade_dict = {}
                for attr in [
                    "id",
                    "symbol",
                    "action",
                    "size",
                    "price",
                    "timestamp",
                    "strategy_id",
                    "commission",
                    "slippage",
                ]:
                    if hasattr(trade, attr):
                        trade_dict[attr] = getattr(trade, attr)
                trades_data.append(trade_dict)

        return {
            "status": "success",
            "trades": trades_data,
            "count": len(trades_data),
            "filters": {"symbol": symbol, "days": days, "limit": limit},
        }
    except Exception as e:
        logger.error(f"Error fetching trade history: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{trade_id}")
async def get_trade_by_id(trade_id: int):
    """
    Get a specific trade by ID

    Args:
        trade_id: Trade ID

    Returns:
        Trade details
    """
    try:
        trade = trade_repository.get_trade_by_id(trade_id)
        if not trade:
            raise HTTPException(
                status_code=404, detail=f"Trade not found with ID {trade_id}"
            )

        return {
            "status": "success",
            "data": trade.to_dict() if hasattr(trade, "to_dict") else vars(trade),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching trade {trade_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/execute")
async def execute_trade(
    symbol: str = Body(..., description="Trading symbol"),
    action: str = Body(..., description="Trade action (BUY/SELL)"),
    size: float = Body(..., description="Position size"),
    price: Optional[float] = Body(
        None,
        description="Execution price (if not provided, current market price will be used)",
    ),
):
    """
    Execute a trade (simulated)

    Args:
        symbol: Trading symbol
        action: Trade action (BUY/SELL)
        size: Position size
        price: Execution price (optional)

    Returns:
        Trade execution result
    """
    try:
        # Validate action
        if action.upper() not in ["BUY", "SELL"]:
            raise HTTPException(status_code=400, detail="Action must be BUY or SELL")

        # If price not provided, get current market price
        if price is None:
            price_data = market_data_handler.get_live_price(symbol)
            if price_data and price_data.get("price"):
                price = price_data["price"]
            else:
                raise HTTPException(
                    status_code=404, detail=f"Unable to get current price for {symbol}"
                )

        # Create trade object
        trade = Trade()
        trade.symbol = symbol
        trade.action = action.upper()
        trade.size = size
        trade.price = price
        trade.timestamp = datetime.utcnow()
        trade.strategy_id = "manual"  # Manual trade
        trade.commission = abs(size * price * 0.001)  # 0.1% commission
        trade.slippage = 0.0  # No slippage in simulation

        # Save trade to database
        saved_trade = trade_repository.create_trade(trade)
        if not saved_trade:
            raise HTTPException(
                status_code=500, detail="Error saving trade to database"
            )

        logger.info(f"Executed trade: {symbol} {action} {size} @ {price}")

        return {
            "status": "success",
            "message": f"Trade executed successfully",
            "trade": (
                saved_trade.to_dict()
                if hasattr(saved_trade, "to_dict")
                else vars(saved_trade)
            ),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing trade: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats")
async def get_trading_statistics(
    symbol: Optional[str] = Query(None, description="Filter by trading symbol"),
    days: int = Query(30, description="Number of days for statistics", ge=1, le=365),
):
    """
    Get trading statistics

    Args:
        symbol: Filter by trading symbol (optional)
        days: Number of days for statistics (1-365)

    Returns:
        Trading statistics including win rate, average win/loss, etc.
    """
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Get trades
        if symbol:
            trades = trade_repository.get_trades_by_symbol(symbol, start_date, end_date)
        else:
            trades = trade_repository.get_trades_history(days)

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
            pnl = getattr(trade, "pnl", 0.0)
            if pnl == 0 and hasattr(trade, "size") and hasattr(trade, "price"):
                # Simple calculation
                pnl = trade.size * trade.price * (1 if trade.action == "SELL" else -1)

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


@router.delete("/{trade_id}")
async def cancel_trade(trade_id: int):
    """
    Cancel/Delete a trade (for simulation purposes)

    Args:
        trade_id: Trade ID to cancel

    Returns:
        Confirmation of cancellation
    """
    try:
        # In a real system, you might want to check if the trade can be canceled
        # For simulation, we'll just return a success message
        logger.info(f"Trade {trade_id} canceled")

        return {
            "status": "success",
            "message": f"Trade {trade_id} canceled successfully",
        }
    except Exception as e:
        logger.error(f"Error canceling trade {trade_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
