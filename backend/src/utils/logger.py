"""
Structured Logger for QuantumTrade Platform
Provides consistent logging format and levels across the application
"""

import logging
import logging.handlers
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import traceback


class StructuredLogger:
    """Structured logger with JSON formatting and multiple handlers"""

    def __init__(self, name: str = "quantumtrade", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """Setup logging handlers"""
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler for general logs
        if not os.path.exists("logs"):
            os.makedirs("logs")

        file_handler = logging.handlers.RotatingFileHandler(
            "logs/quantumtrade.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
        )
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # JSON file handler for structured logs
        json_handler = logging.handlers.RotatingFileHandler(
            "logs/quantumtrade_structured.log", maxBytes=10 * 1024 * 1024, backupCount=5
        )
        json_formatter = JSONFormatter()
        json_handler.setFormatter(json_formatter)
        self.logger.addHandler(json_handler)

    def _log(self, level: int, message: str, **kwargs):
        """Internal logging method"""
        if kwargs:
            # Add structured data to message
            structured_data = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
            full_message = f"{message} | {structured_data}"
            self.logger.log(level, full_message)

            # Also log structured data separately
            self.logger.log(
                level,
                json.dumps(
                    {
                        "message": message,
                        "timestamp": datetime.utcnow().isoformat(),
                        "data": kwargs,
                    }
                ),
            )
        else:
            self.logger.log(level, message)

    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log error message"""
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self._log(logging.CRITICAL, message, **kwargs)

    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        kwargs["traceback"] = traceback.format_exc()
        self._log(logging.ERROR, message, **kwargs)


class ColoredFormatter(logging.Formatter):
    """Colored console formatter"""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        record.levelname = f"{log_color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, "__dict__"):
            for key, value in record.__dict__.items():
                if key not in [
                    "name",
                    "msg",
                    "args",
                    "levelname",
                    "levelno",
                    "pathname",
                    "filename",
                    "module",
                    "lineno",
                    "funcName",
                    "created",
                    "msecs",
                    "relativeCreated",
                    "thread",
                    "threadName",
                    "process",
                    "exc_info",
                    "exc_text",
                    "stack_info",
                ]:
                    log_entry[key] = value

        return json.dumps(log_entry)


# Global logger instance
logger = StructuredLogger("quantumtrade")


def get_logger(name: str = "quantumtrade") -> StructuredLogger:
    """
    Get a structured logger instance

    Args:
        name: Logger name

    Returns:
        StructuredLogger instance
    """
    return StructuredLogger(name)


def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None):
    """
    Setup global logging configuration

    Args:
        level: Logging level
        log_file: Optional custom log file path
    """
    global logger
    logger = StructuredLogger("quantumtrade", level)

    # Set level for all existing loggers
    logging.getLogger().setLevel(level)

    return logger


# Convenience functions
def debug(message: str, **kwargs):
    """Log debug message"""
    logger.debug(message, **kwargs)


def info(message: str, **kwargs):
    """Log info message"""
    logger.info(message, **kwargs)


def warning(message: str, **kwargs):
    """Log warning message"""
    logger.warning(message, **kwargs)


def error(message: str, **kwargs):
    """Log error message"""
    logger.error(message, **kwargs)


def critical(message: str, **kwargs):
    """Log critical message"""
    logger.critical(message, **kwargs)


def exception(message: str, **kwargs):
    """Log exception with traceback"""
    logger.exception(message, **kwargs)
