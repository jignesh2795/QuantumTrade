#!/usr/bin/env python3
"""
Script to initialize Supabase Cloud database tables
"""

import sys
import os
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))


def init_supabase_tables():
    """Initialize Supabase tables"""
    try:
        # Load environment variables
        load_dotenv()

        # Import database modules
        from backend.src.database import models, connection
        from backend.src.database.init_supabase_tables import create_supabase_tables

        print("🚀 Initializing Supabase Cloud database tables...")

        # Create SQLAlchemy tables
        print("  Creating core database tables...")
        models.Base.metadata.create_all(bind=connection.engine)
        print("  ✅ Core tables created")

        # Create Supabase-specific tables
        print("  Creating Supabase-specific tables...")
        create_supabase_tables()
        print("  ✅ Supabase tables created")

        print("\n🎉 Database initialization complete!")
        print("\nNext steps:")
        print("1. Visit your Supabase Dashboard → Table Editor to verify tables")
        print("2. Run the application with: docker-compose up")

        return True

    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False


if __name__ == "__main__":
    success = init_supabase_tables()
    sys.exit(0 if success else 1)
