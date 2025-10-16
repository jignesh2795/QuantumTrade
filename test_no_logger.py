import asyncio
import logging
from datetime import datetime

# Disable logging to avoid any issues
logging.disable(logging.CRITICAL)

async def test_agent():
    print("Testing AgentX without logger...")
    
    try:
        from backend.ai_agents.agentx_executor import AgentXExecutor
        
        # Create agent without logger
        agent = AgentXExecutor.__new__(AgentXExecutor)
        agent.name = "AgentX"
        agent.agent_type = "execution"
        agent.is_active = True
        agent.last_update = datetime.utcnow()
        agent.confidence_threshold = 0.6
        agent.execution_history = []
        agent.avg_slippage = 0.0
        agent.fill_rate = 1.0
        agent.total_executions = 0
        
        print("✅ AgentX created manually")
        
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
        print("✅ Analysis completed")
        print(f"Result keys: {list(result.keys())}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_agent())