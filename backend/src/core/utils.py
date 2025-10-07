"""
Utility functions for QuantumTrade backend.
Shared helper functions used across the application.
"""

import json
from datetime import datetime
from typing import Any, Dict


def format_response(data: Any, status: str = "success") -> Dict[str, Any]:
    """Format a standard API response."""
    return {"status": status, "timestamp": datetime.utcnow().isoformat(), "data": data}


def parse_json_file(file_path: str) -> Dict:
    """Parse a JSON file and return its contents."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def calculate_position_size(
    account_balance: float, risk_percent: float, stop_loss: float
) -> float:
    """Calculate position size based on risk parameters."""
    risk_amount = account_balance * (risk_percent / 100)
    if stop_loss > 0:
        return risk_amount / stop_loss
    return 0.0


def sanitize_input(input_str: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    # Remove potentially dangerous characters
    sanitized = (
        input_str.replace("<", "").replace(">", "").replace('"', "").replace("'", "")
    )
    return sanitized.strip()
