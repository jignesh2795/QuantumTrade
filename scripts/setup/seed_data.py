"""
QuantumTrade Database Seed Script
Populates database with initial data for testing and development
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Add backend src to path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "..", "backend", "src")
)

from database.seed_data import seed_all_data


def seed_database():
    """Seed database with sample data"""
    try:
        print("Seeding database with sample data...")
        result = seed_all_data()
        print(f"Database seeding completed successfully!")
        print(f"Seeded data: {result}")
    except Exception as e:
        print(f"Error seeding database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    seed_database()
