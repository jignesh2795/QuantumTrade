"""
Supabase client module for QuantumTrade backend.
Handles Supabase API, Realtime, and Auth integration.
"""

import os
from supabase import create_client, Client
from .config import Config

# Initialize Supabase client
supabase: Client = None

if Config.SUPABASE_URL and Config.SUPABASE_ANON_KEY:
    supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_ANON_KEY)


def get_supabase_client():
    """Returns the Supabase client instance."""
    return supabase
