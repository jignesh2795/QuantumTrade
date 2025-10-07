"""
Simplified Trading Routes for QuantumTrade Platform
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict
from ..core.trading_engine_simplified import run_strategy, calculate_pnl
from ..db.database import get_db_connection

router = APIRouter(prefix="/trade", tags=["trading"])


@router.get("/strategies")
async def get_strategies():
    """
    Get available trading strategies

    Returns:
        List of available strategies
    """
    return {"strategies": ["moving_average", "rsi", "bollinger_bands", "macd"]}


@router.post("/execute")
async def execute_trade(symbol: str, price: float, volume: int, trade_type: str):
    """
    Execute a trade

    Args:
        symbol: Trading symbol
        price: Trade price
        volume: Trade volume
        trade_type: Type of trade (BUY/SELL)

    Returns:
        Trade execution result
    """
    try:
        conn = await get_db_connection()
        await conn.execute(
            "INSERT INTO trades (symbol, price, volume, trade_type) VALUES ($1, $2, $3, $4)",
            symbol,
            price,
            volume,
            trade_type,
        )
        await conn.close()

        return {
            "status": "success",
            "message": f"Trade executed: {trade_type} {volume} shares of {symbol} at ${price}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing trade: {e}")


@router.get("/portfolio")
async def get_portfolio():
    """
    Get portfolio data

    Returns:
        Portfolio data
    """
    try:
        conn = await get_db_connection()
        rows = await conn.fetch("SELECT * FROM portfolio")
        await conn.close()

        portfolio = [dict(row) for row in rows]
        return {"portfolio": portfolio}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching portfolio: {e}")


@router.get("/history")
async def get_trade_history(limit: int = 100):
    """
    Get trade history

    Args:
        limit: Maximum number of trades to return

    Returns:
        Trade history
    """
    try:
        conn = await get_db_connection()
        rows = await conn.fetch(
            "SELECT * FROM trades ORDER BY timestamp DESC LIMIT $1", limit
        )
        await conn.close()

        trades = [dict(row) for row in rows]
        return {"trades": trades}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching trade history: {e}"
        )
