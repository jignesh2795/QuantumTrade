"""
Base agent for QuantumTrade platform.
Abstract agent interface for all trading agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):
    """Abstract base class for all trading agents."""

    def __init__(self, name: str):
        self.name = name
        self.is_trained = False

    @abstractmethod
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data and return insights."""
        pass

    @abstractmethod
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions based on data."""
        pass

    @abstractmethod
    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action."""
        pass

    def train(self, training_data: Dict[str, Any]) -> Dict[str, Any]:
        """Train the agent with provided data."""
        # Default implementation - override in subclasses
        self.is_trained = True
        return {"status": "trained", "agent": self.name}

    def reset(self):
        """Reset agent state."""
        self.is_trained = False
