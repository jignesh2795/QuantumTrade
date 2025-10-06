"""
Simulates trade execution
"""
class ExecutionAgent:
    """
    Simulates trade execution
    """
    def execute_trade(self, symbol, action, size):
        return {"symbol": symbol, "action": action, "size": size, "status": "executed"}