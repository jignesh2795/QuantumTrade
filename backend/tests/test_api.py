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

if __name__ == "__main__":
    pytest.main([__file__])