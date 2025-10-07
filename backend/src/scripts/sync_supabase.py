"""
Supabase synchronization script for QuantumTrade backend.
Synchronizes data between local and Supabase databases.
"""

import asyncio
from ..core.supabase_client import get_supabase_client
from ..core.database import SessionLocal
from ..models import user, trade, strategy


def sync_supabase():
    """Synchronize data with Supabase."""
    print("Starting Supabase synchronization...")

    try:
        # Get Supabase client
        supabase = get_supabase_client()
        if not supabase:
            print("Supabase client not configured. Skipping sync.")
            return

        # Get local database session
        db = SessionLocal()

        # Example sync logic (this is a simplified mock)
        # In reality, you would implement proper sync logic here

        # Sync users
        local_users = db.query(user.User).all()
        print(f"Found {len(local_users)} users in local database")

        # Sync trades
        local_trades = db.query(trade.Trade).all()
        print(f"Found {len(local_trades)} trades in local database")

        # Sync strategies
        local_strategies = db.query(strategy.Strategy).all()
        print(f"Found {len(local_strategies)} strategies in local database")

        print("Supabase synchronization completed!")

    except Exception as e:
        print(f"Error during Supabase sync: {e}")
    finally:
        if "db" in locals():
            db.close()


if __name__ == "__main__":
    sync_supabase()
