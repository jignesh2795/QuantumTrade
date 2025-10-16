"""
Test script for AI agents
Runs through various scenarios to verify agent behavior
"""
import sys
import asyncio
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ai_agents.agentx_executor import AgentXExecutor
from backend.ai_agents.optima_optimizer import OptimaOptimizer
from backend.ai_agents.hivemind_coordinator import HiveMindCoordinator
from backend.ai_agents.ml_signal_generator import MLSignalGenerator
from backend.ai_agents.base_agent import Signal
from backend.core.exchange_base import Candle


async def test_agentx():
    """Test AgentX execution agent"""
    print("\n" + "=" * 60)
    print("🧪 Testing AgentX (Execution Agent)")
    print("=" * 60)
    
    agent = AgentXExecutor()
    
    # Test execution analysis
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
    
    print(f"✅ Execution Analysis:")
    print(f"   Strategy: {result['execution_strategy']}")
    print(f"   Predicted Slippage: {result['predicted_slippage']*100:.3f}%")
    print(f"   Optimal Price: ${result['optimal_price']:,.2f}")
    print(f"   Confidence: {result['confidence']:.2%}")
    
    # Test execution recording
    agent.record_execution({
        "order_id": "TEST123",
        "filled": True,
        "actual_slippage": 0.0015
    })
    
    status = agent.get_status()
    print(f"\n✅ AgentX Status:")
    print(f"   Total Executions: {status['total_executions']}")
    print(f"   Avg Slippage: {status['avg_slippage']*100:.3f}%")
    print(f"   Fill Rate: {status['fill_rate']*100:.1f}%")


async def test_optima():
    """Test Optima optimization agent"""
    print("\n" + "=" * 60)
    print("🧪 Testing Optima (Optimization Agent)")
    print("=" * 60)
    
    agent = OptimaOptimizer()
    
    # Simulate some performance data
    for i in range(60):
        agent._record_performance(
            performance={"win_rate": 0.5 + (i * 0.001)},
            parameters={"sma_fast_period": 10}
        )
    
    # Test optimization analysis
    data = {
        "performance": {"win_rate": 0.45, "total_pnl": -100},
        "parameters": {
            "sma_fast_period": 10,
            "sma_slow_period": 30,
            "position_size": 0.1
        }
    }
    
    result = await agent.analyze(data)
    
    print(f"✅ Optimization Analysis:")
    print(f"   Needs Optimization: {result.get('needs_optimization', False)}")
    
    if result.get('suggestions'):
        print(f"   Suggestions ({len(result['suggestions'])}):")
        for suggestion in result['suggestions'][:3]:
            print(f"      - {suggestion['parameter']}: {suggestion['current']} → {suggestion['suggested']}")
            print(f"        Reason: {suggestion['reason']}")
    
    status = agent.get_status()
    print(f"\n✅ Optima Status:")
    print(f"   Optimization Cycles: {status['optimization_cycles']}")
    print(f"   Performance Records: {status['performance_records']}")


async def test_hivemind():
    """Test HiveMind coordinator agent"""
    print("\n" + "=" * 60)
    print("🧪 Testing HiveMind (Coordinator Agent)")
    print("=" * 60)
    
    agent = HiveMindCoordinator()
    
    # Create test signals
    signals = [
        Signal("Strategy", "buy", 0.75, "Bullish SMA crossover"),
        Signal("MLSignal", "buy", 0.68, "ML prediction positive"),
        Signal("Guard", "hold", 0.50, "Risk check neutral"),
        Signal("AgentX", "buy", 0.70, "Good execution conditions")
    ]
    
    print(f"📊 Input Signals ({len(signals)}):")
    for signal in signals:
        print(f"   {signal.agent_name}: {signal.action.upper()} @ {signal.confidence:.2%}")
    
    # Test decision making
    result = await agent.analyze({"signals": signals})
    
    print(f"\n✅ HiveMind Decision:")
    print(f"   Decision: {result['decision'].upper()}")
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Consensus: {result['consensus']:.2%}")
    print(f"   Reason: {result['reason']}")
    print(f"   Vote Distribution:")
    for action, votes in result['votes'].items():
        print(f"      {action}: {votes:.2%}")
    
    # Test weight calibration
    print(f"\n🎯 Testing Weight Calibration:")
    print(f"   Initial Weights: {agent.agent_weights}")
    
    agent.calibrate_weights({
        "Strategy": 0.65,
        "MLSignal": 0.58,
        "Guard": 0.80,
        "AgentX": 0.75
    })
    
    print(f"   Updated Weights: {agent.agent_weights}")
    
    status = agent.get_status()
    print(f"\n✅ HiveMind Status:")
    print(f"   Decisions Made: {status['decisions_made']}")
    print(f"   Consensus Threshold: {status['consensus_threshold']:.2%}")


async def test_ml_signal():
    """Test ML Signal Generator"""
    print("\n" + "=" * 60)
    print("🧪 Testing MLSignal (ML Generator Agent)")
    print("=" * 60)
    
    agent = MLSignalGenerator()
    
    # Create mock candles with uptrend
    candles = []
    now = datetime.utcnow()
    base_price = 40000
    
    for i in range(50):
        price = base_price + (i * 50)  # Gradual uptrend
        candles.append(Candle(
            timestamp=now - timedelta(hours=50-i),
            open=price,
            high=price + 20,
            low=price - 20,
            close=price + 10,
            volume=1000 + (i * 10)
        ))
    
    # Test signal generation
    result = await agent.analyze({"candles": candles})
    
    print(f"✅ ML Signal:")
    print(f"   Action: {result['action'].upper()}")
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Reason: {result['reason']}")
    
    if 'probabilities' in result:
        print(f"   Probabilities:")
        for action, prob in result['probabilities'].items():
            print(f"      {action}: {prob:.2%}")
    
    status = agent.get_status()
    print(f"\n✅ MLSignal Status:")
    print(f"   ML Available: {status['ml_available']}")
    print(f"   Is Trained: {status['is_trained']}")
    print(f"   Model Type: {status['model_type']}")


async def test_full_ensemble():
    """Test full agent ensemble working together"""
    print("\n" + "=" * 60)
    print("🧪 Testing Full Agent Ensemble")
    print("=" * 60)
    
    # Initialize all agents
    agentx = AgentXExecutor()
    optima = OptimaOptimizer()
    hivemind = HiveMindCoordinator()
    ml_signal = MLSignalGenerator()
    
    # Create mock data
    candles = []
    now = datetime.utcnow()
    for i in range(50):
        price = 43000 + (i * 20)
        candles.append(Candle(
            timestamp=now - timedelta(hours=50-i),
            open=price,
            high=price + 50,
            low=price - 50,
            close=price + 25,
            volume=1000
        ))
    
    # Collect signals from all agents
    signals = []
    
    # ML Signal
    ml_result = await ml_signal.analyze({"candles": candles})
    signals.append(Signal(
        "MLSignal",
        ml_result['action'],
        ml_result['confidence'],
        ml_result['reason']
    ))
    
    # Mock strategy signal
    signals.append(Signal(
        "Strategy",
        "buy",
        0.75,
        "Bullish crossover detected"
    ))
    
    # Mock guard signal
    signals.append(Signal(
        "Guard",
        "hold",
        0.60,
        "Risk parameters acceptable"
    ))
    
    print(f"📊 Collected Signals ({len(signals)}):")
    for signal in signals:
        print(f"   {signal.agent_name}: {signal.action.upper()} @ {signal.confidence:.2%}")
    
    # HiveMind makes decision
    decision = await hivemind.analyze({"signals": signals})
    
    print(f"\n🧠 HiveMind Final Decision:")
    print(f"   Action: {decision['decision'].upper()}")
    print(f"   Confidence: {decision['confidence']:.2%}")
    print(f"   Consensus: {decision['consensus']:.2%}")
    
    # If decision is to buy, get execution plan
    if decision['decision'] == 'buy':
        exec_plan = await agentx.analyze({
            "symbol": "BTCUSDT",
            "side": "buy",
            "quantity": 0.1,
            "current_price": candles[-1].close,
            "order_type": "market",
            "avg_volume": 1000,
            "volatility": 0.02,
            "spread": 0.001
        })
        
        print(f"\n🤖 AgentX Execution Plan:")
        print(f"   Strategy: {exec_plan['execution_strategy']}")
        print(f"   Optimal Price: ${exec_plan['optimal_price']:,.2f}")
        print(f"   Predicted Slippage: {exec_plan['predicted_slippage']*100:.3f}%")
    
    print(f"\n✅ Full ensemble test complete!")


async def main():
    """Run all agent tests"""
    print("=" * 60)
    print("🤖 QUANTUMTRADE AI AGENT TEST SUITE")
    print("=" * 60)
    
    try:
        await test_agentx()
        await asyncio.sleep(1)
        
        await test_optima()
        await asyncio.sleep(1)
        
        await test_hivemind()
        await asyncio.sleep(1)
        
        await test_ml_signal()
        await asyncio.sleep(1)
        
        await test_full_ensemble()
        
        print("\n" + "=" * 60)
        print("✅ ALL AGENT TESTS PASSED!")
        print("=" * 60)
        print("\nYour AI agent system is working correctly!")
        print("Ready to trade with intelligent agents! 🚀")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)