"""
Simplified Backtest Loader for QuantumTrade Platform
"""

import csv
import random
from typing import List


def load_mock_data(file_path: str = "data/mock_prices.csv") -> List[float]:
    """
    Load mock price data from CSV file

    Args:
        file_path: Path to CSV file with mock price data

    Returns:
        List of price data points
    """
    try:
        data = []
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                data.append(float(row[1]))
        return data
    except FileNotFoundError:
        # Generate mock data if file doesn't exist
        return generate_mock_data(1000)
    except Exception as e:
        print(f"Error loading mock data: {e}")
        return generate_mock_data(1000)


def generate_mock_data(count: int = 1000) -> List[float]:
    """
    Generate mock price data

    Args:
        count: Number of data points to generate

    Returns:
        List of mock price data points
    """
    data = []
    base_price = 100.0
    for i in range(count):
        # Generate realistic price movements
        change = random.uniform(-2.0, 2.0)
        base_price += change
        data.append(round(base_price, 2))
    return data


def save_mock_data(data: List[float], file_path: str = "data/mock_prices.csv"):
    """
    Save mock data to CSV file

    Args:
        data: List of price data points
        file_path: Path to save CSV file
    """
    try:
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "price"])
            for i, price in enumerate(data):
                writer.writerow([i, price])
        print(f"Mock data saved to {file_path}")
    except Exception as e:
        print(f"Error saving mock data: {e}")
