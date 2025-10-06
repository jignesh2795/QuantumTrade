"""
Utility functions for data processing using numpy and pandas
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any

def calculate_portfolio_metrics(portfolio_data: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calculate portfolio metrics using numpy and pandas
    """
    if not portfolio_data:
        return {}
    
    # Convert to DataFrame for easier processing
    df = pd.DataFrame(portfolio_data)
    
    # Calculate metrics
    total_value = df['value'].sum()
    avg_price = df['price'].mean()
    max_position = df['value'].max()
    min_position = df['value'].min()
    
    return {
        'total_value': total_value,
        'average_price': avg_price,
        'max_position': max_position,
        'min_position': min_position,
        'position_count': len(df)
    }

def generate_price_series(initial_price: float, days: int = 30) -> List[float]:
    """
    Generate a price series using numpy
    """
    # Generate random walk
    returns = np.random.normal(0, 0.02, days)  # 2% daily volatility
    prices = [initial_price]
    
    for r in returns:
        prices.append(prices[-1] * (1 + r))
    
    return prices[1:]  # Remove initial price

if __name__ == "__main__":
    # Example usage
    sample_portfolio = [
        {"symbol": "AAPL", "quantity": 10, "price": 150.00, "value": 1500.00},
        {"symbol": "GOOGL", "quantity": 5, "price": 2500.00, "value": 12500.00},
        {"symbol": "TSLA", "quantity": 20, "price": 200.00, "value": 4000.00}
    ]
    
    metrics = calculate_portfolio_metrics(sample_portfolio)
    print("Portfolio Metrics:", metrics)
    
    price_series = generate_price_series(150.0, 10)
    print("Price Series:", price_series)