from fastapi import APIRouter

# Import all route modules
from .market import router as market_router
from .portfolio import router as portfolio_router
from .trades import router as trades_router
from .auth import router as auth_router
from .backtest import router as backtest_router

# Import Supabase route modules
from .supabase_trades import router as supabase_trades_router
from .supabase_portfolio import router as supabase_portfolio_router
from .supabase_strategies import router as supabase_strategies_router

# Import agents for backward compatibility
from ...agents.strategy_agent import StrategyAgent
from ...agents.data_agent import DataAgent
from ...agents.risk_agent import RiskAgent
from ...agents.portfolio import PortfolioAgent
from ...agents.execution_agent import ExecutionAgent

router = APIRouter()

# Include all sub-routers
router.include_router(market_router)
router.include_router(portfolio_router)
router.include_router(trades_router)
router.include_router(auth_router)
router.include_router(backtest_router)

# Include Supabase sub-routers
router.include_router(supabase_trades_router)
router.include_router(supabase_portfolio_router)
router.include_router(supabase_strategies_router)

# Keep existing endpoints for backward compatibility
portfolio = PortfolioAgent()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/agents")
def list_agents():
    return {
        "agents": [
            "data_agent",
            "strategy_agent",
            "risk_agent",
            "portfolio",
            "execution_agent",
        ]
    }


@router.get("/strategy/signal")
def strategy_signal(symbol: str = "BTC-USD"):
    agent = StrategyAgent(symbol)
    return agent.generate_signal()


@router.get("/data/price")
def get_price(symbol: str = "BTC-USD"):
    agent = DataAgent()
    return agent.get_price(symbol)


@router.get("/data/historical")
def get_historical_data(symbol: str = "BTC-USD", days: int = 30):
    agent = DataAgent()
    return agent.get_historical_data(symbol, days)


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
