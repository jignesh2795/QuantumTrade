"""
Strategy service for QuantumTrade backend.
Handles AI agent strategy trainer/executor.
"""

from typing import Dict, Any
from ..agents.strategy_agent import StrategyAgent
from ..core.utils import format_response


class StrategyService:
    """Service for handling AI agent strategy trainer/executor."""

    def __init__(self):
        self.agents = {}

    def create_strategy_agent(
        self, symbol: str, model_name: str = None
    ) -> StrategyAgent:
        """Create a new strategy agent for a symbol."""
        agent = StrategyAgent(symbol, model_name)
        self.agents[symbol] = agent
        return agent

    def get_strategy_agent(self, symbol: str) -> StrategyAgent:
        """Get an existing strategy agent for a symbol."""
        return self.agents.get(symbol)

    async def execute_strategy(self, symbol: str, data: Dict) -> Dict:
        """Execute a strategy for a symbol with given data."""
        agent = self.get_strategy_agent(symbol)
        if not agent:
            agent = self.create_strategy_agent(symbol)

        try:
            signal = agent.generate_signal(data)
            return format_response(
                {"symbol": symbol, "signal": signal, "timestamp": data.get("timestamp")}
            )
        except Exception as e:
            return format_response({"error": str(e)}, status="error")

    def list_agents(self) -> Dict:
        """List all active strategy agents."""
        return {"agents": list(self.agents.keys()), "count": len(self.agents)}


# Global strategy service instance
strategy_service = StrategyService()
