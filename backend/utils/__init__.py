"""Utility functions"""
from backend.utils.logger import setup_logger, TradingLogger
from backend.utils.settings import Settings, settings
from backend.utils.notifications import NotificationManager
from backend.utils.helpers import (
    calculate_percentage_change,
    round_to_precision,
    format_currency,
    get_market_hours,
)

__all__ = [
    "setup_logger",
    "TradingLogger",
    "Settings",
    "settings",
    "NotificationManager",
    "calculate_percentage_change",
    "round_to_precision",
    "format_currency",
    "get_market_hours",
]