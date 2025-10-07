"""
Execution Agent for QuantumTrade Platform
Simulates trade execution with order book matching and trade logs
"""

import random
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class ExecutionAgent:
    """
    Simulates trade execution with order book matching and trade logs
    """

    def __init__(self):
        """Initialize ExecutionAgent"""
        self.order_book = {}  # symbol -> {bids: [], asks: []}
        self.trade_logs = []  # List of all executed trades
        self.order_id_counter = 1000

    def execute_trade(
        self, symbol: str, action: str, size: float, limit_price: float = None
    ) -> Dict:
        """
        Execute a trade with simulated order book matching

        Args:
            symbol: Trading symbol
            action: Trade action ("BUY" or "SELL")
            size: Trade size
            limit_price: Optional limit price for the order

        Returns:
            Dictionary with execution details
        """
        try:
            # Generate order ID
            order_id = self.order_id_counter
            self.order_id_counter += 1

            # Simulate market price
            market_price = self._get_market_price(symbol)

            # If no limit price specified, use market price with slippage
            if limit_price is None:
                if action.upper() == "BUY":
                    # For buy orders, we might pay slightly more (slippage)
                    limit_price = market_price * (1 + random.uniform(0, 0.005))
                else:
                    # For sell orders, we might receive slightly less (slippage)
                    limit_price = market_price * (1 - random.uniform(0, 0.005))

            # Simulate order execution
            execution_result = self._simulate_order_execution(
                symbol, action, size, limit_price
            )

            # Add order details
            execution_result["order_id"] = order_id
            execution_result["symbol"] = symbol
            execution_result["action"] = action.upper()
            execution_result["size"] = size
            execution_result["limit_price"] = round(limit_price, 2)
            execution_result["market_price"] = market_price
            execution_result["timestamp"] = datetime.utcnow().isoformat()

            # Calculate commission (0.1% of trade value)
            commission = abs(size * execution_result["price"] * 0.001)
            execution_result["commission"] = round(commission, 2)

            # Calculate slippage
            slippage = abs(execution_result["price"] - market_price)
            execution_result["slippage"] = round(slippage, 2)

            # Log the trade
            self.trade_logs.append(execution_result)

            # Keep only last 1000 trade logs
            if len(self.trade_logs) > 1000:
                self.trade_logs = self.trade_logs[-1000:]

            logger.info(
                f"Order executed: {symbol} {action} {size} @ {execution_result['price']}"
            )

            return execution_result

        except Exception as e:
            logger.error(f"Error executing trade for {symbol}: {e}")
            return {
                "status": "error",
                "message": f"Error executing trade: {str(e)}",
                "symbol": symbol,
                "action": action,
                "size": size,
            }

    def _get_market_price(self, symbol: str) -> float:
        """
        Get simulated market price for a symbol

        Args:
            symbol: Trading symbol

        Returns:
            Simulated market price
        """
        try:
            # Base prices for different symbols
            base_prices = {
                "BTC-USD": 30000,
                "ETH-USD": 2000,
                "SOL-USD": 25,
                "AAPL": 150,
                "GOOGL": 2500,
                "TSLA": 200,
            }

            base_price = base_prices.get(symbol, 100.0)

            # Add some random volatility
            volatility = 0.005  # 0.5% volatility
            random_factor = 1 + random.uniform(-volatility, volatility)

            return round(base_price * random_factor, 2)
        except Exception as e:
            logger.error(f"Error getting market price for {symbol}: {e}")
            return 100.0

    def _simulate_order_execution(
        self, symbol: str, action: str, size: float, limit_price: float
    ) -> Dict:
        """
        Simulate order execution with order book matching

        Args:
            symbol: Trading symbol
            action: Trade action
            size: Trade size
            limit_price: Limit price

        Returns:
            Dictionary with execution details
        """
        try:
            # Simulate order book depth
            order_book_depth = random.randint(5, 20)

            # Simulate execution based on order book depth
            fill_probability = min(1.0, order_book_depth / 20.0)

            if random.random() > fill_probability:
                return {
                    "status": "rejected",
                    "message": "Order not filled due to insufficient liquidity",
                    "price": 0.0,
                    "filled_size": 0.0,
                }

            # Simulate partial fills
            fill_ratio = random.uniform(0.5, 1.0)
            filled_size = size * fill_ratio

            # Simulate execution price based on limit price and market conditions
            if action.upper() == "BUY":
                # For buy orders, execution price might be slightly higher than limit
                execution_price = limit_price * random.uniform(1.0, 1.001)
            else:
                # For sell orders, execution price might be slightly lower than limit
                execution_price = limit_price * random.uniform(0.999, 1.0)

            return {
                "status": "filled" if fill_ratio == 1.0 else "partially_filled",
                "message": "Order executed successfully",
                "price": round(execution_price, 2),
                "filled_size": round(filled_size, 4),
                "remaining_size": round(size - filled_size, 4),
            }
        except Exception as e:
            logger.error(f"Error simulating order execution for {symbol}: {e}")
            return {
                "status": "error",
                "message": "Error in order execution simulation",
                "price": 0.0,
                "filled_size": 0.0,
            }

    def get_trade_logs(self, limit: int = 50) -> List[Dict]:
        """
        Get recent trade logs

        Args:
            limit: Maximum number of logs to return

        Returns:
            List of recent trade logs
        """
        try:
            return self.trade_logs[-limit:]
        except Exception as e:
            logger.error(f"Error getting trade logs: {e}")
            return []

    def get_order_book(self, symbol: str) -> Dict:
        """
        Get simulated order book for a symbol

        Args:
            symbol: Trading symbol

        Returns:
            Dictionary with order book data
        """
        try:
            # Generate simulated order book
            bids = []
            asks = []

            market_price = self._get_market_price(symbol)

            # Generate 5 levels of bids and asks
            for i in range(1, 6):
                # Bids (lower than market price)
                bid_price = market_price * (1 - (i * 0.001))
                bid_size = random.randint(1, 100)
                bids.append({"price": round(bid_price, 2), "size": bid_size})

                # Asks (higher than market price)
                ask_price = market_price * (1 + (i * 0.001))
                ask_size = random.randint(1, 100)
                asks.append({"price": round(ask_price, 2), "size": ask_size})

            return {
                "symbol": symbol,
                "bids": bids,
                "asks": asks,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error getting order book for {symbol}: {e}")
            return {"symbol": symbol, "bids": [], "asks": [], "error": str(e)}

    def cancel_order(self, order_id: int) -> Dict:
        """
        Cancel an order (simulated)

        Args:
            order_id: Order ID to cancel

        Returns:
            Dictionary with cancellation result
        """
        try:
            # In a real implementation, we would check if the order exists
            # For simulation, we'll just return success
            return {
                "status": "success",
                "message": f"Order {order_id} cancelled",
                "order_id": order_id,
            }
        except Exception as e:
            logger.error(f"Error cancelling order {order_id}: {e}")
            return {
                "status": "error",
                "message": f"Error cancelling order: {str(e)}",
                "order_id": order_id,
            }
