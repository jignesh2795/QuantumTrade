"""
AgentX - Execution Agent
Handles order execution and routing
"""
from typing import Dict, Any, List, Optional
from backend.ai_agents.base_agent import BaseAgent, Signal
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class AgentXExecutor(BaseAgent):
    """
    AgentX - Execution Agent
    
    Responsibilities:
    - Order execution optimization
    - Smart order routing
    - Slippage prediction
    - Fill rate optimization
    """
    
    def __init__(self):
        super().__init__(name="AgentX", agent_type="execution")
        self.execution_history = []
        self.avg_slippage = 0.0
        self.fill_rate = 1.0
        self.total_executions = 0
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze execution conditions and optimize order placement
        
        Args:
            data: Contains order details, market conditions
            
        Returns:
            Execution plan with optimized parameters
        """
        self.update_timestamp()
        
        order_type = data.get('order_type', 'market')
        symbol = data.get('symbol')
        quantity = data.get('quantity')
        side = data.get('side')
        current_price = data.get('current_price')
        
        # Predict slippage based on market conditions
        predicted_slippage = self._predict_slippage(data)
        
        # Calculate optimal execution price
        optimal_price = self._calculate_optimal_price(
            current_price, 
            predicted_slippage, 
            side
        )
        
        # Determine execution strategy
        execution_strategy = self._determine_execution_strategy(data)
        
        result = {
            "agent": self.name,
            "execution_ready": True,
            "order_type": order_type,
            "predicted_slippage": predicted_slippage,
            "optimal_price": optimal_price,
            "execution_strategy": execution_strategy,
            "confidence": 0.85,
            "recommendation": f"Execute {side} {quantity} {symbol} @ ~${optimal_price:.2f}"
        }
        
        logger.info(
            f"🤖 AgentX: {execution_strategy} execution | "
            f"Predicted slippage: {predicted_slippage*100:.3f}%"
        )
        
        return result
    
    def _predict_slippage(self, data: Dict[str, Any]) -> float:
        """
        Predict order slippage based on market conditions
        
        Factors:
        - Order size vs average volume
        - Market volatility
        - Spread
        - Time of day
        """
        quantity = data.get('quantity', 0)
        avg_volume = data.get('avg_volume', 1000)
        volatility = data.get('volatility', 0.02)
        spread = data.get('spread', 0.001)
        
        # Calculate size impact
        size_ratio = quantity / avg_volume
        size_impact = size_ratio * 0.01  # 1% per 100% of avg volume
        
        # Volatility impact
        volatility_impact = volatility * 0.5
        
        # Spread impact
        spread_impact = spread
        
        # Combined slippage prediction
        predicted_slippage = size_impact + volatility_impact + spread_impact
        
        # Update running average
        self.avg_slippage = (self.avg_slippage * 0.9) + (predicted_slippage * 0.1)
        
        return min(predicted_slippage, 0.01)  # Cap at 1%
    
    def _calculate_optimal_price(
        self, 
        current_price: float, 
        slippage: float, 
        side: str
    ) -> float:
        """Calculate optimal execution price accounting for slippage"""
        if side.lower() == "buy":
            return current_price * (1 + slippage)
        else:
            return current_price * (1 - slippage)
    
    def _determine_execution_strategy(self, data: Dict[str, Any]) -> str:
        """
        Determine best execution strategy
        
        Strategies:
        - AGGRESSIVE: Market order, immediate execution
        - PASSIVE: Limit order, wait for better price
        - TWAP: Time-weighted average price (future)
        - VWAP: Volume-weighted average price (future)
        """
        urgency = data.get('urgency', 'normal')
        market_condition = data.get('market_condition', 'normal')
        
        if urgency == 'high' or market_condition == 'volatile':
            return "AGGRESSIVE"
        elif market_condition == 'calm':
            return "PASSIVE"
        else:
            return "BALANCED"
    
    def record_execution(self, order_data: Dict[str, Any]):
        """Record execution for learning"""
        self.execution_history.append({
            "timestamp": self.last_update,
            "order": order_data,
            "slippage": order_data.get('actual_slippage', 0),
            "filled": order_data.get('filled', True)
        })
        
        self.total_executions += 1
        
        # Keep only last 100 executions
        if len(self.execution_history) > 100:
            self.execution_history.pop(0)
        
        # Update fill rate
        filled_orders = sum(1 for e in self.execution_history if e['filled'])
        self.fill_rate = filled_orders / len(self.execution_history)
    
    def get_status(self) -> Dict[str, Any]:
        """Get AgentX status"""
        return {
            "name": self.name,
            "type": self.agent_type,
            "active": self.is_active,
            "last_update": self.last_update.isoformat(),
            "total_executions": self.total_executions,
            "avg_slippage": self.avg_slippage,
            "fill_rate": self.fill_rate,
            "execution_history_size": len(self.execution_history)
        }