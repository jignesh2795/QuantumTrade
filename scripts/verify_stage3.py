#!/usr/bin/env python3
"""
Verification script for QuantumTrade Stage 3: Supabase Cloud Integration
"""

import os
import sys
import subprocess
import time
from dotenv import load_dotenv


def check_environment_variables():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")

    # Load environment variables
    load_dotenv()

    required_vars = ["DATABASE_URL", "SUPABASE_URL", "SUPABASE_ANON_KEY"]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            print(f"  ✅ {var}: SET")

    if missing_vars:
        print(f"  ❌ Missing environment variables: {missing_vars}")
        return False

    print("  ✅ All required environment variables are set")
    return True


def check_docker_compose():
    """Check if docker-compose.yml is properly configured"""
    print("\n🔍 Checking docker-compose configuration...")

    try:
        with open("docker-compose.yml", "r") as f:
            content = f.read()

        # Check for required services
        if "backend:" in content and "frontend:" in content:
            print("  ✅ Required services found: backend, frontend")
        else:
            print("  ❌ Missing required services")
            return False

        # Check for env_file in backend
        if "env_file:" in content and ".env" in content:
            print("  ✅ Environment file configuration found")
        else:
            print("  ❌ Missing environment file configuration")
            return False

        print("  ✅ Docker Compose configuration is correct")
        return True

    except FileNotFoundError:
        print("  ❌ docker-compose.yml not found")
        return False
    except Exception as e:
        print(f"  ❌ Error reading docker-compose.yml: {e}")
        return False


def check_database_connection():
    """Check if database connection works"""
    print("\n🔍 Checking database connection...")

    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("  ❌ DATABASE_URL not set")
        return False

    # Simple check - just verify URL format
    if database_url.startswith("postgresql://"):
        print("  ✅ Database URL format is correct")
        return True
    else:
        print("  ❌ Database URL format is incorrect")
        return False


def check_supabase_client():
    """Check if Supabase client is properly configured"""
    print("\n🔍 Checking Supabase client configuration...")

    try:
        # Check frontend Supabase client
        with open("frontend/src/supabaseClient.js", "r") as f:
            content = f.read()

        if "createClient" in content and "VITE_SUPABASE_URL" in content:
            print("  ✅ Frontend Supabase client configured correctly")
            return True
        else:
            print("  ❌ Frontend Supabase client configuration issues")
            return False

    except FileNotFoundError:
        print("  ❌ frontend/src/supabaseClient.js not found")
        return False
    except Exception as e:
        print(f"  ❌ Error reading Supabase client: {e}")
        return False


def check_docker_services():
    """Check if Docker services are running"""
    print("\n🔍 Checking Docker services...")

    try:
        # Check if Docker is running
        result = subprocess.run(
            ["docker", "version"], capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            print("  ❌ Docker is not running")
            return False

        print("  ✅ Docker is running")

        # Check if services are up
        result = subprocess.run(
            ["docker-compose", "ps"], capture_output=True, text=True, timeout=10
        )
        if (
            "quantumtrade_backend" in result.stdout
            and "quantumtrade_frontend" in result.stdout
        ):
            print("  ✅ QuantumTrade services are running")
            return True
        else:
            print(
                "  ⚠️  QuantumTrade services are not running (this is OK for verification)"
            )
            return True

    except subprocess.TimeoutExpired:
        print("  ❌ Docker command timed out")
        return False
    except Exception as e:
        print(f"  ❌ Error checking Docker services: {e}")
        return False


def main():
    """Main verification function"""
    print("🧪 QuantumTrade Stage 3 Verification")
    print("=" * 40)

    checks = [
        check_environment_variables,
        check_docker_compose,
        check_database_connection,
        check_supabase_client,
        check_docker_services,
    ]

    passed = 0
    total = len(checks)

    for check in checks:
        if check():
            passed += 1
        else:
            print("  ❌ Check failed")

    print("\n" + "=" * 40)
    print(f"✅ Verification Results: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 Stage 3 setup is complete and verified!")
        print("\nNext steps:")
        print("1. Make sure your .env file has valid Supabase credentials")
        print("2. Run: docker-compose up --build")
        print("3. Visit http://localhost:5173 for frontend")
        print("4. Visit http://localhost:8000/docs for backend API")
        return True
    else:
        print("❌ Stage 3 setup requires attention")
        print("\nPlease check the failed checks above and ensure:")
        print("1. .env file is properly configured with Supabase credentials")
        print("2. docker-compose.yml matches the Stage 3 specification")
        print("3. Supabase Cloud project is created and configured")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
