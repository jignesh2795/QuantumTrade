"""
Backtesting API Routes for QuantumTrade Platform
Provides endpoints for running backtests and retrieving backtest results
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import logging
import asyncio
import json

from ...agents.strategy_agent import StrategyAgent
from ...core.market_data import MarketDataHandler
from ...database.models import BacktestResult
from ...database.repositories import BacktestRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/backtest", tags=["backtesting"])

# Initialize components
market_data_handler = MarketDataHandler()
backtest_repository = BacktestRepository()


@router.post("/run")
async def run_backtest(
    strategy: str = Body(..., description="Strategy to backtest"),
    symbol: str = Body(..., description="Trading symbol"),
    start_date: str = Body(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Body(..., description="End date (YYYY-MM-DD)"),
    initial_capital: float = Body(10000.0, description="Initial capital for backtest"),
    position_size: float = Body(1.0, description="Position size multiplier"),
):
    """
    Run a backtest for a specific strategy and symbol

    Args:
        strategy: Strategy to backtest (e.g., moving_average, rsi, breakout)
        symbol: Trading symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        initial_capital: Initial capital for backtest
        position_size: Position size multiplier

    Returns:
        Backtest results including performance metrics
    """
    try:
        # Parse dates
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
            )

        if start_dt >= end_dt:
            raise HTTPException(
                status_code=400, detail="Start date must be before end date"
            )

        # Get historical data
        days = (end_dt - start_dt).days
        if days > 365:
            raise HTTPException(
                status_code=400, detail="Maximum backtest period is 365 days"
            )

        historical_data = market_data_handler.get_historical_data(symbol, days)
        if not historical_data:
            raise HTTPException(
                status_code=404, detail=f"No historical data available for {symbol}"
            )

        # Initialize strategy agent
        strategy_agent = StrategyAgent(symbol, strategy)

        # Run backtest simulation
        results = await _run_backtest_simulation(
            strategy_agent, historical_data, initial_capital, position_size
        )

        # Save results to database
        backtest_result = BacktestResult()
        backtest_result.strategy = strategy
        backtest_result.symbol = symbol
        backtest_result.start_date = start_dt
        backtest_result.end_date = end_dt
        backtest_result.initial_capital = initial_capital
        backtest_result.final_capital = results["final_capital"]
        backtest_result.total_return = results["total_return"]
        backtest_result.max_drawdown = results["max_drawdown"]
        backtest_result.sharpe_ratio = results["sharpe_ratio"]
        backtest_result.win_rate = results["win_rate"]
        backtest_result.total_trades = results["total_trades"]
        backtest_result.timestamp = datetime.utcnow()

        saved_result = backtest_repository.create_backtest_result(backtest_result)

        return {
            "status": "success",
            "message": "Backtest completed successfully",
            "results": results,
            "backtest_id": saved_result.id if saved_result else None,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running backtest: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def _run_backtest_simulation(
    strategy_agent, historical_data, initial_capital, position_size
):
    """
    Run backtest simulation

    Args:
        strategy_agent: Strategy agent to test
        historical_data: Historical price data
        initial_capital: Initial capital
        position_size: Position size multiplier

    Returns:
        Backtest results
    """
    try:
        # Initialize simulation variables
        capital = initial_capital
        position = 0
        position_value = 0
        trades = []
        equity_curve = [capital]
        peak_capital = capital

        # Process each day of historical data
        for i, data_point in enumerate(historical_data):
            # Create price data for strategy agent
            price_data = {
                "symbol": data_point["symbol"],
                "price": data_point["close"],
                "timestamp": data_point["date"],
            }

            # Generate signal
            signal = strategy_agent.generate_signal(price_data)

            # Execute trade based on signal
            if signal["action"] == "BUY" and position <= 0:
                # Close short position if exists
                if position < 0:
                    capital += abs(position) * data_point["close"]

                # Open long position
                position = position_size * signal["size"]
                position_value = position * data_point["close"]
                capital -= position_value
                trades.append(
                    {
                        "date": data_point["date"],
                        "action": "BUY",
                        "size": position,
                        "price": data_point["close"],
                        "capital": capital,
                    }
                )

            elif signal["action"] == "SELL" and position >= 0:
                # Close long position if exists
                if position > 0:
                    capital += position * data_point["close"]

                # Open short position
                position = -position_size * signal["size"]
                position_value = abs(position) * data_point["close"]
                capital += position_value
                trades.append(
                    {
                        "date": data_point["date"],
                        "action": "SELL",
                        "size": position,
                        "price": data_point["close"],
                        "capital": capital,
                    }
                )

            # Update equity curve
            current_value = capital + (position * data_point["close"])
            equity_curve.append(current_value)

            # Update peak capital for drawdown calculation
            peak_capital = max(peak_capital, current_value)

        # Close any open positions at the end
        if position != 0 and historical_data:
            final_price = historical_data[-1]["close"]
            capital += position * final_price
            trades.append(
                {
                    "date": historical_data[-1]["date"],
                    "action": "CLOSE",
                    "size": -position,
                    "price": final_price,
                    "capital": capital,
                }
            )

        # Calculate performance metrics
        final_capital = capital
        total_return = (final_capital - initial_capital) / initial_capital

        # Calculate max drawdown
        peak = initial_capital
        max_drawdown = 0.0
        for equity in equity_curve:
            if equity > peak:
                peak = equity
            drawdown = (peak - equity) / peak if peak > 0 else 0
            max_drawdown = max(max_drawdown, drawdown)

        # Calculate Sharpe ratio (simplified)
        if len(equity_curve) > 1:
            returns = [
                (equity_curve[i] - equity_curve[i - 1]) / equity_curve[i - 1]
                for i in range(1, len(equity_curve))
                if equity_curve[i - 1] > 0
            ]
            if returns and len(returns) > 1:
                avg_return = sum(returns) / len(returns)
                std_dev = (
                    sum((r - avg_return) ** 2 for r in returns) / (len(returns) - 1)
                ) ** 0.5
                sharpe_ratio = (avg_return / std_dev) * (252**0.5) if std_dev > 0 else 0
            else:
                sharpe_ratio = 0.0
        else:
            sharpe_ratio = 0.0

        # Calculate win rate
        winning_trades = (
            sum(
                1
                for trade in trades
                if trade.get("capital", 0) > initial_capital / len(trades)
            )
            if trades
            else 0
        )
        win_rate = winning_trades / len(trades) if trades else 0.0

        results = {
            "initial_capital": initial_capital,
            "final_capital": final_capital,
            "total_return": total_return,
            "total_return_percent": total_return * 100,
            "max_drawdown": max_drawdown,
            "max_drawdown_percent": max_drawdown * 100,
            "sharpe_ratio": sharpe_ratio,
            "total_trades": len(trades),
            "win_rate": win_rate,
            "win_rate_percent": win_rate * 100,
            "trades": trades[-50:],  # Return last 50 trades
        }

        return results
    except Exception as e:
        logger.error(f"Error in backtest simulation: {e}")
        raise


@router.get("/results")
async def get_backtest_results(
    strategy: Optional[str] = Query(None, description="Filter by strategy"),
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    limit: int = Query(50, description="Number of results to return", ge=1, le=1000),
):
    """
    Get backtest results

    Args:
        strategy: Filter by strategy (optional)
        symbol: Filter by symbol (optional)
        limit: Number of results to return (1-1000)

    Returns:
        List of backtest results
    """
    try:
        if strategy and symbol:
            results = backtest_repository.get_backtest_results_by_strategy_and_symbol(
                strategy, symbol, limit
            )
        elif strategy:
            results = backtest_repository.get_backtest_results_by_strategy(
                strategy, limit
            )
        elif symbol:
            results = backtest_repository.get_backtest_results_by_symbol(symbol, limit)
        else:
            results = backtest_repository.get_all_backtest_results(limit)

        # Convert to dictionary format
        results_data = []
        for result in results:
            if hasattr(result, "to_dict"):
                results_data.append(result.to_dict())
            else:
                result_dict = {}
                for attr in [
                    "id",
                    "strategy",
                    "symbol",
                    "start_date",
                    "end_date",
                    "initial_capital",
                    "final_capital",
                    "total_return",
                    "max_drawdown",
                    "sharpe_ratio",
                    "win_rate",
                    "total_trades",
                    "timestamp",
                ]:
                    if hasattr(result, attr):
                        value = getattr(result, attr)
                        # Convert datetime to string
                        if isinstance(value, datetime):
                            value = value.isoformat()
                        result_dict[attr] = value
                results_data.append(result_dict)

        return {
            "status": "success",
            "results": results_data,
            "count": len(results_data),
        }
    except Exception as e:
        logger.error(f"Error fetching backtest results: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/results/{backtest_id}")
async def get_backtest_result_by_id(backtest_id: int):
    """
    Get a specific backtest result by ID

    Args:
        backtest_id: Backtest result ID

    Returns:
        Backtest result details
    """
    try:
        result = backtest_repository.get_backtest_result_by_id(backtest_id)
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Backtest result not found with ID {backtest_id}",
            )

        return {
            "status": "success",
            "data": result.to_dict() if hasattr(result, "to_dict") else vars(result),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching backtest result {backtest_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/strategies")
async def get_available_strategies():
    """
    Get list of available strategies for backtesting

    Returns:
        List of available strategies
    """
    try:
        # In a real implementation, this might come from a configuration
        strategies = ["random", "moving_average", "rsi", "breakout", "mean_reversion"]

        return {"status": "success", "strategies": strategies, "count": len(strategies)}
    except Exception as e:
        logger.error(f"Error fetching available strategies: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/results/{backtest_id}")
async def delete_backtest_result(backtest_id: int):
    """
    Delete a backtest result

    Args:
        backtest_id: Backtest result ID to delete

    Returns:
        Deletion confirmation
    """
    try:
        success = backtest_repository.delete_backtest_result(backtest_id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Backtest result not found with ID {backtest_id}",
            )

        return {
            "status": "success",
            "message": f"Backtest result {backtest_id} deleted successfully",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting backtest result {backtest_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
