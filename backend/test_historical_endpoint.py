import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

def test_historical_endpoint():
    response = client.get("/data/historical?symbol=BTC-USD&days=5")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_historical_endpoint()