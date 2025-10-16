"""
Settings and Configuration Management - Updated for Phase 2
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
    USE_TESTNET = os.getenv("USE_TESTNET", "true").lower() == "true"
    
    # Trading parameters
    INITIAL_CAPITAL = float(os.getenv("INITIAL_CAPITAL", "10000"))
    DEFAULT_SYMBOL = os.getenv("DEFAULT_SYMBOL", "BTCUSDT")
    TIMEFRAME = os.getenv("TIMEFRAME", "1h")
    
    # Risk management (Phase 2)
    MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "0.1"))  # 10% of capital
    MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", "0.02"))  # 2% daily loss limit
    MAX_DRAWDOWN = float(os.getenv("MAX_DRAWDOWN", "0.10"))  # 10% max drawdown
    STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", "0.02"))  # 2% stop loss
    TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", "0.04"))  # 4% take profit
    
    # Strategy settings
    STRATEGY = os.getenv("STRATEGY", "sma_crossover")
    SMA_FAST_PERIOD = int(os.getenv("SMA_FAST_PERIOD", "10"))
    SMA_SLOW_PERIOD = int(os.getenv("SMA_SLOW_PERIOD", "30"))
    
    # Notifications (Phase 2)
    EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    FROM_EMAIL = os.getenv("FROM_EMAIL", "")
    TO_EMAIL = os.getenv("TO_EMAIL", "")
    
    # Safety features (Phase 2)
    REQUIRE_CONFIRMATION = os.getenv("REQUIRE_CONFIRMATION", "true").lower() == "true"
    DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
    
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
        if self.TRADING_MODE == "live":
            if not self.API_KEY or not self.API_SECRET:
                raise ValueError("API_KEY and API_SECRET required for live trading")
            
            if self.REQUIRE_CONFIRMATION:
                print("\n" + "="*60)
                print("⚠️  LIVE TRADING MODE WARNING")
                print("="*60)
                print(f"Exchange: {self.EXCHANGE}")
                print(f"Symbol: {self.DEFAULT_SYMBOL}")
                print(f"Max Position Size: {self.MAX_POSITION_SIZE*100:.1f}%")
                print(f"Max Daily Loss: {self.MAX_DAILY_LOSS*100:.1f}%")
                print(f"Stop Loss: {self.STOP_LOSS_PCT*100:.1f}%")
                print("="*60)
                
                confirmation = input("\nType 'YES' to continue with live trading: ")
                if confirmation != "YES":
                    raise ValueError("Live trading not confirmed")
        
        return True


# Global settings instance
settings = Settings()