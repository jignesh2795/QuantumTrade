"""
Test settings configuration
"""
import pytest
from backend.utils.settings import Settings


def test_settings_initialization():
    """Test settings initialization"""
    settings = Settings()
    assert settings.TRADING_MODE in ["paper", "live"]
    assert settings.INITIAL_CAPITAL > 0
    assert settings.MAX_POSITION_SIZE > 0
    assert settings.MAX_POSITION_SIZE <= 1.0


def test_settings_validation():
    """Test settings validation"""
    settings = Settings()
    settings.TRADING_MODE = "paper"
    assert settings.validate() == True


def test_directory_creation():
    """Test that required directories are created"""
    settings = Settings()
    assert settings.DATABASE_DIR.exists()
    assert settings.LOGS_DIR.exists()
    assert settings.CONFIG_DIR.exists()