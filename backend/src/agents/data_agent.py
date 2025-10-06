"""
Sample data agent that provides market prices and historical data
"""
import random
from datetime import datetime, timedelta

class DataAgent:
    """
    Sample data agent that provides market prices and historical data
    """
    def __init__(self):
        self.data = {
            "BTC-USD": 30000,
            "ETH-USD": 2000,
            "SOL-USD": 25
        }
        
        # Generate some historical data
        self.historical_data = {}
        for symbol in self.data.keys():
            self.historical_data[symbol] = self._generate_historical_data(symbol)

    def _generate_historical_data(self, symbol):
        """Generate mock historical data for a symbol"""
        data = []
        base_price = self.data[symbol]
        current_date = datetime.now() - timedelta(days=30)
        
        for i in range(30):
            # Add some random variation
            price = base_price * (1 + random.uniform(-0.1, 0.1))
            data.append({
                "date": (current_date + timedelta(days=i)).strftime("%Y-%m-%d"),
                "price": round(price, 2),
                "volume": random.randint(1000, 10000)
            })
        return data

    def get_price(self, symbol: str):
        return {"symbol": symbol, "price": self.data.get(symbol, None)}
    
    def get_historical_data(self, symbol: str, days: int = 30):
        """Get historical data for a symbol"""
        data = self.historical_data.get(symbol, [])
        # Return only the requested number of days
        return {"symbol": symbol, "data": data[-days:] if len(data) >= days else data}