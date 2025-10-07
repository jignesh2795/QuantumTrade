"""
Sync Service for QuantumTrade Platform
Handles bi-directional data synchronization between Supabase Cloud and local Postgres mirror
"""

import os
import time
import requests
import psycopg2
from datetime import datetime
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
LOCAL_DB_URL = os.getenv("LOCAL_DATABASE_URL")
SYNC_INTERVAL = int(os.getenv("SUPABASE_SYNC_INTERVAL", 15))  # Default to 15 minutes

# Supabase API headers
SUPABASE_HEADERS = {
    "apikey": SUPABASE_SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}


def get_supabase_data(table_name: str, limit: int = 1000) -> List[Dict[str, Any]]:
    """
    Fetch data from Supabase table

    Args:
        table_name: Name of the Supabase table
        limit: Maximum number of records to fetch

    Returns:
        List of records from the table
    """
    try:
        url = f"{SUPABASE_URL}/rest/v1/{table_name}?limit={limit}"
        response = requests.get(url, headers=SUPABASE_HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching data from Supabase table {table_name}: {e}")
        return []


def insert_local_data(table_name: str, data: List[Dict[str, Any]]) -> bool:
    """
    Insert data into local Postgres table

    Args:
        table_name: Name of the local table
        data: List of records to insert

    Returns:
        True if successful, False otherwise
    """
    if not data:
        return True

    try:
        conn = psycopg2.connect(LOCAL_DB_URL)
        cur = conn.cursor()

        # Get column names from first record
        columns = list(data[0].keys())
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))

        # Prepare insert query
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

        # Insert all records
        for record in data:
            values = [record.get(col) for col in columns]
            cur.execute(query, values)

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error inserting data into local table {table_name}: {e}")
        return False


def sync_table(table_name: str) -> bool:
    """
    Sync a single table from Supabase to local Postgres

    Args:
        table_name: Name of the table to sync

    Returns:
        True if successful, False otherwise
    """
    logger.info(f"Syncing table: {table_name}")

    # Fetch data from Supabase
    data = get_supabase_data(table_name)
    if not data:
        logger.info(f"No data found in Supabase table {table_name}")
        return True

    logger.info(f"Fetched {len(data)} records from Supabase table {table_name}")

    # Insert data into local database
    success = insert_local_data(table_name, data)
    if success:
        logger.info(
            f"Successfully synced {len(data)} records to local table {table_name}"
        )
    else:
        logger.error(f"Failed to sync data to local table {table_name}")

    return success


def sync_tables():
    """
    Sync all configured tables between Supabase and local Postgres
    """
    print(f"[{datetime.now()}] 🔄 Starting sync between Supabase ↔ Local Postgres...")

    # Tables to sync (this should be configurable in a real implementation)
    tables_to_sync = [
        "trades",
        "portfolio",
        "strategy_configurations",
        "strategy_executions",
    ]

    success_count = 0
    for table in tables_to_sync:
        try:
            if sync_table(table):
                success_count += 1
        except Exception as e:
            logger.error(f"Error syncing table {table}: {e}")

    print(
        f"✅ Sync complete: {success_count}/{len(tables_to_sync)} tables synced successfully"
    )


def main():
    """
    Main sync service loop
    """
    logger.info("Starting Supabase ↔ Local Postgres sync service...")

    while True:
        try:
            sync_tables()
            logger.info(f"Sleeping for {SYNC_INTERVAL} minutes...")
            time.sleep(SYNC_INTERVAL * 60)  # Convert minutes to seconds
        except KeyboardInterrupt:
            logger.info("Sync service stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in sync service: {e}")
            time.sleep(60)  # Wait 1 minute before retrying


if __name__ == "__main__":
    main()
