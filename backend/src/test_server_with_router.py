from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.routes import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_historical_endpoint():
    response = client.get("/data/historical?symbol=BTC-USD&days=5")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")

def test_all_endpoints():
    # Test root
    response = client.get("/")
    print(f"Root status: {response.status_code}")
    
    # Test health
    response = client.get("/health")
    print(f"Health status: {response.status_code}")
    
    # Test agents
    response = client.get("/agents")
    print(f"Agents status: {response.status_code}")
    
    # Test historical
    response = client.get("/data/historical?symbol=BTC-USD&days=5")
    print(f"Historical status: {response.status_code}")
    
    # Test price
    response = client.get("/data/price?symbol=BTC-USD")
    print(f"Price status: {response.status_code}")

if __name__ == "__main__":
    test_all_endpoints()