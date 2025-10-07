"""
Portfolio API Routes for QuantumTrade Platform
Provides endpoints for portfolio management and position tracking
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging

from ...core.portfolio import PortfolioManager
from ...core.market_data import MarketDataHandler

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

# Initialize portfolio manager
portfolio_manager = PortfolioManager()
market_data_handler = MarketDataHandler()


@router.get("/summary")
async def get_portfolio_summary():
    """
    Get current portfolio summary

    Returns:
        Portfolio summary including cash balance, positions, and performance metrics
    """
    try:
        # Update position prices with current market data
        positions = portfolio_manager.get_all_positions()
        if positions:
            symbols = [pos.symbol for pos in positions]
            current_prices = market_data_handler.get_multiple_symbols(symbols)
            price_dict = {
                symbol: data["price"] for symbol, data in current_prices.items() if data
            }
            portfolio_manager.update_position_prices(price_dict)

        summary = portfolio_manager.get_portfolio_summary()
        if not summary:
            raise HTTPException(
                status_code=500, detail="Error generating portfolio summary"
            )

        return {
            "status": "success",
            "data": summary.to_dict() if hasattr(summary, "to_dict") else summary,
        }
    except Exception as e:
        logger.error(f"Error fetching portfolio summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/positions")
async def get_portfolio_positions():
    """
    Get all current positions in the portfolio

    Returns:
        List of all current positions with details
    """
    try:
        positions = portfolio_manager.get_all_positions()
        positions_data = [
            pos.to_dict() if hasattr(pos, "to_dict") else pos.__dict__
            for pos in positions
        ]

        return {
            "status": "success",
            "positions": positions_data,
            "count": len(positions_data),
        }
    except Exception as e:
        logger.error(f"Error fetching portfolio positions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/position/{symbol}")
async def get_position(symbol: str):
    """
    Get details for a specific position

    Args:
        symbol: Trading symbol

    Returns:
        Position details
    """
    try:
        position = portfolio_manager.get_position(symbol)
        if not position:
            raise HTTPException(
                status_code=404, detail=f"Position not found for {symbol}"
            )

        return {
            "status": "success",
            "data": (
                position.to_dict()
                if hasattr(position, "to_dict")
                else position.__dict__
            ),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching position {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/position")
async def add_position(symbol: str, size: float, price: float):
    """
    Add or update a position in the portfolio

    Args:
        symbol: Trading symbol
        size: Position size (positive for long, negative for short)
        price: Entry price

    Returns:
        Updated position details
    """
    try:
        position = portfolio_manager.add_position(symbol, size, price)
        if not position:
            raise HTTPException(status_code=500, detail="Error adding position")

        return {
            "status": "success",
            "message": f"Position added for {symbol}",
            "data": (
                position.to_dict()
                if hasattr(position, "to_dict")
                else position.__dict__
            ),
        }
    except Exception as e:
        logger.error(f"Error adding position {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/position/{symbol}")
async def close_position(symbol: str, price: Optional[float] = None):
    """
    Close a position in the portfolio

    Args:
        symbol: Trading symbol
        price: Exit price (if not provided, current market price will be used)

    Returns:
        Confirmation of position closure
    """
    try:
        # If price not provided, get current market price
        if price is None:
            price_data = market_data_handler.get_live_price(symbol)
            if price_data:
                price = price_data["price"]
            else:
                raise HTTPException(
                    status_code=404, detail=f"Unable to get current price for {symbol}"
                )

        position = portfolio_manager.close_position(symbol, price)
        if not position:
            raise HTTPException(
                status_code=404, detail=f"Position not found for {symbol}"
            )

        return {
            "status": "success",
            "message": f"Position closed for {symbol}",
            "data": (
                position.to_dict()
                if hasattr(position, "to_dict")
                else position.__dict__
            ),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error closing position {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history")
async def get_transaction_history(
    limit: int = Query(
        50, description="Number of transactions to return", ge=1, le=1000
    )
):
    """
    Get transaction history

    Args:
        limit: Number of recent transactions to return (1-1000)

    Returns:
        List of recent transactions
    """
    try:
        history = portfolio_manager.get_transaction_history(limit)

        return {"status": "success", "transactions": history, "count": len(history)}
    except Exception as e:
        logger.error(f"Error fetching transaction history: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/performance")
async def get_portfolio_performance():
    """
    Get portfolio performance metrics

    Returns:
        Portfolio performance metrics including PnL, returns, etc.
    """
    try:
        # Update position prices first
        positions = portfolio_manager.get_all_positions()
        if positions:
            symbols = [pos.symbol for pos in positions]
            current_prices = market_data_handler.get_multiple_symbols(symbols)
            price_dict = {
                symbol: data["price"] for symbol, data in current_prices.items() if data
            }
            portfolio_manager.update_position_prices(price_dict)

        summary = portfolio_manager.get_portfolio_summary()
        if not summary:
            raise HTTPException(
                status_code=500, detail="Error generating portfolio summary"
            )

        # Calculate performance metrics
        performance = {
            "total_value": summary.total_value,
            "cash_balance": summary.cash_balance,
            "positions_value": summary.positions_value,
            "total_pnl": summary.total_pnl,
            "total_pnl_percent": summary.total_pnl_percent,
            "positions_count": len(summary.positions),
        }

        return {"status": "success", "data": performance}
    except Exception as e:
        logger.error(f"Error calculating portfolio performance: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
