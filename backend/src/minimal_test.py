from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/test")
def test_endpoint():
    return {"message": "test"}

@app.get("/data/historical")
def get_historical_data(symbol: str = "BTC-USD", days: int = 30):
    return {"symbol": symbol, "days": days}

# Test with TestClient
client = TestClient(app)

def test_with_client():
    response = client.get("/data/historical?symbol=BTC-USD&days=5")
    print(f"TestClient status: {response.status_code}")
    print(f"TestClient response: {response.json()}")

if __name__ == "__main__":
    test_with_client()