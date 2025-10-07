"""
Strategy Agent for QuantumTrade Platform
Generates buy/sell/hold signals based on various technical indicators and strategies
"""

import random
import logging
from typing import Dict, List, Optional
from datetime import datetime
import math
from src.core.model_server import load_model, predict
import pandas as pd
import os

MODEL_NAME = os.getenv("STRATEGY_MODEL", "rf_v1")


class StrategyAgent:
    def __init__(self, symbol="BTCUSDT"):
        self.model = None
        self.symbol = symbol
        try:
            self.model = load_model(MODEL_NAME)
        except Exception:
            self.model = None

    def generate_signal(self, df: pd.DataFrame):
        # df must contain 'price' column (history)
        if self.model:
            pred = predict(self.model, df)
            if pred == 1:
                return {"symbol": self.symbol, "signal": "BUY"}
            else:
                return {"symbol": self.symbol, "signal": "SELL"}
        # fallback: naive
        last = df["price"].iloc[-1]
        prev = df["price"].iloc[-2]
        return {"symbol": self.symbol, "signal": "BUY" if last > prev else "SELL"}
