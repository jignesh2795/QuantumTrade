"""
Test paper exchange functionality
"""
import pytest
import asyncio
from backend.core.paper_exchange import PaperExchange


@pytest.mark.asyncio
async def test_paper_exchange_connection():
    """Test paper exchange connection"""
    exchange = PaperExchange(initial_capital=10000)
    result = await exchange.connect()
    assert result == True
    assert exchange.is_connected == True
    await exchange.disconnect()


@pytest.mark.asyncio
async def test_get_current_price():
    """Test getting current price"""
    exchange = PaperExchange()
    await exchange.connect()
    price = await exchange.get_current_price("BTCUSDT")
    assert price > 0
    await exchange.disconnect()


@pytest.mark.asyncio
async def test_place_buy_order():
    """Test placing a buy order"""
    exchange = PaperExchange(initial_capital=10000)
    await exchange.connect()
    
    result = await exchange.place_order(
        symbol="BTCUSDT",
        side="buy",
        quantity=0.1,
        order_type="market"
    )
    
    assert result.status == "filled"
    assert result.side == "buy"
    assert result.quantity == 0.1
    
    await exchange.disconnect()


@pytest.mark.asyncio
async def test_place_sell_order():
    """Test placing a sell order"""
    exchange = PaperExchange(initial_capital=10000)
    await exchange.connect()
    
    # First buy
    await exchange.place_order("BTCUSDT", "buy", 0.1, order_type="market")
    
    # Then sell
    result = await exchange.place_order("BTCUSDT", "sell", 0.1, order_type="market")
    
    assert result.status == "filled"
    assert result.side == "sell"
    
    await exchange.disconnect()


@pytest.mark.asyncio
async def test_insufficient_balance():
    """Test order rejection due to insufficient balance"""
    exchange = PaperExchange(initial_capital=100)
    await exchange.connect()
    
    result = await exchange.place_order(
        symbol="BTCUSDT",
        side="buy",
        quantity=10.0,  # Too large
        order_type="market"
    )
    
    assert result.status == "rejected"
    await exchange.disconnect()


@pytest.mark.asyncio
async def test_get_balance():
    """Test getting account balance"""
    exchange = PaperExchange(initial_capital=10000)
    await exchange.connect()
    
    balance = await exchange.get_balance()
    
    assert balance['cash'] == 10000
    assert balance['total'] == 10000
    assert balance['pnl'] == 0
    
    await exchange.disconnect()