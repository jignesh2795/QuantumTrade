"""
Simplified Supabase Client for QuantumTrade Platform
"""

from supabase import create_client
import os

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_supabase_client():
    """
    Get Supabase client instance

    Returns:
        Supabase client instance
    """
    return supabase


def test_supabase_connection():
    """
    Test Supabase connection

    Returns:
        Connection test result
    """
    try:
        # Simple health check
        response = supabase.rpc("version").execute()
        return True
    except Exception as e:
        print(f"Supabase connection test failed: {e}")
        return False
