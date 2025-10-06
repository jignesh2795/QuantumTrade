"""
Generates buy/sell/hold signals based on price trends and technical indicators
"""
import random
import requests

class StrategyAgent:
    """
    Generates buy/sell/hold signals based on price trends and technical indicators
    """
    def __init__(self, symbol="BTC-USD"):
        self.symbol = symbol

    def generate_signal(self):
        # In a real implementation, we would fetch historical data and apply technical analysis
        # For this demo, we'll enhance the random signal with some basic logic
        
        # Fetch current price (in a real implementation, this would be from our DataAgent)
        try:
            response = requests.get(f"http://localhost:8000/data/price?symbol={self.symbol}")
            if response.status_code == 200:
                data = response.json()
                current_price = data.get("price", 0)
            else:
                current_price = 0
        except:
            current_price = 0
        
        # Enhanced signal generation based on price (simplified)
        if current_price > 0:
            # Simple logic: if price is high, more likely to sell; if low, more likely to buy
            if current_price > 25000:  # For BTC
                signal = random.choices(["SELL", "HOLD", "BUY"], weights=[0.5, 0.3, 0.2])[0]
            elif current_price < 15000:  # For BTC
                signal = random.choices(["BUY", "HOLD", "SELL"], weights=[0.5, 0.3, 0.2])[0]
            else:
                signal = random.choice(["BUY", "SELL", "HOLD"])
        else:
            signal = random.choice(["BUY", "SELL", "HOLD"])
            
        return {"symbol": self.symbol, "signal": signal, "timestamp": "2025-10-06T17:00:00Z"}