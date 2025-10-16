print("Starting simple test...")

try:
    from backend.ai_agents.base_agent import Signal
    print("✅ Signal imported")
    
    signal = Signal("TestAgent", "buy", 0.75, "Test signal")
    print("✅ Signal created:", signal)
    
    signal_dict = signal.to_dict()
    print("✅ Signal converted to dict:", signal_dict)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("Simple test completed.")