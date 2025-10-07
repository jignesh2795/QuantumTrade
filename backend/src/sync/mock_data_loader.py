"""
Mock Data Loader for QuantumTrade Platform
Generates mock market and backtesting data for local development
"""

import os
import random
import psycopg2
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Environment variables
LOCAL_DB_URL = os.getenv("LOCAL_DATABASE_URL")
MOCK_DATA_COUNT = int(os.getenv("MOCK_DATA_COUNT", 5000))
MOCK_DATA_SEED = int(os.getenv("MOCK_DATA_SEED", 42))

# Sample data for mock generation
SYMBOLS = ["AAPL", "TSLA", "BTC", "ETH", "GOOGL", "AMZN", "MSFT", "NFLX", "NVDA", "AMD"]
TRADE_TYPES = ["BUY", "SELL"]
STRATEGIES = ["moving_average", "rsi", "bollinger_bands", "macd"]

def create_mock_tables():
    """
    Create mock data tables in local database if they don't exist
    """
    try:
        conn = psycopg2.connect(LOCAL_DB_URL)
        cur = conn.cursor()
        
        # Create mock_trades table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mock_trades (
                id SERIAL PRIMARY KEY,
                symbol TEXT,
                trade_type TEXT,
                price FLOAT,
                volume INT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create mock_portfolio table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mock_portfolio (
                id SERIAL PRIMARY KEY,
                symbol TEXT,
                quantity FLOAT,
                avg_price FLOAT,
                current_price FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create mock_strategy_executions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mock_strategy_executions (
                id SERIAL PRIMARY KEY,
                strategy_name TEXT,
                symbol TEXT,
                signal TEXT,
                confidence FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Mock tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating mock tables: {e}")
        return False

def generate_mock_trades(count: int) -> list:
    """
    Generate mock trade data
    
    Args:
        count: Number of mock trades to generate
        
    Returns:
        List of mock trade records
    """
    random.seed(MOCK_DATA_SEED)
    trades = []
    
    for i in range(count):
        trade = {
            "symbol": random.choice(SYMBOLS),
            "trade_type": random.choice(TRADE_TYPES),
            "price": round(random.uniform(50, 500), 2),
            "volume": random.randint(1, 1000),
            "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 1440))  # Up to 24 hours ago
        }
        trades.append(trade)
    
    return trades

def generate_mock_portfolio(count: int) -> list:
    """
    Generate mock portfolio data
    
    Args:
        count: Number of mock portfolio entries to generate
        
    Returns:
        List of mock portfolio records
    """
    random.seed(MOCK_DATA_SEED)
    portfolio = []
    
    for i in range(count):
        entry = {
            "symbol": random.choice(SYMBOLS),
            "quantity": round(random.uniform(1, 100), 4),
            "avg_price": round(random.uniform(50, 500), 2),
            "current_price": round(random.uniform(50, 500), 2),
            "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 1440))
        }
        portfolio.append(entry)
    
    return portfolio

def generate_mock_strategy_executions(count: int) -> list:
    """
    Generate mock strategy execution data
    
    Args:
        count: Number of mock strategy executions to generate
        
    Returns:
        List of mock strategy execution records
    """
    random.seed(MOCK_DATA_SEED)
    executions = []
    
    for i in range(count):
        execution = {
            "strategy_name": random.choice(STRATEGIES),
            "symbol": random.choice(SYMBOLS),
            "signal": random.choice(["BUY", "SELL", "HOLD"]),
            "confidence": round(random.uniform(0.5, 1.0), 4),
            "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 1440))
        }
        executions.append(execution)
    
    return executions

def insert_mock_data(table_name: str, data: list) -> bool:
    """
    Insert mock data into local database
    
    Args:
        table_name: Name of the table to insert data into
        data: List of records to insert
        
    Returns:
        True if successful, False otherwise
    """
    if not data:
        return True
        
    try:
        conn = psycopg2.connect(LOCAL_DB_URL)
        cur = conn.cursor()
        
        if table_name == "mock_trades":
            query = """
                INSERT INTO mock_trades (symbol, trade_type, price, volume, timestamp)
                VALUES (%(symbol)s, %(trade_type)s, %(price)s, %(volume)s, %(timestamp)s)
            """
        elif table_name == "mock_portfolio":
            query = """
                INSERT INTO mock_portfolio (symbol, quantity, avg_price, current_price, timestamp)
                VALUES (%(symbol)s, %(quantity)s, %(avg_price)s, %(current_price)s, %(timestamp)s)
            """
        elif table_name == "mock_strategy_executions":
            query = """
                INSERT INTO mock_strategy_executions (strategy_name, symbol, signal, confidence, timestamp)
                VALUES (%(strategy_name)s, %(symbol)s, %(signal)s, %(confidence)s, %(timestamp)s)
            """
        else:
            logger.error(f"Unknown table name: {table_name}")
            return False
            
        # Insert all records
        for record in data:
            cur.execute(query, record)
            
        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"Inserted {len(data)} records into {table_name}")
        return True
    except Exception as e:
        logger.error(f"Error inserting mock data into {table_name}: {e}")
        return False

def load_mock_data():
    """
    Load mock data into local database
    """
    logger.info("📊 Generating and seeding mock data into local DB...")
    
    # Create tables first
    if not create_mock_tables():
        logger.error("Failed to create mock tables")
        return False
    
    # Generate and insert mock trades
    mock_trades = generate_mock_trades(MOCK_DATA_COUNT)
    if not insert_mock_data("mock_trades", mock_trades):
        logger.error("Failed to insert mock trades")
        return False
    
    # Generate and insert mock portfolio data
    mock_portfolio = generate_mock_portfolio(MOCK_DATA_COUNT // 10)  # Fewer portfolio entries
    if not insert_mock_data("mock_portfolio", mock_portfolio):
        logger.error("Failed to insert mock portfolio")
        return False
    
    # Generate and insert mock strategy executions
    mock_executions = generate_mock_strategy_executions(MOCK_DATA_COUNT // 5)  # Fewer execution entries
    if not insert_mock_data("mock_strategy_executions", mock_executions):
        logger.error("Failed to insert mock strategy executions")
        return False
    
    logger.info("✅ Mock data inserted successfully.")
    return True

if __name__ == "__main__":
    load_mock_data()