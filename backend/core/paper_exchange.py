"""
Paper trading exchange simulator
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid
from backend.core.exchange_base import ExchangeBase, Candle, OrderResult
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class PaperExchange(ExchangeBase):
    """
    Paper trading exchange that simulates real trading
    without actual money
    """
    
    def __init__(self, initial_capital: float = 10000):
        super().__init__()
        self.initial_capital = initial_capital
        self.cash_balance = initial_capital
        self.positions: Dict[str, Dict] = {}
        self.orders: Dict[str, OrderResult] = {}
        self.trade_history: List[OrderResult] = []
        
        # Price simulation
        self.current_prices: Dict[str, float] = {}
        self.price_history: Dict[str, List[Candle]] = {}
        
    async def connect(self) -> bool:
        """Connect to paper exchange"""
        logger.info("📝 Connecting to Paper Trading Exchange")
        self.is_connected = True
        
        # Initialize with a realistic starting price
        self.current_prices["BTCUSDT"] = 43000.0
        logger.info(f"✅ Paper exchange connected | Initial capital: ${self.initial_capital:,.2f}")
        return True
    
    async def disconnect(self):
        """Disconnect from paper exchange"""
        self.is_connected = False
        logger.info("Paper exchange disconnected")
    
    async def get_current_price(self, symbol: str) -> float:
        """Get current simulated price"""
        if symbol not in self.current_prices:
            self.current_prices[symbol] = 100.0
        
        # Small random walk ±0.2% per cycle
        import random
        current = self.current_prices[symbol]
        change_pct = random.uniform(-0.002, 0.002)
        new_price = current * (1 + change_pct)
        self.current_prices[symbol] = new_price
        return new_price
    
    async def get_candles(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 100
    ) -> List[Candle]:
        """Get simulated historical candles"""
        if symbol not in self.price_history or len(self.price_history[symbol]) < limit:
            candles = []
            base_price = self.current_prices.get(symbol, 100.0)
            now = datetime.utcnow()
            
            # Initialize first 'slow_period' candles exactly at current price for realistic SMA
            slow_period = 30  # Default slow period
            for i in range(slow_period):
                timestamp = now - timedelta(hours=slow_period - i)
                candles.append(Candle(
                    timestamp=timestamp,
                    open=base_price,
                    high=base_price,
                    low=base_price,
                    close=base_price,
                    volume=1000
                ))
            
            # Generate remaining candles with small random walk ±0.5%
            for i in range(slow_period, limit):
                timestamp = now - timedelta(hours=limit - i)
                import random
                change = random.uniform(-0.005, 0.005)  # ±0.5% per candle
                open_price = base_price * (1 + change)
                high = open_price * (1 + abs(random.uniform(0, 0.002)))
                low = open_price * (1 - abs(random.uniform(0, 0.002)))
                close = (high + low) / 2
                volume = random.uniform(1000, 5000)
                
                candles.append(Candle(
                    timestamp=timestamp,
                    open=open_price,
                    high=high,
                    low=low,
                    close=close,
                    volume=volume
                ))
                
                base_price = close
            
            self.price_history[symbol] = candles
            return candles[-limit:]
        
        return self.price_history[symbol][-limit:]
    
    async def place_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: Optional[float] = None,
        order_type: str = "market"
    ) -> OrderResult:
        """Place a simulated order"""
        order_id = f"PAPER_{uuid.uuid4().hex[:8]}"
        
        if order_type == "market" or price is None:
            execution_price = await self.get_current_price(symbol)
        else:
            execution_price = price
        
        order_value = quantity * execution_price
        
        if side.lower() == "buy":
            if order_value > self.cash_balance:
                logger.warning(f"❌ Insufficient balance for order | Need: ${order_value:,.2f}, Have: ${self.cash_balance:,.2f}")
                return OrderResult(
                    order_id=order_id,
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    price=execution_price,
                    status="rejected",
                    timestamp=datetime.utcnow()
                )
            
            self.cash_balance -= order_value
            if symbol not in self.positions:
                self.positions[symbol] = {"quantity": 0, "avg_price": 0}
            
            pos = self.positions[symbol]
            total_quantity = pos["quantity"] + quantity
            pos["avg_price"] = ((pos["avg_price"] * pos["quantity"]) + order_value) / total_quantity
            pos["quantity"] = total_quantity
            
        else:  # sell
            if symbol not in self.positions or self.positions[symbol]["quantity"] < quantity:
                logger.warning(f"❌ Insufficient position for sell | Need: {quantity}, Have: {self.positions.get(symbol, {}).get('quantity', 0)}")
                return OrderResult(
                    order_id=order_id,
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    price=execution_price,
                    status="rejected",
                    timestamp=datetime.utcnow()
                )
            
            self.cash_balance += order_value
            self.positions[symbol]["quantity"] -= quantity
            if self.positions[symbol]["quantity"] <= 0:
                del self.positions[symbol]
        
        result = OrderResult(
            order_id=order_id,
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=execution_price,
            status="filled",
            filled_quantity=quantity,
            avg_fill_price=execution_price,
            timestamp=datetime.utcnow()
        )
        
        self.orders[order_id] = result
        self.trade_history.append(result)
        
        logger.info(
            f"✅ Paper order executed | {side.upper()} {quantity} {symbol} @ ${execution_price:,.2f} | "
            f"Balance: ${self.cash_balance:,.2f}"
        )
        return result
    
    async def cancel_order(self, order_id: str, symbol: str) -> bool:
        if order_id in self.orders:
            self.orders[order_id].status = "cancelled"
            return True
        return False
    
    async def get_order_status(self, order_id: str, symbol: str) -> OrderResult:
        return self.orders.get(order_id)
    
    async def get_balance(self) -> Dict[str, float]:
        total_value = self.cash_balance
        for symbol, pos in self.positions.items():
            current_price = await self.get_current_price(symbol)
            total_value += pos["quantity"] * current_price
        
        return {
            "cash": self.cash_balance,
            "total": total_value,
            "pnl": total_value - self.initial_capital,
            "pnl_pct": ((total_value - self.initial_capital) / self.initial_capital) * 100
        }
    
    async def get_positions(self) -> List[Dict]:
        positions = []
        for symbol, pos in self.positions.items():
            current_price = await self.get_current_price(symbol)
            position_value = pos["quantity"] * current_price
            cost_basis = pos["quantity"] * pos["avg_price"]
            pnl = position_value - cost_basis
            
            positions.append({
                "symbol": symbol,
                "quantity": pos["quantity"],
                "avg_price": pos["avg_price"],
                "current_price": current_price,
                "value": position_value,
                "pnl": pnl,
                "pnl_pct": (pnl / cost_basis) * 100 if cost_basis > 0 else 0
            })
        return positions