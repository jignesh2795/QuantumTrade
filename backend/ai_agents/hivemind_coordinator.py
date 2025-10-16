"""
HiveMind - Coordinator Agent
Aggregates signals and makes final decisions
"""
from typing import Dict, Any, List
import numpy as np
from backend.ai_agents.base_agent import BaseAgent, Signal
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class HiveMindCoordinator(BaseAgent):
    """
    HiveMind - Coordinator Agent
    
    Responsibilities:
    - Aggregate signals from all agents
    - Resolve conflicts
    - Make final trading decisions
    - Calibrate agent weights
    """
    
    def __init__(self):
        super().__init__(name="HiveMind", agent_type="coordinator")
        
        # Agent weights (how much to trust each agent)
        self.agent_weights = {
            "AgentX": 0.25,
            "Guard": 0.30,
            "Optima": 0.20,
            "Strategy": 0.25
        }
        
        self.decision_history = []
        self.consensus_threshold = 0.6
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate signals and make final decision
        
        Args:
            data: Contains signals from all agents
            
        Returns:
            Final trading decision
        """
        self.update_timestamp()
        
        signals = data.get('signals', [])
        
        if not signals:
            return {
                "agent": self.name,
                "decision": "hold",
                "confidence": 0.0,
                "reason": "No signals received"
            }
        
        # Aggregate signals
        decision = self._aggregate_signals(signals)
        
        # Record decision
        self._record_decision(decision, signals)
        
        logger.info(
            f"🤖 HiveMind: {decision['decision'].upper()} | "
            f"Confidence: {decision['confidence']:.2%} | "
            f"Consensus: {decision.get('consensus', 0):.2%}"
        )
        
        return decision
    
    def _aggregate_signals(self, signals: List[Signal]) -> Dict[str, Any]:
        """
        Aggregate signals using weighted voting
        
        Algorithm:
        1. Weight each signal by agent weight and confidence
        2. Calculate consensus score for each action
        3. Choose action with highest consensus
        4. Apply consensus threshold
        """
        # Count votes for each action
        votes = {"buy": 0.0, "sell": 0.0, "hold": 0.0}
        
        for signal in signals:
            agent_name = signal.agent_name
            action = signal.action.lower()
            confidence = signal.confidence
            
            # Get agent weight
            weight = self.agent_weights.get(agent_name, 0.1)
            
            # Weighted vote
            vote_power = weight * confidence
            votes[action] += vote_power
        
        # Normalize votes
        total_votes = sum(votes.values())
        if total_votes > 0:
            for action in votes:
                votes[action] /= total_votes
        
        # Choose action with highest consensus
        best_action = max(votes, key=votes.get)
        consensus = votes[best_action]
        
        # Apply consensus threshold
        if consensus < self.consensus_threshold:
            best_action = "hold"
            reason = f"Low consensus ({consensus:.2%} < {self.consensus_threshold:.2%})"
        else:
            # Find reasons from supporting signals
            reasons = [
                s.reason for s in signals 
                if s.action.lower() == best_action
            ]
            reason = " | ".join(reasons[:2])  # Top 2 reasons
        
        return {
            "agent": self.name,
            "decision": best_action,
            "confidence": consensus,
            "consensus": consensus,
            "votes": votes,
            "reason": reason,
            "signals_count": len(signals)
        }
    
    def _record_decision(self, decision: Dict, signals: List[Signal]):
        """Record decision for learning"""
        self.decision_history.append({
            "timestamp": self.last_update,
            "decision": decision,
            "signals": [s.to_dict() for s in signals]
        })
        
        # Keep last 500 decisions
        if len(self.decision_history) > 500:
            self.decision_history.pop(0)
    
    def update_agent_weight(self, agent_name: str, weight: float):
        """Update trust weight for an agent"""
        weight = max(0.0, min(1.0, weight))
        self.agent_weights[agent_name] = weight
        
        # Normalize weights
        total = sum(self.agent_weights.values())
        if total > 0:
            for agent in self.agent_weights:
                self.agent_weights[agent] /= total
        
        logger.info(f"⚖️  Updated {agent_name} weight to {weight:.2%}")
    
    def calibrate_weights(self, performance_data: Dict[str, float]):
        """
        Calibrate agent weights based on performance
        
        Args:
            performance_data: Dict of agent_name -> accuracy/performance score
        """
        logger.info("🎯 Calibrating agent weights...")
        
        for agent_name, performance in performance_data.items():
            if agent_name in self.agent_weights:
                # Adjust weight based on performance
                current_weight = self.agent_weights[agent_name]
                adjustment = (performance - 0.5) * 0.1  # ±10% based on performance
                new_weight = current_weight + adjustment
                self.update_agent_weight(agent_name, new_weight)
    
    def get_status(self) -> Dict[str, Any]:
        """Get HiveMind status"""
        return {
            "name": self.name,
            "type": self.agent_type,
            "active": self.is_active,
            "last_update": self.last_update.isoformat(),
            "agent_weights": self.agent_weights,
            "consensus_threshold": self.consensus_threshold,
            "decisions_made": len(self.decision_history)
        }