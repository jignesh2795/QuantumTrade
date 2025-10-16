"""
Simple test for AI agents without async
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_base_agent():
    """Test base agent"""
    try:
        from backend.ai_agents.base_agent import BaseAgent, Signal
        print("✅ BaseAgent and Signal imported successfully")
        
        # Test signal creation
        signal = Signal("TestAgent", "buy", 0.75, "Test signal")
        print(f"   Signal created: {signal}")
        return True
    except Exception as e:
        print(f"❌ BaseAgent test failed: {e}")
        return False

def test_agentx():
    """Test AgentX executor"""
    try:
        from backend.ai_agents.agentx_executor import AgentXExecutor
        print("✅ AgentXExecutor imported successfully")
        return True
    except Exception as e:
        print(f"❌ AgentXExecutor test failed: {e}")
        return False

def test_optima():
    """Test Optima optimizer"""
    try:
        from backend.ai_agents.optima_optimizer import OptimaOptimizer
        print("✅ OptimaOptimizer imported successfully")
        return True
    except Exception as e:
        print(f"❌ OptimaOptimizer test failed: {e}")
        return False

def test_hivemind():
    """Test HiveMind coordinator"""
    try:
        from backend.ai_agents.hivemind_coordinator import HiveMindCoordinator
        print("✅ HiveMindCoordinator imported successfully")
        return True
    except Exception as e:
        print(f"❌ HiveMindCoordinator test failed: {e}")
        return False

def test_ml_signal():
    """Test ML Signal Generator"""
    try:
        from backend.ai_agents.ml_signal_generator import MLSignalGenerator
        print("✅ MLSignalGenerator imported successfully")
        return True
    except Exception as e:
        print(f"❌ MLSignalGenerator test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing AI Agents (Simple Import Test)...")
    print("=" * 50)
    
    tests = [
        test_base_agent,
        test_agentx,
        test_optima,
        test_hivemind,
        test_ml_signal
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("=" * 50)
    print(f"Passed: {passed}/{len(tests)} tests")
    
    if passed == len(tests):
        print("🎉 All AI agent imports successful!")
    else:
        print("❌ Some imports failed!")