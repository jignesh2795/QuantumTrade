import pytest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Use relative imports
from agents.data_agent import DataAgent
from agents.strategy_agent import StrategyAgent
from agents.risk_agent import RiskAgent
from agents.portfolio import PortfolioAgent
from agents.execution_agent import ExecutionAgent

def test_data_agent():
    agent = DataAgent()
    assert agent is not None
    
    # Test price retrieval
    result = agent.get_price("BTC-USD")
    assert result["symbol"] == "BTC-USD"
    assert result["price"] == 30000
    
    # Test historical data
    result = agent.get_historical_data("BTC-USD", 5)
    assert result["symbol"] == "BTC-USD"
    assert "data" in result
    assert len(result["data"]) <= 5

def test_strategy_agent():
    agent = StrategyAgent("BTC-USD")
    assert agent.symbol == "BTC-USD"
    
    # Test signal generation
    result = agent.generate_signal()
    assert "symbol" in result
    assert "signal" in result
    assert "timestamp" in result
    assert result["signal"] in ["BUY", "SELL", "HOLD"]

def test_risk_agent():
    agent = RiskAgent()
    assert agent.max_risk_percent == 5
    
    # Test risk assessment
    result = agent.assess_risk(1000, 10000)
    assert "position_size" in result
    assert "account_balance" in result
    assert "risk_percent" in result
    assert "status" in result
    assert result["risk_percent"] == 10.0
    assert result["status"] == "RISKY"

def test_portfolio_agent():
    agent = PortfolioAgent()
    assert agent.positions == []
    
    # Test adding a position
    result = agent.add_position("BTC-USD", 1.0, 30000)
    assert "message" in result
    assert "positions" in result
    assert len(result["positions"]) == 1
    assert result["positions"][0]["symbol"] == "BTC-USD"
    
    # Test listing positions
    result = agent.list_positions()
    assert "positions" in result
    assert len(result["positions"]) == 1

def test_execution_agent():
    agent = ExecutionAgent()
    
    # Test trade execution
    result = agent.execute_trade("BTC-USD", "BUY", 1.0)
    assert "symbol" in result
    assert "action" in result
    assert "size" in result
    assert "status" in result
    assert result["symbol"] == "BTC-USD"
    assert result["action"] == "BUY"
    assert result["size"] == 1.0
    assert result["status"] == "executed"

if __name__ == "__main__":
    pytest.main([__file__])