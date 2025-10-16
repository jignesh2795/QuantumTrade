"""
Verify that AI agents work correctly
"""
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

async def test_agentx():
    """Test AgentX"""
    try:
        from backend.ai_agents.agentx_executor import AgentXExecutor
        agent = AgentXExecutor()
        print("✅ AgentXExecutor created successfully")
        
        # Test analyze method
        data = {
            "symbol": "BTCUSDT",
            "side": "buy",
            "quantity": 0.1,
            "current_price": 43000,
            "order_type": "market",
            "avg_volume": 1000,
            "volatility": 0.02,
            "spread": 0.001
        }
        
        result = await agent.analyze(data)
        print(f"✅ AgentX analysis completed")
        print(f"   Execution strategy: {result.get('execution_strategy', 'N/A')}")
        print(f"   Predicted slippage: {result.get('predicted_slippage', 0)*100:.3f}%")
        return True
    except Exception as e:
        print(f"❌ AgentX test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_hivemind():
    """Test HiveMind"""
    try:
        from backend.ai_agents.hivemind_coordinator import HiveMindCoordinator
        from backend.ai_agents.base_agent import Signal
        agent = HiveMindCoordinator()
        print("✅ HiveMindCoordinator created successfully")
        
        # Test with signals
        signals = [
            Signal("Strategy", "buy", 0.75, "Bullish crossover"),
            Signal("MLSignal", "buy", 0.68, "ML prediction"),
            Signal("Guard", "hold", 0.50, "Risk check")
        ]
        
        result = await agent.analyze({"signals": signals})
        print(f"✅ HiveMind analysis completed")
        print(f"   Decision: {result.get('decision', 'N/A')}")
        print(f"   Confidence: {result.get('confidence', 0)*100:.2f}%")
        return True
    except Exception as e:
        print(f"❌ HiveMind test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run verification tests"""
    print("Verifying AI Agents...")
    print("=" * 50)
    
    tests = [
        test_agentx(),
        test_hivemind()
    ]
    
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    passed = sum(1 for r in results if r is True)
    total = len(results)
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All AI agent verifications passed!")
    else:
        print("❌ Some verifications failed!")

if __name__ == "__main__":
    asyncio.run(main())