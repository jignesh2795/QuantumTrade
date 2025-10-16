from typing import Optional, Dict, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import os
from backend.utils.logger import setup_logger

from backend.db.models import Order, OrderStatus, OrderType, OrderSide, Bot
from backend.core.exchange_base import ExchangeBase
from backend.core.event_bus import event_bus, EventTypes

logger = setup_logger(__name__)


class OrderManager:
    """Manages order creation, tracking, and lifecycle"""
    
    def __init__(self, db: AsyncSession, exchange: ExchangeBase):
        self.db = db
        self.exchange = exchange
        self.active_orders: Dict[str, Order] = {}
    
    async def create_order(
        self,
        bot_id: int,
        symbol: str,
        side: OrderSide,
        order_type: OrderType,
        quantity: float,
        price: Optional[float] = None,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        strategy_signal: Optional[str] = None,
    ) -> Order:
        """
        Create and submit an order
        
        Args:
            bot_id: Trading bot ID
            symbol: Trading pair (e.g., BTC/USDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Limit price (for LIMIT orders)
            stop_loss: Stop loss price
            take_profit: Take profit price
            strategy_signal: Signal that triggered the order
            
        Returns:
            Order object
        """
        try:
            # Get bot info
            result = await self.db.execute(
                select(Bot).where(Bot.id == bot_id)
            )
            bot = result.scalar_one_or_none()
            
            if not bot:
                raise ValueError(f"Bot {bot_id} not found")
            
            # Create order in database
            order = Order(
                bot_id=bot_id,
                exchange="binance",  # This should come from bot config
                symbol=symbol,
                order_type=order_type,
                side=side,
                quantity=quantity,
                price=price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                strategy_signal=strategy_signal,
                status=OrderStatus.PENDING,
            )
            
            self.db.add(order)
            await self.db.commit()
            await self.db.refresh(order)
            
            logger.info(f"Order created in DB: {order.id}")
            
            # Submit to exchange
            try:
                exchange_order = await self.exchange.create_order(
                    symbol=symbol,
                    side=side,
                    order_type=order_type,
                    quantity=quantity,
                    price=price,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                )
                
                # Update order with exchange info
                order.exchange_order_id = exchange_order['id']
                order.status = OrderStatus.FILLED if exchange_order['status'] == 'closed' else OrderStatus.PENDING
                
                if order.status == OrderStatus.FILLED:
                    order.filled_quantity = exchange_order.get('filled', quantity)
                    order.average_price = exchange_order.get('price', price)
                    order.filled_at = datetime.now()
                    order.total_cost = order.filled_quantity * order.average_price
                    order.fee = exchange_order.get('fee', {}).get('cost', 0)
                    order.fee_currency = exchange_order.get('fee', {}).get('currency', 'USDT')
                
                await self.db.commit()
                
                # Track active order
                if order.status == OrderStatus.PENDING:
                    self.active_orders[str(order.id)] = order
                
                # Emit event
                event_type = EventTypes.ORDER_FILLED if order.status == OrderStatus.FILLED else EventTypes.ORDER_CREATED
                await event_bus.emit(
                    event_type,
                    {
                        'order_id': order.id,
                        'exchange_order_id': order.exchange_order_id,
                        'bot_id': bot_id,
                        'symbol': symbol,
                        'side': side.value,
                        'quantity': quantity,
                        'price': order.average_price or price,
                        'status': order.status.value,
                    },
                    bot_id=bot_id
                )
                
                if os.name == 'nt':  # Windows
                    logger.info(f"Order submitted: {order.id} -> {order.exchange_order_id}")
                else:
                    logger.success(f"Order submitted: {order.id} -> {order.exchange_order_id}")
                
            except Exception as e:
                # Mark order as failed
                order.status = OrderStatus.FAILED
                order.notes = str(e)
                await self.db.commit()
                
                logger.error(f"Order submission failed: {e}")
                
                await event_bus.emit(
                    EventTypes.ORDER_FAILED,
                    {
                        'order_id': order.id,
                        'error': str(e),
                        'bot_id': bot_id,
                    },
                    bot_id=bot_id
                )
                
                raise
            
            return order
            
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise
    
    async def cancel_order(self, order_id: int) -> bool:
        """Cancel an order"""
        try:
            result = await self.db.execute(
                select(Order).where(Order.id == order_id)
            )
            order = result.scalar_one_or_none()
            
            if not order:
                logger.warning(f"Order {order_id} not found")
                return False
            
            if order.status != OrderStatus.PENDING:
                logger.warning(f"Cannot cancel order {order_id} with status {order.status}")
                return False
            
            # Cancel on exchange
            success = await self.exchange.cancel_order(
                order.exchange_order_id,
                order.symbol
            )
            
            if success:
                order.status = OrderStatus.CANCELLED
                await self.db.commit()
                
                # Remove from active orders
                self.active_orders.pop(str(order.id), None)
                
                await event_bus.emit(
                    EventTypes.ORDER_CANCELLED,
                    {
                        'order_id': order.id,
                        'bot_id': order.bot_id,
                    },
                    bot_id=order.bot_id
                )
                
                logger.info(f"Order cancelled: {order.id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            return False
    
    async def update_order_status(self, order_id: int):
        """Update order status from exchange"""
        try:
            result = await self.db.execute(
                select(Order).where(Order.id == order_id)
            )
            order = result.scalar_one_or_none()
            
            if not order or not order.exchange_order_id:
                return
            
            # Fetch from exchange
            exchange_order = await self.exchange.get_order_status(
                order.exchange_order_id,
                order.symbol
            )
            
            # Update order
            old_status = order.status
            
            if exchange_order['status'] == 'closed':
                order.status = OrderStatus.FILLED
                order.filled_quantity = exchange_order.get('filled', order.quantity)
                order.average_price = exchange_order.get('price', order.price)
                order.filled_at = datetime.now()
                order.total_cost = order.filled_quantity * order.average_price
                order.fee = exchange_order.get('fee', {}).get('cost', 0)
                
                self.active_orders.pop(str(order.id), None)
                
            elif exchange_order['status'] == 'canceled':
                order.status = OrderStatus.CANCELLED
                self.active_orders.pop(str(order.id), None)
            
            await self.db.commit()
            
            # Emit event if status changed
            if old_status != order.status:
                event_type = EventTypes.ORDER_FILLED if order.status == OrderStatus.FILLED else EventTypes.ORDER_CANCELLED
                await event_bus.emit(
                    event_type,
                    {
                        'order_id': order.id,
                        'bot_id': order.bot_id,
                        'status': order.status.value,
                    },
                    bot_id=order.bot_id
                )
            
        except Exception as e:
            logger.error(f"Error updating order status: {e}")
    
    async def check_active_orders(self):
        """Check status of all active orders"""
        for order_id in list(self.active_orders.keys()):
            order = self.active_orders[order_id]
            await self.update_order_status(order.id)
    
    async def get_bot_orders(
        self,
        bot_id: int,
        limit: int = 50,
        status: Optional[OrderStatus] = None
    ) -> List[Order]:
        """Get orders for a bot"""
        try:
            query = select(Order).where(Order.bot_id == bot_id)
            
            if status:
                query = query.where(Order.status == status)
            
            query = query.order_by(Order.created_at.desc()).limit(limit)
            
            result = await self.db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error fetching bot orders: {e}")
            return []
    
    async def get_order(self, order_id: int) -> Optional[Order]:
        """Get a specific order"""
        try:
            result = await self.db.execute(
                select(Order).where(Order.id == order_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error fetching order: {e}")
            return None


__all__ = ["OrderManager"]