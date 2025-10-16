"""Utility functions"""
from backend.utils.logger import setup_logger, TradingLogger
from backend.utils.settings import Settings, settings
from backend.utils.notifications import NotificationManager
from backend.utils.helpers import (
    calculate_percentage_change,
    round_to_precision,
    format_currency,
    calculate_sma,
    calculate_ema,
    timestamp_to_string,
    string_to_timestamp,
    safe_divide,
    dict_to_json,
    json_to_dict
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
    "calculate_sma",
    "calculate_ema",
    "timestamp_to_string",
    "string_to_timestamp",
    "safe_divide",
    "dict_to_json",
    "json_to_dict"
]