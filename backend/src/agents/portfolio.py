"""
Tracks open positions
"""
class PortfolioAgent:
    """
    Tracks open positions
    """
    def __init__(self):
        self.positions = []

    def add_position(self, symbol, size, price):
        self.positions.append({"symbol": symbol, "size": size, "price": price})
        return {"message": "Position added", "positions": self.positions}

    def list_positions(self):
        return {"positions": self.positions}