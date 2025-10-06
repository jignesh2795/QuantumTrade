import pytest
from fastapi.testclient import TestClient
from src.api.server import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_agents():
    response = client.get("/agents")
    assert response.status_code == 200
    assert "agents" in response.json()
    agents = response.json()["agents"]
    assert "data_agent" in agents
    assert "strategy_agent" in agents
    assert "risk_agent" in agents
    assert "portfolio" in agents
    assert "execution_agent" in agents

def test_strategy_signal():
    response = client.get("/strategy/signal?symbol=BTC-USD")
    assert response.status_code == 200
    data = response.json()
    assert "symbol" in data
    assert "signal" in data
    assert data["symbol"] == "BTC-USD"
    assert data["signal"] in ["BUY", "SELL", "HOLD"]

def test_data_price():
    response = client.get("/data/price?symbol=ETH-USD")
    assert response.status_code == 200
    data = response.json()
    assert "symbol" in data
    assert "price" in data
    assert data["symbol"] == "ETH-USD"
    assert data["price"] == 2000

def test_data_historical():
    response = client.get("/data/historical?symbol=BTC-USD&days=5")
    assert response.status_code == 200
    data = response.json()
    assert "symbol" in data
    assert "data" in data
    assert data["symbol"] == "BTC-USD"
    assert len(data["data"]) <= 5

def test_portfolio_add_and_list():
    # Add a position
    response = client.post("/portfolio/add?symbol=BTC-USD&size=1.0&price=30000")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "positions" in data
    
    # List positions
    response = client.get("/portfolio/list")
    assert response.status_code == 200
    data = response.json()
    assert "positions" in data
    assert len(data["positions"]) > 0

def test_risk_assessment():
    response = client.get("/risk/assess?position_size=1000&account_balance=10000")
    assert response.status_code == 200
    data = response.json()
    assert "position_size" in data
    assert "account_balance" in data
    assert "risk_percent" in data
    assert "status" in data

def test_execute_trade():
    response = client.post("/execute/trade?symbol=BTC-USD&action=BUY&size=1.0")
    assert response.status_code == 200
    data = response.json()
    assert "symbol" in data
    assert "action" in data
    assert "size" in data
    assert "status" in data
    assert data["status"] == "executed"

if __name__ == "__main__":
    pytest.main([__file__])