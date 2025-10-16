"""
Test AI Agents functionality
"""
import pytest
import asyncio
from backend.ai_agents.agentx_executor import AgentXExecutor
from backend.ai_agents.optima_optimizer import OptimaOptimizer
from backend.ai_agents.hivemind_coordinator import HiveMindCoordinator
from backend.ai_agents.ml_signal_generator import MLSignalGenerator
from backend.ai_agents.base_agent import Signal


@pytest.mark.asyncio
async def test_agentx_initialization():
    """Test AgentX initialization"""
    agent = AgentXExecutor()
    assert agent.name == "AgentX"
    assert agent.agent_type == "execution"
    assert agent.is_active == True


@pytest.mark.asyncio
async def test_agentx_execution_analysis():
    """Test AgentX execution analysis"""
    agent = AgentXExecutor()
    
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
    
    assert "execution_ready" in result
    assert "predicted_slippage" in result
    assert "optimal_price" in result
    assert result["predicted_slippage"] > 0


@pytest.mark.asyncio
async def test_optima_initialization():
    """Test Optima initialization"""
    agent = OptimaOptimizer()
    assert agent.name == "Optima"
    assert agent.agent_type == "optimizer"


@pytest.mark.asyncio
async def test_optima_optimization():
    """Test Optima optimization suggestions"""
    agent = OptimaOptimizer()
    
    data = {
        "performance": {"win_rate": 0.45, "total_pnl": -100},
        "parameters": {
            "sma_fast_period": 10,
            "sma_slow_period": 30,
            "position_size": 0.1
        }
    }
    
    result = await agent.analyze(data)
    
    assert "agent" in result
    assert result["agent"] == "Optima"


@pytest.mark.asyncio
async def test_hivemind_initialization():
    """Test HiveMind initialization"""
    agent = HiveMindCoordinator()
    assert agent.name == "HiveMind"
    assert agent.agent_type == "coordinator"
    assert len(agent.agent_weights) > 0


@pytest.mark.asyncio
async def test_hivemind_signal_aggregation():
    """Test HiveMind signal aggregation"""
    agent = HiveMindCoordinator()
    
    signals = [
        Signal("Strategy", "buy", 0.7, "Bullish crossover"),
        Signal("MLSignal", "buy", 0.6, "ML prediction"),
        Signal("Guard", "hold", 0.5, "Risk check")
    ]
    
    result = await agent.analyze({"signals": signals})
    
    assert "decision" in result
    assert "confidence" in result
    assert "consensus" in result
    assert result["decision"] in ["buy", "sell", "hold"]


@pytest.mark.asyncio
async def test_hivemind_weight_update():
    """Test HiveMind weight updates"""
    agent = HiveMindCoordinator()
    
    initial_weight = agent.agent_weights.get("Strategy", 0.25)
    agent.update_agent_weight("Strategy", 0.35)
    new_weight = agent.agent_weights["Strategy"]
    
    assert new_weight != initial_weight


@pytest.mark.asyncio
async def test_ml_signal_initialization():
    """Test ML Signal Generator initialization"""
    agent = MLSignalGenerator()
    assert agent.name == "MLSignal"
    assert agent.agent_type == "ml_generator"


@pytest.mark.asyncio
async def test_ml_signal_generation():
    """Test ML signal generation (rule-based fallback)"""
    agent = MLSignalGenerator()
    
    from backend.core.exchange_base import Candle
    from datetime import datetime, timedelta
    
    # Create mock candles
    candles = []
    now = datetime.utcnow()
    for i in range(50):
        candles.append(Candle(
            timestamp=now - timedelta(hours=50-i),
            open=100 + i * 0.5,
            high=101 + i * 0.5,
            low=99 + i * 0.5,
            close=100 + i * 0.5,
            volume=1000
        ))
    
    result = await agent.analyze({"candles": candles})
    
    assert "action" in result
    assert "confidence" in result
    assert result["action"] in ["buy", "sell", "hold"]


def test_signal_creation():
    """Test Signal object creation"""
    signal = Signal(
        agent_name="TestAgent",
        action="buy",
        confidence=0.75,
        reason="Test signal"
    )
    
    assert signal.agent_name == "TestAgent"
    assert signal.action == "buy"
    assert signal.confidence == 0.75
    
    signal_dict = signal.to_dict()
    assert "agent" in signal_dict
    assert "action" in signal_dict