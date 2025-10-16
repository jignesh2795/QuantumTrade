"""
Simple test for HiveMind coordinator
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_hivemind_import():
    """Test that we can import and instantiate HiveMind"""
    try:
        from backend.ai_agents.hivemind_coordinator import HiveMindCoordinator
        agent = HiveMindCoordinator()
        print("✅ HiveMindCoordinator imported and instantiated successfully")
        print(f"   Agent name: {agent.name}")
        print(f"   Agent type: {agent.agent_type}")
        return True
    except Exception as e:
        print(f"❌ HiveMindCoordinator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing HiveMind Coordinator...")
    print("=" * 40)
    
    if test_hivemind_import():
        print("=" * 40)
        print("✅ HiveMind Coordinator test passed!")
    else:
        print("=" * 40)
        print("❌ HiveMind Coordinator test failed!")