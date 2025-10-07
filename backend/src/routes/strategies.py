"""
Strategy routes for QuantumTrade backend.
API endpoints for strategy configuration.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models.strategy import Strategy
from ..core.database import get_db
from ..core.utils import format_response

router = APIRouter(prefix="/strategies", tags=["strategies"])


class StrategyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    is_active: bool = True


class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


@router.post("/", response_model=dict)
async def create_strategy(strategy: StrategyCreate, db=Depends(get_db)):
    """Create a new strategy."""
    try:
        new_strategy = Strategy(
            name=strategy.name,
            description=strategy.description,
            parameters=strategy.parameters,
            is_active=strategy.is_active,
        )

        db.add(new_strategy)
        db.commit()
        db.refresh(new_strategy)

        return format_response(
            {
                "id": new_strategy.id,
                "name": new_strategy.name,
                "description": new_strategy.description,
                "parameters": new_strategy.parameters,
                "is_active": new_strategy.is_active,
                "created_at": (
                    new_strategy.created_at.isoformat()
                    if new_strategy.created_at
                    else None
                ),
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=dict)
async def list_strategies(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    """List strategies."""
    try:
        strategies = db.query(Strategy).offset(skip).limit(limit).all()

        strategy_list = []
        for strategy in strategies:
            strategy_list.append(
                {
                    "id": strategy.id,
                    "name": strategy.name,
                    "description": strategy.description,
                    "parameters": strategy.parameters,
                    "is_active": strategy.is_active,
                    "created_at": (
                        strategy.created_at.isoformat() if strategy.created_at else None
                    ),
                }
            )

        return format_response(
            {"strategies": strategy_list, "count": len(strategy_list)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{strategy_id}", response_model=dict)
async def get_strategy(strategy_id: int, db=Depends(get_db)):
    """Get a specific strategy by ID."""
    try:
        strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
        if not strategy:
            raise HTTPException(status_code=404, detail="Strategy not found")

        return format_response(
            {
                "id": strategy.id,
                "name": strategy.name,
                "description": strategy.description,
                "parameters": strategy.parameters,
                "is_active": strategy.is_active,
                "created_at": (
                    strategy.created_at.isoformat() if strategy.created_at else None
                ),
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{strategy_id}", response_model=dict)
async def update_strategy(
    strategy_id: int, strategy: StrategyUpdate, db=Depends(get_db)
):
    """Update a strategy by ID."""
    try:
        db_strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
        if not db_strategy:
            raise HTTPException(status_code=404, detail="Strategy not found")

        # Update fields if provided
        if strategy.name is not None:
            db_strategy.name = strategy.name
        if strategy.description is not None:
            db_strategy.description = strategy.description
        if strategy.parameters is not None:
            db_strategy.parameters = strategy.parameters
        if strategy.is_active is not None:
            db_strategy.is_active = strategy.is_active

        db.commit()
        db.refresh(db_strategy)

        return format_response(
            {
                "id": db_strategy.id,
                "name": db_strategy.name,
                "description": db_strategy.description,
                "parameters": db_strategy.parameters,
                "is_active": db_strategy.is_active,
                "updated_at": (
                    db_strategy.updated_at.isoformat()
                    if db_strategy.updated_at
                    else None
                ),
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{strategy_id}", response_model=dict)
async def delete_strategy(strategy_id: int, db=Depends(get_db)):
    """Delete a strategy by ID."""
    try:
        strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
        if not strategy:
            raise HTTPException(status_code=404, detail="Strategy not found")

        db.delete(strategy)
        db.commit()

        return format_response({"message": "Strategy deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
