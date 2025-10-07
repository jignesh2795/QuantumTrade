"""
Data Validation Utilities for QuantumTrade Platform
Provides validation functions for various data types and business rules
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def validate_symbol(symbol: str) -> bool:
    """
    Validate trading symbol format

    Args:
        symbol: Trading symbol to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        if not symbol or not isinstance(symbol, str):
            return False

        # Symbol should be 1-20 characters, alphanumeric and common separators
        pattern = r"^[A-Z0-9\-\.\/]{1,20}$"
        return bool(re.match(pattern, symbol.upper()))
    except Exception as e:
        logger.error(f"Error validating symbol {symbol}: {e}")
        return False


def validate_price(price: float) -> bool:
    """
    Validate price value

    Args:
        price: Price to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        if not isinstance(price, (int, float)):
            return False

        # Price should be positive and reasonable
        return 0 < price < 1000000  # Max $1M per share
    except Exception as e:
        logger.error(f"Error validating price {price}: {e}")
        return False


def validate_quantity(quantity: float) -> bool:
    """
    Validate quantity value

    Args:
        quantity: Quantity to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        if not isinstance(quantity, (int, float)):
            return False

        # Quantity should be positive
        return quantity > 0
    except Exception as e:
        logger.error(f"Error validating quantity {quantity}: {e}")
        return False


def validate_trade_action(action: str) -> bool:
    """
    Validate trade action

    Args:
        action: Trade action to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        if not action or not isinstance(action, str):
            return False

        valid_actions = {"BUY", "SELL"}
        return action.upper() in valid_actions
    except Exception as e:
        logger.error(f"Error validating trade action {action}: {e}")
        return False


def validate_date_range(start_date: str, end_date: str) -> bool:
    """
    Validate date range

    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)

    Returns:
        True if valid, False otherwise
    """
    try:
        if not start_date or not end_date:
            return False

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        # End date should be after start date
        if end <= start:
            return False

        # Date range should not exceed 1 year
        if (end - start).days > 365:
            return False

        return True
    except ValueError:
        # Invalid date format
        return False
    except Exception as e:
        logger.error(f"Error validating date range {start_date} to {end_date}: {e}")
        return False


def validate_email(email: str) -> bool:
    """
    Validate email format

    Args:
        email: Email to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        if not email or not isinstance(email, str):
            return False

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
    except Exception as e:
        logger.error(f"Error validating email {email}: {e}")
        return False


def validate_username(username: str) -> bool:
    """
    Validate username format

    Args:
        username: Username to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        if not username or not isinstance(username, str):
            return False

        # Username should be 3-30 characters, alphanumeric and underscores only
        pattern = r"^[a-zA-Z0-9_]{3,30}$"
        return bool(re.match(pattern, username))
    except Exception as e:
        logger.error(f"Error validating username {username}: {e}")
        return False


def validate_password(password: str) -> Dict[str, Any]:
    """
    Validate password strength

    Args:
        password: Password to validate

    Returns:
        Dictionary with validation results
    """
    try:
        if not password or not isinstance(password, str):
            return {"valid": False, "errors": ["Password is required"]}

        errors = []

        # Check length
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")

        # Check for uppercase letter
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")

        # Check for lowercase letter
        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")

        # Check for digit
        if not re.search(r"\d", password):
            errors.append("Password must contain at least one digit")

        # Check for special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")

        return {"valid": len(errors) == 0, "errors": errors}
    except Exception as e:
        logger.error(f"Error validating password: {e}")
        return {"valid": False, "errors": ["Internal validation error"]}


def validate_trade_data(trade_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate complete trade data

    Args:
        trade_data: Dictionary containing trade data

    Returns:
        Dictionary with validation results
    """
    try:
        errors = []

        # Validate required fields
        required_fields = ["symbol", "action", "size", "price"]
        for field in required_fields:
            if field not in trade_data or trade_data[field] is None:
                errors.append(f"Missing required field: {field}")

        if errors:
            return {"valid": False, "errors": errors}

        # Validate individual fields
        if not validate_symbol(trade_data["symbol"]):
            errors.append("Invalid symbol format")

        if not validate_trade_action(trade_data["action"]):
            errors.append("Invalid trade action")

        if not validate_quantity(trade_data["size"]):
            errors.append("Invalid quantity")

        if not validate_price(trade_data["price"]):
            errors.append("Invalid price")

        return {"valid": len(errors) == 0, "errors": errors}
    except Exception as e:
        logger.error(f"Error validating trade data: {e}")
        return {"valid": False, "errors": ["Internal validation error"]}


def validate_portfolio_data(portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate portfolio data

    Args:
        portfolio_data: Dictionary containing portfolio data

    Returns:
        Dictionary with validation results
    """
    try:
        errors = []

        # Validate required fields
        required_fields = ["symbol", "size", "avg_price", "current_price"]
        for field in required_fields:
            if field not in portfolio_data or portfolio_data[field] is None:
                errors.append(f"Missing required field: {field}")

        if errors:
            return {"valid": False, "errors": errors}

        # Validate individual fields
        if not validate_symbol(portfolio_data["symbol"]):
            errors.append("Invalid symbol format")

        if not validate_quantity(portfolio_data["size"]):
            errors.append("Invalid position size")

        if not validate_price(portfolio_data["avg_price"]):
            errors.append("Invalid average price")

        if not validate_price(portfolio_data["current_price"]):
            errors.append("Invalid current price")

        return {"valid": len(errors) == 0, "errors": errors}
    except Exception as e:
        logger.error(f"Error validating portfolio data: {e}")
        return {"valid": False, "errors": ["Internal validation error"]}


def validate_backtest_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate backtest configuration

    Args:
        config: Dictionary containing backtest configuration

    Returns:
        Dictionary with validation results
    """
    try:
        errors = []

        # Validate required fields
        required_fields = ["strategy", "symbol", "start_date", "end_date"]
        for field in required_fields:
            if field not in config or config[field] is None:
                errors.append(f"Missing required field: {field}")

        if errors:
            return {"valid": False, "errors": errors}

        # Validate individual fields
        if not validate_symbol(config["symbol"]):
            errors.append("Invalid symbol format")

        if not isinstance(config["strategy"], str) or not config["strategy"]:
            errors.append("Invalid strategy")

        if not validate_date_range(config["start_date"], config["end_date"]):
            errors.append("Invalid date range")

        # Validate initial capital if provided
        if "initial_capital" in config:
            if (
                not isinstance(config["initial_capital"], (int, float))
                or config["initial_capital"] <= 0
            ):
                errors.append("Invalid initial capital")

        return {"valid": len(errors) == 0, "errors": errors}
    except Exception as e:
        logger.error(f"Error validating backtest config: {e}")
        return {"valid": False, "errors": ["Internal validation error"]}


def sanitize_symbol(symbol: str) -> str:
    """
    Sanitize symbol input

    Args:
        symbol: Symbol to sanitize

    Returns:
        Sanitized symbol
    """
    try:
        if not symbol or not isinstance(symbol, str):
            return ""

        # Remove any non-alphanumeric characters except common separators
        sanitized = re.sub(r"[^A-Z0-9\-\.\/]", "", symbol.upper())
        return sanitized[:20]  # Limit to 20 characters
    except Exception as e:
        logger.error(f"Error sanitizing symbol {symbol}: {e}")
        return ""


def validate_json_data(data: Dict[str, Any], schema: Dict[str, str]) -> Dict[str, Any]:
    """
    Validate JSON data against a schema

    Args:
        data: Data to validate
        schema: Schema defining expected fields and types

    Returns:
        Dictionary with validation results
    """
    try:
        errors = []

        for field, expected_type in schema.items():
            if field not in data:
                errors.append(f"Missing required field: {field}")
                continue

            value = data[field]

            # Validate type
            if expected_type == "string":
                if not isinstance(value, str):
                    errors.append(f"Field {field} must be a string")
            elif expected_type == "number":
                if not isinstance(value, (int, float)):
                    errors.append(f"Field {field} must be a number")
            elif expected_type == "boolean":
                if not isinstance(value, bool):
                    errors.append(f"Field {field} must be a boolean")
            elif expected_type == "array":
                if not isinstance(value, list):
                    errors.append(f"Field {field} must be an array")
            elif expected_type == "object":
                if not isinstance(value, dict):
                    errors.append(f"Field {field} must be an object")

        return {"valid": len(errors) == 0, "errors": errors}
    except Exception as e:
        logger.error(f"Error validating JSON data: {e}")
        return {"valid": False, "errors": ["Internal validation error"]}
