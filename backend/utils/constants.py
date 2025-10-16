"""
Application constants
"""

# Trading modes
PAPER_MODE = "paper"
LIVE_MODE = "live"

# Order types
MARKET_ORDER = "market"
LIMIT_ORDER = "limit"
STOP_LOSS_ORDER = "stop_loss"
TAKE_PROFIT_ORDER = "take_profit"

# Order sides
BUY = "buy"
SELL = "sell"

# Order statuses
PENDING = "pending"
FILLED = "filled"
CANCELLED = "cancelled"
REJECTED = "rejected"

# Timeframes
TIMEFRAME_1M = "1m"
TIMEFRAME_5M = "5m"
TIMEFRAME_15M = "15m"
TIMEFRAME_1H = "1h"
TIMEFRAME_4H = "4h"
TIMEFRAME_1D = "1d"

# Risk parameters
DEFAULT_MAX_POSITION_SIZE = 0.1  # 10%
DEFAULT_MAX_DAILY_LOSS = 0.02    # 2%
DEFAULT_STOP_LOSS_PCT = 0.02     # 2%
DEFAULT_TAKE_PROFIT_PCT = 0.04   # 4%

# Exchange names
BINANCE = "binance"
ZERODHA = "zerodha"
UPSTOX = "upstox"
PAPER = "paper"