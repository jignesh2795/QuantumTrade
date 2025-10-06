import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# pytest configuration
pytest_plugins = []

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )