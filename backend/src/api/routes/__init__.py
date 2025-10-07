from fastapi import APIRouter 
from src.agents.strategy_agent import StrategyAgent 
from src.agents.data_agent import DataAgent 
from src.agents.risk_agent import RiskAgent 
from src.agents.portfolio import PortfolioAgent 
from src.agents.execution_agent import ExecutionAgent 
 
router = APIRouter() 
 
portfolio = PortfolioAgent() 
 
@router.get("/health") 
def health_check(): 
    return {"status": "ok"} 
 
@router.get("/agents") 
def list_agents(): 
    return {"agents": ["data_agent", "strategy_agent", "risk_agent", "portfolio", "execution_agent"]} 
 
@router.get("/strategy/signal") 
def strategy_signal(symbol: str = "BTC-USD"): 
    agent = StrategyAgent(symbol) 
    return agent.generate_signal() 
 
@router.get("/data/price") 
def get_price(symbol: str = "BTC-USD"): 
    agent = DataAgent() 
    return agent.get_price(symbol) 
 
@router.post("/portfolio/add") 
def add_position(symbol: str, size: float, price: float): 
    return portfolio.add_position(symbol, size, price) 
 
@router.get("/portfolio/list") 
def list_positions(): 
    return portfolio.list_positions() 
 
@router.get("/risk/assess") 
def assess_risk(position_size: float = 1000, account_balance: float = 10000): 
    agent = RiskAgent() 
    return agent.assess_risk(position_size, account_balance) 
 
@router.post("/execute/trade") 
def execute_trade(symbol: str, action: str, size: float): 
    agent = ExecutionAgent() 
    return agent.execute_trade(symbol, action, size) 
