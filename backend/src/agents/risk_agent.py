"""
Checks risk on a given position
"""
class RiskAgent:
    """
    Checks risk on a given position
    """
    def __init__(self, max_risk_percent=5):
        self.max_risk_percent = max_risk_percent

    def assess_risk(self, position_size: float, account_balance: float):
        risk = (position_size / account_balance) * 100
        status = "OK" if risk <= self.max_risk_percent else "RISKY"
        return {"position_size": position_size, "account_balance": account_balance, "risk_percent": risk, "status": status}