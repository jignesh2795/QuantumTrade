"""
Pytest configuration and fixtures
"""
import pytest
import asyncio
from backend.utils.settings import Settings


@pytest.fixture
def settings():
    """Fixture for settings"""
    return Settings()


@pytest.fixture
def event_loop():
    """Create an event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()