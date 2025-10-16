"""
Base Agent Class
All AI agents inherit from this base class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseAgent(ABC):
    """
    Base class for all AI agents
    
    All agents must implement:
    - analyze(): Process data and generate insights
    - get_status(): Return current agent status
    """
    
    def __init__(self, name: str, agent_type: str):
        self.name = name
        self.agent_type = agent_type
        self.is_active = True
        self.last_update = datetime.utcnow()
        self.confidence_threshold = 0.6
        
        logger.info(f"🤖 {name} initialized | Type: {agent_type}")
    
    @abstractmethod
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze data and generate insights
        
        Args:
            data: Input data for analysis
            
        Returns:
            Dictionary with analysis results
        """
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status
        
        Returns:
            Dictionary with agent status
        """
        pass
    
    def update_timestamp(self):
        """Update last update timestamp"""
        self.last_update = datetime.utcnow()
    
    def activate(self):
        """Activate the agent"""
        self.is_active = True
        logger.info(f"✅ {self.name} activated")
    
    def deactivate(self):
        """Deactivate the agent"""
        self.is_active = False
        logger.warning(f"⚠️  {self.name} deactivated")
    
    def set_confidence_threshold(self, threshold: float):
        """Set minimum confidence threshold"""
        self.confidence_threshold = max(0.0, min(1.0, threshold))
        logger.info(f"🎯 {self.name} confidence threshold set to {threshold:.2%}")


class Signal:
    """Trading signal from an agent"""
    
    def __init__(
        self,
        agent_name: str,
        action: str,
        confidence: float,
        reason: str,
        metadata: Optional[Dict] = None
    ):
        self.agent_name = agent_name
        self.action = action  # buy, sell, hold
        self.confidence = confidence
        self.reason = reason
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "agent": self.agent_name,
            "action": self.action,
            "confidence": self.confidence,
            "reason": self.reason,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }
    
    def __repr__(self):
        return f"Signal({self.agent_name}: {self.action} @ {self.confidence:.2%})"