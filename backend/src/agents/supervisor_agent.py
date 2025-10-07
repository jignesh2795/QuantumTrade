"""
Supervisor agent for QuantumTrade platform.
Orchestrates all agents (meta controller) implementation.
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent
from .strategy_agent import StrategyAgent
from .risk_agent import RiskAgent
from .performance_agent import PerformanceAgent
from .data_agent import DataAgent
from ..core.utils import format_response


class SupervisorAgent(BaseAgent):
    """Supervisor agent that orchestrates all other agents."""

    def __init__(self):
        super().__init__("supervisor_agent")
        self.agents = {}
        self.initialize_agents()

    def initialize_agents(self):
        """Initialize all subordinate agents."""
        self.agents["strategy"] = StrategyAgent("BTCUSDT")
        self.agents["risk"] = RiskAgent()
        self.agents["performance"] = PerformanceAgent()
        self.agents["data"] = DataAgent()

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate analysis across all agents."""
        results = {}

        # Run analysis on each agent
        for name, agent in self.agents.items():
            try:
                results[name] = agent.analyze(data)
            except Exception as e:
                results[name] = {"error": str(e)}

        return {
            "supervisor_analysis": "completed",
            "agent_results": results,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        }

    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate predictions across all agents."""
        results = {}

        # Run predictions on each agent
        for name, agent in self.agents.items():
            try:
                results[name] = agent.predict(data)
            except Exception as e:
                results[name] = {"error": str(e)}

        return {
            "supervisor_prediction": "completed",
            "agent_predictions": results,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        }

    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate execution across all agents."""
        results = {}

        # Execute action on each agent
        for name, agent in self.agents.items():
            try:
                results[name] = agent.execute(action)
            except Exception as e:
                results[name] = {"error": str(e)}

        return format_response(
            {
                "supervisor_execution": "completed",
                "agent_executions": results,
                "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
            }
        )

    def run_trading_cycle(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run a complete trading cycle through all agents."""
        try:
            # 1. Data agent processes market data
            processed_data = self.agents["data"].preprocess_data(market_data)

            # 2. Strategy agent generates signals
            strategy_signal = self.agents["strategy"].generate_signal(processed_data)

            # 3. Risk agent assesses risk
            risk_assessment = self.agents["risk"].assess_risk(
                position_size=1000,  # Mock position size
                account_balance=10000,  # Mock account balance
            )

            # 4. If risk is acceptable, execute trade
            execution_result = None
            if not risk_assessment.get("is_risky", True):
                execution_result = self.agents["strategy"].execute(strategy_signal)
                # Add to performance tracking
                self.agents["performance"].add_trade(
                    {
                        "symbol": strategy_signal.get("symbol"),
                        "action": strategy_signal.get("signal"),
                        "pnl": (
                            100 if strategy_signal.get("signal") == "BUY" else -50
                        ),  # Mock PnL
                    }
                )

            # 5. Get performance metrics
            performance_report = self.agents["performance"].get_performance_report()

            return format_response(
                {
                    "cycle": "completed",
                    "strategy_signal": strategy_signal,
                    "risk_assessment": risk_assessment,
                    "execution_result": execution_result,
                    "performance_report": performance_report,
                    "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
                }
            )
        except Exception as e:
            return format_response({"error": str(e)}, status="error")

    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        status = {}
        for name, agent in self.agents.items():
            status[name] = {
                "name": agent.name,
                "is_trained": getattr(agent, "is_trained", False),
                "status": "active",
            }

        return format_response({"supervisor": self.name, "agents": status})

    def add_agent(self, name: str, agent: BaseAgent):
        """Add a new agent to the supervisor."""
        self.agents[name] = agent

    def remove_agent(self, name: str):
        """Remove an agent from the supervisor."""
        if name in self.agents:
            del self.agents[name]
