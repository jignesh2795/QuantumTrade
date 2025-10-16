"""
Test imports for AI agents
"""
print("Starting import tests...")

# Test 1: Base agent
try:
    from backend.ai_agents.base_agent import BaseAgent, Signal
    print("✅ BaseAgent and Signal imported")
except Exception as e:
    print(f"❌ BaseAgent import failed: {e}")

# Test 2: AgentX
try:
    from backend.ai_agents.agentx_executor import AgentXExecutor
    print("✅ AgentXExecutor imported")
except Exception as e:
    print(f"❌ AgentXExecutor import failed: {e}")

# Test 3: Optima
try:
    from backend.ai_agents.optima_optimizer import OptimaOptimizer
    print("✅ OptimaOptimizer imported")
except Exception as e:
    print(f"❌ OptimaOptimizer import failed: {e}")

# Test 4: HiveMind
try:
    from backend.ai_agents.hivemind_coordinator import HiveMindCoordinator
    print("✅ HiveMindCoordinator imported")
except Exception as e:
    print(f"❌ HiveMindCoordinator import failed: {e}")

# Test 5: ML Signal
try:
    from backend.ai_agents.ml_signal_generator import MLSignalGenerator
    print("✅ MLSignalGenerator imported")
except Exception as e:
    print(f"❌ MLSignalGenerator import failed: {e}")

print("Import tests completed.")