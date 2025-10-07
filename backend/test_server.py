#!/usr/bin/env python3
"""
Test if the QuantumTrade server can be imported and started
"""


def test_server_import():
    """Test importing the server"""
    try:
        from src.api.server import app

        print("✓ Server module imported successfully")
        print(f"  App title: {app.title}")
        print(f"  App version: {app.version}")
        return True
    except Exception as e:
        print(f"✗ Failed to import server module: {e}")
        return False


def test_routes():
    """Test if routes are registered"""
    try:
        from src.api.server import app

        print(f"✓ App has {len(app.routes)} routes registered")
        # Print first few routes
        for i, route in enumerate(app.routes[:5]):
            print(f"  Route {i+1}: {route.path} [{route.methods}]")
        return True
    except Exception as e:
        print(f"✗ Failed to check routes: {e}")
        return False


def test_core_components():
    """Test importing core components"""
    components = [
        ("realtime_feed", "from src.core.realtime_feed import BINANCE_WS"),
        ("backtester", "from src.core.backtester import run_backtest"),
        ("model_trainer", "from src.core.model_trainer import train_model"),
        ("model_server", "from src.core.model_server import load_model"),
    ]

    failed = []
    for name, import_stmt in components:
        try:
            exec(import_stmt)
            print(f"✓ {name} imported successfully")
        except Exception as e:
            print(f"✗ {name} import failed: {e}")
            failed.append(name)

    return len(failed) == 0


def main():
    """Main test function"""
    print("QuantumTrade Server Test")
    print("=" * 30)

    server_ok = test_server_import()
    routes_ok = test_routes()
    components_ok = test_core_components()

    print("\n" + "=" * 30)
    print("Test Results:")
    print(f"  Server Import: {'✓ PASS' if server_ok else '✗ FAIL'}")
    print(f"  Routes: {'✓ PASS' if routes_ok else '✗ FAIL'}")
    print(f"  Core Components: {'✓ PASS' if components_ok else '✗ FAIL'}")

    overall = server_ok and routes_ok and components_ok
    print(f"\nOverall: {'✓ ALL TESTS PASSED' if overall else '✗ SOME TESTS FAILED'}")

    if overall:
        print("\n🎉 QuantumTrade server is working correctly!")
        print("You can now run the application with:")
        print("  uvicorn src.api.server:app --host 0.0.0.0 --port 8000")
    else:
        print("\n❌ QuantumTrade server has issues.")
        print("Please check the error messages above.")

    return overall


if __name__ == "__main__":
    main()
