"""
Backtest routes for QuantumTrade backend.
API endpoints to trigger/run backtests.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import pandas as pd
from ..services.backtest_service import backtest_service
from ..core.utils import format_response

router = APIRouter(prefix="/backtest", tags=["backtest"])


class BacktestRequest(BaseModel):
    strategy_name: str
    symbol: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


@router.post("/run", response_model=dict)
async def run_backtest(request: BacktestRequest):
    """Run a backtest."""
    try:
        # Generate mock data for backtesting
        # In a real implementation, you would fetch actual historical data
        data = pd.DataFrame()  # Empty DataFrame for mock

        # Run backtest
        results = await backtest_service.run_backtest(
            strategy_name=request.strategy_name,
            data=data,
            parameters=request.parameters,
        )

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results/{backtest_id}", response_model=dict)
async def get_backtest_results(backtest_id: int):
    """Get backtest results by ID."""
    try:
        results = backtest_service.get_backtest_results(backtest_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=dict)
async def list_backtests():
    """List all backtests."""
    try:
        results = backtest_service.list_backtests()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=dict)
async def backtest_status():
    """Get backtest service status."""
    try:
        return format_response(
            {"status": "operational", "message": "Backtest service is running"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
