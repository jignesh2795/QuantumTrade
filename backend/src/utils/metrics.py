"""
Metrics Module for QuantumTrade Platform
Prometheus metrics collection and monitoring
"""

from prometheus_client import Counter, Gauge, Histogram, Summary
import time
from typing import Optional

# Application metrics
TRADES_TOTAL = Counter(
    "quantumtrade_trades_total", "Total number of trades executed", ["action", "symbol"]
)
PORTFOLIO_VALUE = Gauge(
    "quantumtrade_portfolio_value", "Current portfolio value in USD"
)
PnL = Gauge("quantumtrade_pnl", "Current profit and loss")
TRADE_LATENCY = Histogram(
    "quantumtrade_trade_latency_seconds", "Trade execution latency in seconds"
)
API_REQUESTS = Counter(
    "quantumtrade_api_requests_total",
    "Total API requests",
    ["method", "endpoint", "status"],
)
ACTIVE_CONNECTIONS = Gauge(
    "quantumtrade_active_connections", "Number of active connections"
)
STRATEGY_SIGNALS = Counter(
    "quantumtrade_strategy_signals_total",
    "Total strategy signals generated",
    ["strategy", "action"],
)

# Performance metrics
SHARPE_RATIO = Gauge("quantumtrade_sharpe_ratio", "Current Sharpe ratio")
MAX_DRAWDOWN = Gauge("quantumtrade_max_drawdown_percent", "Maximum drawdown percentage")
WIN_RATE = Gauge("quantumtrade_win_rate_percent", "Current win rate percentage")

# System metrics
CPU_USAGE = Gauge("quantumtrade_cpu_usage_percent", "CPU usage percentage")
MEMORY_USAGE = Gauge("quantumtrade_memory_usage_bytes", "Memory usage in bytes")
DISK_USAGE = Gauge("quantumtrade_disk_usage_percent", "Disk usage percentage")


class MetricsCollector:
    """Centralized metrics collection"""

    def __init__(self):
        self.start_time = time.time()

    def record_trade(self, action: str, symbol: str):
        """Record a trade execution"""
        TRADES_TOTAL.labels(action=action, symbol=symbol).inc()

    def update_portfolio_value(self, value: float):
        """Update portfolio value metric"""
        PORTFOLIO_VALUE.set(value)

    def update_pnl(self, pnl: float):
        """Update profit and loss metric"""
        PnL.set(pnl)

    def record_trade_latency(self, latency: float):
        """Record trade execution latency"""
        TRADE_LATENCY.observe(latency)

    def record_api_request(self, method: str, endpoint: str, status: int):
        """Record API request"""
        API_REQUESTS.labels(method=method, endpoint=endpoint, status=status).inc()

    def update_active_connections(self, count: int):
        """Update active connections count"""
        ACTIVE_CONNECTIONS.set(count)

    def record_strategy_signal(self, strategy: str, action: str):
        """Record strategy signal generation"""
        STRATEGY_SIGNALS.labels(strategy=strategy, action=action).inc()

    def update_performance_metrics(
        self, sharpe_ratio: float, max_drawdown: float, win_rate: float
    ):
        """Update performance metrics"""
        SHARPE_RATIO.set(sharpe_ratio)
        MAX_DRAWDOWN.set(max_drawdown)
        WIN_RATE.set(win_rate)

    def update_system_metrics(
        self, cpu_percent: float, memory_bytes: float, disk_percent: float
    ):
        """Update system metrics"""
        CPU_USAGE.set(cpu_percent)
        MEMORY_USAGE.set(memory_bytes)
        DISK_USAGE.set(disk_percent)

    def get_uptime(self) -> float:
        """Get application uptime in seconds"""
        return time.time() - self.start_time


# Global metrics collector instance
metrics_collector = MetricsCollector()


# Decorator for measuring function execution time
def measure_latency(func):
    """Decorator to measure function execution latency"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            latency = time.time() - start_time
            TRADE_LATENCY.observe(latency)

    return wrapper
