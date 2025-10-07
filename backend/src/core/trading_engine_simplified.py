"""
Simplified Trading Engine for QuantumTrade Platform
"""


def run_strategy(symbol: str, data: list[float]):
    """
    Run a simple trading strategy based on price movements

    Args:
        symbol: Trading symbol
        data: List of price data points

    Returns:
        List of trading signals
    """
    signals = []
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            signals.append("BUY")
        elif data[i] < data[i - 1]:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return signals


def calculate_pnl(trades: list) -> float:
    """
    Calculate profit and loss from a list of trades

    Args:
        trades: List of trade records

    Returns:
        Total PnL value
    """
    total_pnl = 0.0
    for trade in trades:
        if "pnl" in trade:
            total_pnl += trade["pnl"]
    return total_pnl
