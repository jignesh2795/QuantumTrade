"""
Main application entry point for QuantumTrade backend.
Creates and configures the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import Config
from .core.database import init_database
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="QuantumTrade API",
    description="AI-powered algorithmic trading platform",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from .routes.users import router as users_router
from .routes.trades import router as trades_router
from .routes.strategies import router as strategies_router
from .routes.backtest import router as backtest_router
from .routes.realtime import router as realtime_router
from .routes.webhooks import router as webhooks_router
from .routes.auth import router as auth_router
from .routes.market import router as market_router
from .routes.portfolio import router as portfolio_router
from .routes.secure import router as secure_router
from .routes.supabase_portfolio import router as supabase_portfolio_router
from .routes.supabase_strategies import router as supabase_strategies_router
from .routes.supabase_trades import router as supabase_trades_router
from .routes.trades_api import router as trades_api_router
from .routes.backtest_api import router as backtest_api_router

app.include_router(users_router)
app.include_router(trades_router)
app.include_router(strategies_router)
app.include_router(backtest_router)
app.include_router(realtime_router)
app.include_router(webhooks_router)
app.include_router(auth_router)
app.include_router(market_router)
app.include_router(portfolio_router)
app.include_router(secure_router)
app.include_router(supabase_portfolio_router)
app.include_router(supabase_strategies_router)
app.include_router(supabase_trades_router)
app.include_router(trades_api_router)
app.include_router(backtest_api_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    logger.info("Starting QuantumTrade backend...")
    try:
        init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to QuantumTrade API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "quantumtrade-backend"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
