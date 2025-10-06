"""
Scalability configuration for QuantumTrade
"""
import os

class ScalabilitySettings:
    # Worker Configuration
    WORKER_COUNT: int = int(os.getenv("WORKER_COUNT", "4"))
    WORKER_TIMEOUT: int = int(os.getenv("WORKER_TIMEOUT", "30"))
    
    # Queue Configuration (for async tasks)
    QUEUE_MAX_SIZE: int = int(os.getenv("QUEUE_MAX_SIZE", "1000"))
    QUEUE_TIMEOUT: int = int(os.getenv("QUEUE_TIMEOUT", "30"))
    
    # Caching Configuration
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "10000"))
    
    # Database Connection Pool
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "20"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "30"))
    
    # API Rate Limiting
    API_RATE_LIMIT: str = os.getenv("API_RATE_LIMIT", "100/minute")
    
    # Load Balancing
    ENABLE_LOAD_BALANCING: bool = os.getenv("ENABLE_LOAD_BALANCING", "false").lower() == "true"
    
    # Microservice Configuration
    ENABLE_MICROSERVICES: bool = os.getenv("ENABLE_MICROSERVICES", "false").lower() == "true"
    
    # Async Processing
    ENABLE_ASYNC_PROCESSING: bool = os.getenv("ENABLE_ASYNC_PROCESSING", "true").lower() == "true"

# Agent plugin configuration
AGENT_PLUGINS = {
    "data_agent": {
        "enabled": True,
        "module": "src.agents.plugins.data_agent",
        "class": "DataAgent"
    },
    "strategy_agent": {
        "enabled": True,
        "module": "src.agents.plugins.strategy_agent",
        "class": "StrategyAgent"
    },
    "risk_agent": {
        "enabled": True,
        "module": "src.agents.plugins.risk_agent",
        "class": "RiskAgent"
    },
    "execution_agent": {
        "enabled": True,
        "module": "src.agents.plugins.execution_agent",
        "class": "ExecutionAgent"
    }
}

def get_enabled_agents():
    """Get list of enabled agents"""
    return [name for name, config in AGENT_PLUGINS.items() if config["enabled"]]

def get_agent_config(agent_name: str):
    """Get configuration for a specific agent"""
    return AGENT_PLUGINS.get(agent_name, {})

# Service scaling configuration
SERVICE_SCALING = {
    "api_service": {
        "min_instances": 1,
        "max_instances": 10,
        "scale_threshold": 70  # CPU percentage
    },
    "agent_service": {
        "min_instances": 2,
        "max_instances": 20,
        "scale_threshold": 80
    },
    "database_service": {
        "min_instances": 1,
        "max_instances": 5,
        "scale_threshold": 75
    }
}