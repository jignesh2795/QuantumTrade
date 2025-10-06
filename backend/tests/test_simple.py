import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

def test_imports():
    """Test that we can import all agents"""
    try:
        from agents.data_agent import DataAgent
        from agents.strategy_agent import StrategyAgent
        from agents.risk_agent import RiskAgent
        from agents.portfolio import PortfolioAgent
        from agents.execution_agent import ExecutionAgent
        assert True
    except ImportError as e:
        print(f"Import error: {e}")
        assert False

if __name__ == "__main__":
    test_imports()
    print("All imports successful!")