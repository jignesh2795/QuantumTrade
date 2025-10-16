"""
pytest configuration file
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))


# pytest configuration
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )