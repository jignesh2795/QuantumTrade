"""
Settings and Configuration Management
"""
import os
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATABASE_DIR = BASE_DIR / "database"
    CONFIG_DIR = BASE_DIR / "config"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_DIR}/quantumtrade.db")
    
    # Trading mode
    TRADING_MODE: Literal["paper", "live"] = os.getenv("TRADING_MODE", "paper")
    
    # Exchange/Broker settings
    EXCHANGE = os.getenv("EXCHANGE", "binance")
    API_KEY = os.getenv("API_KEY", "")
    API_SECRET = os.getenv("API_SECRET", "")
    
    # Trading parameters
    INITIAL_CAPITAL = float(os.getenv("INITIAL_CAPITAL", "10000"))
    DEFAULT_SYMBOL = os.getenv("DEFAULT_SYMBOL", "BTCUSDT")
    TIMEFRAME = os.getenv("TIMEFRAME", "1h")
    
    # Risk management
    MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "0.1"))  # 10% of capital
    MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", "0.02"))  # 2% daily loss limit
    
    # Strategy settings
    STRATEGY = os.getenv("STRATEGY", "sma_crossover")
    SMA_FAST_PERIOD = int(os.getenv("SMA_FAST_PERIOD", "10"))
    SMA_SLOW_PERIOD = int(os.getenv("SMA_SLOW_PERIOD", "30"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # API Server
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    def __init__(self):
        """Ensure directories exist"""
        self.DATABASE_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)
        self.CONFIG_DIR.mkdir(exist_ok=True)
    
    def validate(self) -> bool:
        """Validate settings"""
        if self.TRADING_MODE == "live" and (not self.API_KEY or not self.API_SECRET):
            raise ValueError("API_KEY and API_SECRET required for live trading")
        return True


# Global settings instance
settings = Settings()