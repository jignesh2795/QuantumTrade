"""
Portfolio Management Module for QuantumTrade Platform
Handles portfolio tracking, position management, and performance calculation
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Position:
    """Represents a trading position"""
    symbol: str
    size: float
    avg_price: float
    current_price: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
            
    @property
    def market_value(self) -> float:
        """Calculate market value of position"""
        return self.size * self.current_price
        
    @property
    def cost_basis(self) -> float:
        """Calculate cost basis of position"""
        return self.size * self.avg_price
        
    @property
    def unrealized_pnl(self) -> float:
        """Calculate unrealized profit/loss"""
        return self.market_value - self.cost_basis
        
    @property
    def unrealized_pnl_percent(self) -> float:
        """Calculate unrealized profit/loss percentage"""
        if self.cost_basis == 0:
            return 0.0
        return (self.unrealized_pnl / self.cost_basis) * 100
        
    def to_dict(self) -> Dict:
        """Convert position to dictionary"""
        return {
            "symbol": self.symbol,
            "size": self.size,
            "avg_price": self.avg_price,
            "current_price": self.current_price,
            "market_value": self.market_value,
            "cost_basis": self.cost_basis,
            "unrealized_pnl": self.unrealized_pnl,
            "unrealized_pnl_percent": self.unrealized_pnl_percent,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class PortfolioSummary:
    """Represents portfolio summary"""
    total_value: float
    cash_balance: float
    positions_value: float
    positions: List[Position]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
            
    @property
    def total_pnl(self) -> float:
        """Calculate total portfolio PnL"""
        return sum(pos.unrealized_pnl for pos in self.positions)
        
    @property
    def total_pnl_percent(self) -> float:
        """Calculate total portfolio PnL percentage"""
        if self.cash_balance == 0:
            return 0.0
        return (self.total_pnl / self.cash_balance) * 100
        
    def to_dict(self) -> Dict:
        """Convert portfolio summary to dictionary"""
        return {
            "total_value": self.total_value,
            "cash_balance": self.cash_balance,
            "positions_value": self.positions_value,
            "total_pnl": self.total_pnl,
            "total_pnl_percent": self.total_pnl_percent,
            "positions": [pos.to_dict() for pos in self.positions],
            "timestamp": self.timestamp.isoformat()
        }


class PortfolioManager:
    """Manages portfolio positions and performance"""
    
    def __init__(self, initial_cash: float = 10000.0):
        self.cash_balance = initial_cash
        self.positions: Dict[str, Position] = {}
        self.transaction_history: List[Dict] = []
        
    def add_position(self, symbol: str, size: float, price: float) -> Position:
        """Add or update a position"""
        try:
            if symbol in self.positions:
                # Update existing position
                position = self.positions[symbol]
                # Calculate new average price
                total_value = (position.size * position.avg_price) + (size * price)
                total_size = position.size + size
                new_avg_price = total_value / total_size if total_size != 0 else 0
                
                position.size = total_size
                position.avg_price = new_avg_price
                position.timestamp = datetime.utcnow()
            else:
                # Create new position
                position = Position(
                    symbol=symbol,
                    size=size,
                    avg_price=price
                )
                self.positions[symbol] = position
                
            # Update cash balance
            self.cash_balance -= size * price
            
            # Record transaction
            self.transaction_history.append({
                "type": "BUY" if size > 0 else "SELL",
                "symbol": symbol,
                "size": size,
                "price": price,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            logger.info(f"Position updated for {symbol}: {size} @ {price}")
            return position
            
        except Exception as e:
            logger.error(f"Error adding position for {symbol}: {e}")
            return None
            
    def close_position(self, symbol: str, price: float) -> Optional[Position]:
        """Close a position"""
        try:
            if symbol not in self.positions:
                logger.warning(f"No position found for {symbol}")
                return None
                
            position = self.positions[symbol]
            size = -position.size  # Close entire position
            
            # Update cash balance
            self.cash_balance -= size * price  # size is negative, so this adds cash
            
            # Remove position
            del self.positions[symbol]
            
            # Record transaction
            self.transaction_history.append({
                "type": "SELL",
                "symbol": symbol,
                "size": size,
                "price": price,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            logger.info(f"Position closed for {symbol}: {size} @ {price}")
            return position
            
        except Exception as e:
            logger.error(f"Error closing position for {symbol}: {e}")
            return None
            
    def update_position_prices(self, prices: Dict[str, float]) -> None:
        """Update current prices for all positions"""
        try:
            for symbol, price in prices.items():
                if symbol in self.positions:
                    self.positions[symbol].current_price = price
                    
        except Exception as e:
            logger.error(f"Error updating position prices: {e}")
            
    def get_position(self, symbol: str) -> Optional[Position]:
        """Get a specific position"""
        return self.positions.get(symbol)
        
    def get_all_positions(self) -> List[Position]:
        """Get all positions"""
        return list(self.positions.values())
        
    def get_portfolio_summary(self, current_prices: Dict[str, float] = None) -> PortfolioSummary:
        """Get portfolio summary"""
        try:
            # Update prices if provided
            if current_prices:
                self.update_position_prices(current_prices)
                
            # Calculate positions value
            positions_value = sum(pos.market_value for pos in self.positions.values())
            
            # Total portfolio value
            total_value = self.cash_balance + positions_value
            
            # Create portfolio summary
            summary = PortfolioSummary(
                total_value=total_value,
                cash_balance=self.cash_balance,
                positions_value=positions_value,
                positions=list(self.positions.values())
            )
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating portfolio summary: {e}")
            return None
            
    def get_transaction_history(self, limit: int = 50) -> List[Dict]:
        """Get recent transaction history"""
        return self.transaction_history[-limit:]