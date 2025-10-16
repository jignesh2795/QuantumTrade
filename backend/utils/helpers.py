"""
Helper utility functions
"""
from typing import List
from datetime import datetime
import json


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100


def round_to_precision(value: float, precision: int = 8) -> float:
    """Round value to specified decimal places"""
    return round(value, precision)


def format_currency(value: float, symbol: str = "$") -> str:
    """Format value as currency string"""
    return f"{symbol}{value:,.2f}"


def calculate_sma(prices: List[float], period: int) -> float:
    """Calculate Simple Moving Average"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def calculate_ema(prices: List[float], period: int) -> float:
    """Calculate Exponential Moving Average"""
    if len(prices) < period:
        return None
    
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period  # Start with SMA
    
    for price in prices[period:]:
        ema = (price * multiplier) + (ema * (1 - multiplier))
    
    return ema


def timestamp_to_string(timestamp: datetime) -> str:
    """Convert datetime to ISO format string"""
    return timestamp.isoformat()


def string_to_timestamp(timestamp_str: str) -> datetime:
    """Convert ISO format string to datetime"""
    return datetime.fromisoformat(timestamp_str)


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is 0"""
    if denominator == 0:
        return default
    return numerator / denominator


def dict_to_json(data: dict) -> str:
    """Convert dictionary to JSON string"""
    return json.dumps(data, default=str, indent=2)


def json_to_dict(json_str: str) -> dict:
    """Convert JSON string to dictionary"""
    return json.loads(json_str)