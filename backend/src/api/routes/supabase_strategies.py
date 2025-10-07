"""
Supabase Strategies API Routes for QuantumTrade Platform
Provides endpoints for strategy management using Supabase
"""

from fastapi import APIRouter, HTTPException, Query, Body, Header
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from ...database.supabase_crud import SupabaseCRUD

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/strategies", tags=["strategies"])

# Initialize Supabase CRUD
supabase_crud = SupabaseCRUD()


@router.get("/configurations")
async def get_strategy_configurations(
    user_id: str = Header(..., description="User ID")
):
    """
    Get all strategy configurations for a user

    Args:
        user_id: User ID (from header)

    Returns:
        List of strategy configurations
    """
    try:
        # Get strategy configurations from Supabase
        configurations = supabase_crud.get_strategy_configurations(user_id)

        return {
            "status": "success",
            "configurations": configurations,
            "count": len(configurations),
        }
    except Exception as e:
        logger.error(f"Error fetching strategy configurations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/configurations/{strategy_name}")
async def get_strategy_configuration(
    strategy_name: str, user_id: str = Header(..., description="User ID")
):
    """
    Get a specific strategy configuration for a user

    Args:
        strategy_name: Strategy name
        user_id: User ID (from header)

    Returns:
        Strategy configuration
    """
    try:
        # Get strategy configurations from Supabase
        configurations = supabase_crud.get_strategy_configurations(user_id)

        # Find the specific configuration
        configuration = next(
            (
                config
                for config in configurations
                if config.get("strategy_name") == strategy_name
            ),
            None,
        )

        if not configuration:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy configuration not found for {strategy_name}",
            )

        return {
            "status": "success",
            "configuration": configuration,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching strategy configuration {strategy_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/configurations")
async def update_strategy_configuration(
    user_id: str = Header(..., description="User ID"),
    strategy_name: str = Body(..., description="Strategy name"),
    asset: str = Body(..., description="Asset symbol"),
    is_active: bool = Body(True, description="Whether strategy is active"),
    config: Dict[str, Any] = Body({}, description="Configuration data"),
):
    """
    Update a strategy configuration for a user

    Args:
        user_id: User ID (from header)
        strategy_name: Strategy name
        asset: Asset symbol
        is_active: Whether strategy is active
        config: Configuration data

    Returns:
        Updated strategy configuration
    """
    try:
        # Update strategy configuration in Supabase
        configuration = supabase_crud.update_strategy_configuration(
            user_id=user_id,
            strategy_name=strategy_name,
            asset=asset,
            is_active=is_active,
            config=config,
        )

        if not configuration:
            raise HTTPException(
                status_code=500, detail="Error updating strategy configuration"
            )

        logger.info(f"Updated strategy configuration: {strategy_name} for {asset}")

        return {
            "status": "success",
            "message": f"Strategy configuration updated successfully",
            "configuration": configuration,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating strategy configuration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/execute")
async def execute_strategy(
    user_id: str = Header(..., description="User ID"),
    strategy_name: str = Body(..., description="Strategy name"),
    asset: str = Body(..., description="Asset symbol"),
    signal: str = Body(..., description="Trade signal (BUY, SELL, HOLD)"),
    confidence: float = Body(
        ..., description="Signal confidence (0.0 - 1.0)", ge=0.0, le=1.0
    ),
):
    """
    Execute a strategy signal and store in Supabase

    Args:
        user_id: User ID (from header)
        strategy_name: Strategy name
        asset: Asset symbol
        signal: Trade signal (BUY, SELL, HOLD)
        confidence: Signal confidence (0.0 - 1.0)

    Returns:
        Strategy execution result
    """
    try:
        # Validate signal
        if signal.upper() not in ["BUY", "SELL", "HOLD"]:
            raise HTTPException(
                status_code=400, detail="Signal must be BUY, SELL, or HOLD"
            )

        # Create strategy execution in Supabase
        execution = supabase_crud.create_strategy_execution(
            user_id=user_id,
            strategy_name=strategy_name,
            asset=asset,
            signal=signal.upper(),
            confidence=confidence,
        )

        if not execution:
            raise HTTPException(
                status_code=500, detail="Error saving strategy execution to Supabase"
            )

        logger.info(
            f"Executed strategy: {strategy_name} {asset} {signal} ({confidence})"
        )

        return {
            "status": "success",
            "message": f"Strategy executed successfully",
            "execution": execution,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing strategy: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/executions")
async def get_strategy_executions(
    user_id: str = Header(..., description="User ID"),
    strategy_name: Optional[str] = Query(None, description="Filter by strategy name"),
    asset: Optional[str] = Query(None, description="Filter by asset symbol"),
    limit: int = Query(
        100, description="Maximum number of executions to return", ge=1, le=1000
    ),
):
    """
    Get strategy executions for a user

    Args:
        user_id: User ID (from header)
        strategy_name: Filter by strategy name (optional)
        asset: Filter by asset symbol (optional)
        limit: Maximum number of executions to return (1-1000)

    Returns:
        List of strategy executions
    """
    try:
        # In a real implementation, you would query the strategy_executions table
        # For now, we'll return an empty list as a placeholder
        executions = []

        # Filter by strategy_name if provided
        if strategy_name:
            executions = [
                exec
                for exec in executions
                if exec.get("strategy_name") == strategy_name
            ]

        # Filter by asset if provided
        if asset:
            executions = [exec for exec in executions if exec.get("asset") == asset]

        # Apply limit
        executions = executions[:limit] if executions else []

        return {
            "status": "success",
            "executions": executions,
            "count": len(executions),
        }
    except Exception as e:
        logger.error(f"Error fetching strategy executions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
