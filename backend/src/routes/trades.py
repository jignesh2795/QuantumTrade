"""
Trade routes for QuantumTrade backend.
API endpoints for trade CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..models.trade import Trade
from ..core.database import get_db
from ..core.utils import format_response

router = APIRouter(prefix="/trades", tags=["trades"])


class TradeCreate(BaseModel):
    symbol: str
    side: str
    quantity: float
    price: float
    strategy_id: Optional[int] = None


class TradeResponse(BaseModel):
    id: int
    symbol: str
    side: str
    quantity: float
    price: float
    timestamp: datetime
    strategy_id: Optional[int] = None


@router.post("/", response_model=dict)
async def create_trade(trade: TradeCreate, db=Depends(get_db)):
    """Create a new trade."""
    try:
        new_trade = Trade(
            symbol=trade.symbol,
            side=trade.side,
            quantity=trade.quantity,
            price=trade.price,
            strategy_id=trade.strategy_id,
        )

        db.add(new_trade)
        db.commit()
        db.refresh(new_trade)

        return format_response(
            {
                "id": new_trade.id,
                "symbol": new_trade.symbol,
                "side": new_trade.side,
                "quantity": new_trade.quantity,
                "price": new_trade.price,
                "timestamp": new_trade.timestamp.isoformat(),
                "strategy_id": new_trade.strategy_id,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=dict)
async def list_trades(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    """List trades."""
    try:
        trades = db.query(Trade).offset(skip).limit(limit).all()

        trade_list = []
        for trade in trades:
            trade_list.append(
                {
                    "id": trade.id,
                    "symbol": trade.symbol,
                    "side": trade.side,
                    "quantity": trade.quantity,
                    "price": trade.price,
                    "timestamp": (
                        trade.timestamp.isoformat() if trade.timestamp else None
                    ),
                    "strategy_id": trade.strategy_id,
                }
            )

        return format_response({"trades": trade_list, "count": len(trade_list)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{trade_id}", response_model=dict)
async def get_trade(trade_id: int, db=Depends(get_db)):
    """Get a specific trade by ID."""
    try:
        trade = db.query(Trade).filter(Trade.id == trade_id).first()
        if not trade:
            raise HTTPException(status_code=404, detail="Trade not found")

        return format_response(
            {
                "id": trade.id,
                "symbol": trade.symbol,
                "side": trade.side,
                "quantity": trade.quantity,
                "price": trade.price,
                "timestamp": trade.timestamp.isoformat() if trade.timestamp else None,
                "strategy_id": trade.strategy_id,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{trade_id}", response_model=dict)
async def delete_trade(trade_id: int, db=Depends(get_db)):
    """Delete a trade by ID."""
    try:
        trade = db.query(Trade).filter(Trade.id == trade_id).first()
        if not trade:
            raise HTTPException(status_code=404, detail="Trade not found")

        db.delete(trade)
        db.commit()

        return format_response({"message": "Trade deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
