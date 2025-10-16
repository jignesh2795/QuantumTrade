import asyncio

async def test_agent():
    print("Testing AgentX...")
    
    try:
        from backend.ai_agents.agentx_executor import AgentXExecutor
        agent = AgentXExecutor()
        print("✅ AgentX created")
        
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