"""
Data service for QuantumTrade backend.
Handles live and historical data ingestion.
"""

import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
from ..core.supabase_client import get_supabase_client
from ..core.utils import parse_json_file


class DataService:
    """Service for handling live and historical data ingestion."""

    def __init__(self):
        self.supabase = get_supabase_client()

    async def fetch_historical_data(self, symbol: str, days: int = 30) -> pd.DataFrame:
        """Fetch historical market data for a symbol."""
        # This is a mock implementation - in reality, you would fetch from a data source
        # For now, we'll return mock data
        import numpy as np

        # Generate mock price data
        dates = pd.date_range(end=datetime.now(), periods=days, freq="D")
        prices = 100 + np.cumsum(np.random.randn(days) * 0.5)

        df = pd.DataFrame(
            {
                "timestamp": dates,
                "open": prices,
                "high": prices * 1.01,
                "low": prices * 0.99,
                "close": prices,
                "volume": np.random.randint(1000, 10000, days),
            }
        )

        return df

    async def fetch_live_data(self, symbol: str) -> Dict:
        """Fetch live market data for a symbol."""
        # This is a mock implementation - in reality, you would connect to a WebSocket
        import random

        # Generate mock live data
        price = 100 + random.uniform(-5, 5)
        return {
            "symbol": symbol,
            "price": price,
            "timestamp": datetime.utcnow().isoformat(),
            "volume": random.randint(1, 100),
        }

    def load_mock_data(self, file_path: str) -> pd.DataFrame:
        """Load mock data from a JSON file."""
        data = parse_json_file(file_path)
        if data:
            return pd.DataFrame(data)
        return pd.DataFrame()


# Global data service instance
data_service = DataService()
