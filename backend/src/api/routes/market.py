"""
Market Data API Routes for QuantumTrade Platform
Provides endpoints for accessing market data and price information
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from ...core.market_data import MarketDataHandler
from ...agents.data_agent import DataAgent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/market", tags=["market"])

# Initialize market data handler
market_data_handler = MarketDataHandler()


@router.get("/data")
async def get_market_data(symbol: str = Query(..., description="Trading symbol")):
    """
    Get live market data for a specific symbol

    Args:
        symbol: Trading symbol (e.g., BTC-USD, ETH-USD)

    Returns:
        Live market data including price, volume, and OHLC data
    """
    try:
        price_data = market_data_handler.get_live_price(symbol)
        if not price_data:
            raise HTTPException(
                status_code=404, detail=f"Market data not available for {symbol}"
            )

        return {
            "status": "success",
            "data": price_data,
            "timestamp": price_data.get("timestamp"),
        }
    except Exception as e:
        logger.error(f"Error fetching market data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/historical")
async def get_historical_data(
    symbol: str = Query(..., description="Trading symbol"),
    days: int = Query(
        30, description="Number of days of historical data", ge=1, le=365
    ),
):
    """
    Get historical market data for a specific symbol

    Args:
        symbol: Trading symbol
        days: Number of days of historical data (1-365)

    Returns:
        Historical price data including OHLC and volume
    """
    try:
        historical_data = market_data_handler.get_historical_data(symbol, days)
        if not historical_data:
            raise HTTPException(
                status_code=404, detail=f"Historical data not available for {symbol}"
            )

        return {
            "status": "success",
            "symbol": symbol,
            "days": days,
            "data": historical_data,
            "count": len(historical_data),
        }
    except Exception as e:
        logger.error(f"Error fetching historical data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/snapshot")
async def get_market_snapshot():
    """
    Get current market snapshot

    Returns:
        Market snapshot including major indices and market conditions
    """
    try:
        snapshot = market_data_handler.get_market_snapshot()
        return {
            "status": "success",
            "data": snapshot,
            "timestamp": snapshot.get("timestamp"),
        }
    except Exception as e:
        logger.error(f"Error fetching market snapshot: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/symbols")
async def get_available_symbols():
    """
    Get list of available trading symbols

    Returns:
        List of available trading symbols
    """
    try:
        # In a real implementation, this would come from a data source
        # For now, we'll return a static list
        symbols = [
            "BTC-USD",
            "ETH-USD",
            "SOL-USD",
            "AAPL",
            "GOOGL",
            "TSLA",
            "SPX",
            "NDX",
        ]
        return {"status": "success", "symbols": symbols, "count": len(symbols)}
    except Exception as e:
        logger.error(f"Error fetching available symbols: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/batch")
async def get_batch_market_data(
    symbols: List[str] = Query(..., description="List of trading symbols")
):
    """
    Get live market data for multiple symbols

    Args:
        symbols: List of trading symbols

    Returns:
        Live market data for all requested symbols
    """
    try:
        if not symbols:
            raise HTTPException(
                status_code=400, detail="At least one symbol is required"
            )

        prices = market_data_handler.get_multiple_symbols(symbols)

        return {"status": "success", "data": prices, "count": len(prices)}
    except Exception as e:
        logger.error(f"Error fetching batch market data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
