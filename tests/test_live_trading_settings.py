"""
Test live trading settings validation
"""
import pytest
from unittest.mock import patch
from backend.utils.settings import Settings


def test_paper_mode_without_keys():
    """Test paper mode works without API keys"""
    settings = Settings()
    settings.TRADING_MODE = "paper"
    settings.API_KEY = ""
    settings.API_SECRET = ""
    
    # Should not raise an exception
    assert settings.validate() == True


def test_live_mode_without_keys():
    """Test live mode requires API keys"""
    settings = Settings()
    settings.TRADING_MODE = "live"
    settings.API_KEY = ""
    settings.API_SECRET = ""
    
    # Should raise an exception
    with pytest.raises(ValueError, match="API_KEY and API_SECRET required for live trading"):
        settings.validate()


def test_live_mode_with_keys():
    """Test live mode works with API keys"""
    settings = Settings()
    settings.TRADING_MODE = "live"
    settings.API_KEY = "test_key"
    settings.API_SECRET = "test_secret"
    
    # Mock the input to avoid interactive prompt
    with patch('builtins.input', return_value='YES'):
        # Should not raise an exception
        assert settings.validate() == True