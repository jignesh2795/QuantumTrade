"""
QuantumTrade Database Setup Script
Initializes the database schema and tables
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend src to path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "backend", "src")
)

from database.connection import init_database
from database.models import Base


def setup_database():
    """Setup database tables"""
    try:
        print("Initializing database...")
        init_database()
        print("Database setup completed successfully!")
    except Exception as e:
        print(f"Error setting up database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_database()
