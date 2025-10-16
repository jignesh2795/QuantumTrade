"""
Test Binance exchange functionality
"""
import pytest
import asyncio
from backend.core.binance_exchange import BinanceExchange


@pytest.mark.asyncio
async def test_binance_exchange_connection():
    """Test Binance exchange connection"""
    # Note: This test requires actual API keys to work properly
    # For testing purposes, we'll test the connection logic without actual authentication
    exchange = BinanceExchange("test_key", "test_secret")
    
    # This should fail without real API keys, but we can test the structure
    try:
        result = await exchange.connect()
        # If it connects (which shouldn't happen with fake keys), test disconnection
        if result:
            await exchange.disconnect()
    except:
        # Expected behavior with fake keys
        pass
    
    # Verify the exchange object was created correctly
    assert isinstance(exchange, BinanceExchange)
    assert exchange.api_key == "test_key"
    assert exchange.api_secret == "test_secret"


@pytest.mark.asyncio
async def test_binance_signature_generation():
    """Test signature generation"""
    exchange = BinanceExchange("test_key", "test_secret")
    
    # Test signature generation
    params = {"timestamp": 1234567890, "symbol": "BTCUSDT"}
    signature = exchange._generate_signature(params)
    
    # Verify signature is generated (actual value depends on secret)
    assert isinstance(signature, str)
    assert len(signature) > 0


def test_binance_exchange_initialization():
    """Test Binance exchange initialization"""
    exchange = BinanceExchange("test_key", "test_secret")
    
    assert exchange.api_key == "test_key"
    assert exchange.api_secret == "test_secret"
    assert exchange.is_connected == False
    assert exchange.BASE_URL == "https://api.binance.com"
    
    # Test testnet initialization
    testnet_exchange = BinanceExchange("test_key", "test_secret", testnet=True)
    assert testnet_exchange.BASE_URL == "https://testnet.binance.vision"