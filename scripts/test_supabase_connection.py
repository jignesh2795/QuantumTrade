#!/usr/bin/env python3
"""
Script to test Supabase connection using the configured environment variables
"""

import os
import sys

# Add the backend directory to the path so we can import the supabase client
backend_path = os.path.join(os.path.dirname(__file__), "..", "backend")
sys.path.insert(0, backend_path)

# Load environment variables
from dotenv import load_dotenv

load_dotenv()


def test_supabase_connection():
    """Test the Supabase connection using environment variables"""

    # Get the Supabase configuration
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
    supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    database_url = os.getenv("DATABASE_URL")

    print("🔍 Testing Supabase Configuration...")
    print("=" * 50)

    # Check if environment variables are set
    if not supabase_url:
        print("❌ SUPABASE_URL is not set")
        return False

    if not supabase_anon_key:
        print("❌ SUPABASE_ANON_KEY is not set")
        return False

    if not supabase_service_role_key:
        print("❌ SUPABASE_SERVICE_ROLE_KEY is not set")
        return False

    if not database_url:
        print("❌ DATABASE_URL is not set")
        return False

    print(f"✅ SUPABASE_URL: {supabase_url}")
    print(
        f"✅ SUPABASE_ANON_KEY: {'*' * min(50, len(supabase_anon_key))}{'...' if len(supabase_anon_key) > 50 else ''}"
    )
    print(
        f"✅ SUPABASE_SERVICE_ROLE_KEY: {'*' * min(50, len(supabase_service_role_key))}{'...' if len(supabase_service_role_key) > 50 else ''}"
    )
    print(
        f"✅ DATABASE_URL: {database_url.split('@')[-1] if database_url else 'Not set'}"
    )

    # Test database connection
    try:
        print("\n🔌 Testing Database Connection...")
        # Import after setting up the path
        from src.database.supabase_client import (
            test_supabase_connection as test_db_connection,
        )

        if test_db_connection():
            print("✅ Database connection successful!")
        else:
            print("❌ Database connection failed!")
            return False
    except ImportError as e:
        print(f"⚠️  Warning: Could not import Supabase client - {e}")
        print(
            "✅ Environment variables are set correctly, but skipping database connection test"
        )
        return True
    except Exception as e:
        print(f"❌ Database connection test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False

    print("\n🎉 All Supabase configurations are set correctly!")
    return True


if __name__ == "__main__":
    success = test_supabase_connection()
    sys.exit(0 if success else 1)
