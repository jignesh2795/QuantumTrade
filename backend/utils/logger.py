"""
Logging configuration
"""
import logging
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logger(
    name: str,
    level: Optional[str] = None,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Setup logger with console and file handlers
    
    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    # Set level
    log_level = getattr(logging, (level or "INFO").upper())
    logger.setLevel(log_level)
    
    # Create formatters
    # Use simpler format without emojis for Windows compatibility
    if os.name == 'nt':  # Windows
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )
    else:
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )
    
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler - handle Windows encoding issues
    if os.name == 'nt':  # Windows
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    else:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file is None:
        log_dir = Path(__file__).parent.parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"quantumtrade_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Handle encoding for file handler on Windows
    if os.name == 'nt':  # Windows
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
    else:
        file_handler = logging.FileHandler(log_file)
        
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger


class TradingLogger:
    """Specialized logger for trading events"""
    
    def __init__(self, name: str = "trading"):
        self.logger = setup_logger(name)
        self.trade_log_file = Path(__file__).parent.parent.parent / "logs" / "trades.log"
        
    def log_trade(self, trade_data: dict):
        """Log trade execution"""
        # Use text-only format for Windows compatibility
        if os.name == 'nt':  # Windows
            self.logger.info(
                f"TRADE | {trade_data['side']} {trade_data['quantity']} {trade_data['symbol']} "
                f"@ {trade_data['price']} | Order: {trade_data['order_id']}"
            )
        else:
            self.logger.info(
                f"TRADE | {trade_data['side']} {trade_data['quantity']} {trade_data['symbol']} "
                f"@ {trade_data['price']} | Order: {trade_data['order_id']}"
            )
        
        # Also write to trade log
        with open(self.trade_log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()} | {trade_data}\n")
    
    def log_signal(self, signal_data: dict):
        """Log trading signal"""
        # Use text-only format for Windows compatibility
        if os.name == 'nt':  # Windows
            self.logger.info(
                f"SIGNAL | {signal_data['action']} {signal_data['symbol']} | "
                f"Strategy: {signal_data['strategy']} | Confidence: {signal_data['confidence']:.2f}"
            )
        else:
            self.logger.info(
                f"SIGNAL | {signal_data['action']} {signal_data['symbol']} | "
                f"Strategy: {signal_data['strategy']} | Confidence: {signal_data['confidence']:.2f}"
            )
    
    def log_pnl(self, pnl_data: dict):
        """Log P&L update"""
        # Use text-only format for Windows compatibility
        if os.name == 'nt':  # Windows
            self.logger.info(
                f"P&L | Unrealized: {pnl_data['unrealized_pnl']:.2f} | "
                f"Realized: {pnl_data['realized_pnl']:.2f} | "
                f"Total: {pnl_data['total_pnl']:.2f}"
            )
        else:
            self.logger.info(
                f"P&L | Unrealized: {pnl_data['unrealized_pnl']:.2f} | "
                f"Realized: {pnl_data['realized_pnl']:.2f} | "
                f"Total: {pnl_data['total_pnl']:.2f}"
            )