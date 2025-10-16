"""
Binance Exchange Implementation
Real API integration for live trading
"""
import asyncio
import hmac
import hashlib
import time
from typing import Dict, List, Optional
from datetime import datetime
import aiohttp
from backend.core.exchange_base import ExchangeBase, Candle, OrderResult
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class BinanceExchange(ExchangeBase):
    """
    Binance exchange implementation
    Real API integration for live trading
    """
    
    BASE_URL = "https://api.binance.com"
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        super().__init__(api_key, api_secret)
        self.testnet = testnet
        
        if testnet:
            self.BASE_URL = "https://testnet.binance.vision"
        
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def connect(self) -> bool:
        """Connect to Binance"""
        try:
            logger.info(f"🔌 Connecting to Binance {'Testnet' if self.testnet else 'Live'}...")
            
            # Create session
            self.session = aiohttp.ClientSession()
            
            # Test connection
            url = f"{self.BASE_URL}/api/v3/ping"
            async with self.session.get(url) as response:
                if response.status == 200:
                    self.is_connected = True
                    logger.info("✅ Connected to Binance successfully")
                    
                    # Test authentication
                    if self.api_key and self.api_secret:
                        account = await self.get_account_info()
                        if account:
                            logger.info(f"✅ Authentication successful | Account type: {account.get('accountType', 'N/A')}")
                    
                    return True
                else:
                    logger.error(f"❌ Failed to connect: HTTP {response.status}")
                    return False
        
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from Binance"""
        if self.session:
            await self.session.close()
        self.is_connected = False
        logger.info("Binance connection closed")
    
    def _generate_signature(self, params: Dict) -> str:
        """Generate HMAC SHA256 signature"""
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    async def _signed_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None
    ) -> Dict:
        """Make signed API request"""
        if not self.session:
            raise RuntimeError("Not connected to Binance")
        
        params = params or {}
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self._generate_signature(params)
        
        url = f"{self.BASE_URL}{endpoint}"
        headers = {'X-MBX-APIKEY': self.api_key}
        
        try:
            if method == "GET":
                async with self.session.get(url, params=params, headers=headers) as response:
                    return await response.json()
            elif method == "POST":
                async with self.session.post(url, params=params, headers=headers) as response:
                    return await response.json()
            elif method == "DELETE":
                async with self.session.delete(url, params=params, headers=headers) as response:
                    return await response.json()
        except Exception as e:
            logger.error(f"API request error: {e}")
            raise
    
    async def get_account_info(self) -> Dict:
        """Get account information"""
        return await self._signed_request("GET", "/api/v3/account")
    
    async def get_current_price(self, symbol: str) -> float:
        """Get current price for symbol"""
        try:
            url = f"{self.BASE_URL}/api/v3/ticker/price"
            params = {"symbol": symbol}
            
            async with self.session.get(url, params=params) as response:
                data = await response.json()
                return float(data['price'])
        
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            raise
    
    async def get_candles(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 100
    ) -> List[Candle]:
        """Get historical candles"""
        try:
            # Convert timeframe to Binance format
            interval_map = {
                "1m": "1m", "5m": "5m", "15m": "15m",
                "1h": "1h", "4h": "4h", "1d": "1d"
            }
            interval = interval_map.get(timeframe, "1h")
            
            url = f"{self.BASE_URL}/api/v3/klines"
            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            }
            
            async with self.session.get(url, params=params) as response:
                data = await response.json()
                
                candles = []
                for item in data:
                    candles.append(Candle(
                        timestamp=datetime.fromtimestamp(item[0] / 1000),
                        open=float(item[1]),
                        high=float(item[2]),
                        low=float(item[3]),
                        close=float(item[4]),
                        volume=float(item[5])
                    ))
                
                return candles
        
        except Exception as e:
            logger.error(f"Error getting candles for {symbol}: {e}")
            raise
    
    async def place_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: Optional[float] = None,
        order_type: str = "market"
    ) -> OrderResult:
        """Place an order"""
        try:
            params = {
                "symbol": symbol,
                "side": side.upper(),
                "type": order_type.upper(),
                "quantity": quantity
            }
            
            if order_type.lower() == "limit" and price:
                params["price"] = price
                params["timeInForce"] = "GTC"
            
            response = await self._signed_request("POST", "/api/v3/order", params)
            
            return OrderResult(
                order_id=str(response['orderId']),
                symbol=response['symbol'],
                side=response['side'].lower(),
                quantity=float(response['origQty']),
                price=float(response.get('price', 0)),
                status=response['status'].lower(),
                filled_quantity=float(response.get('executedQty', 0)),
                avg_fill_price=float(response.get('price', 0)) if response.get('price') else None,
                timestamp=datetime.fromtimestamp(response['transactTime'] / 1000)
            )
        
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            raise
    
    async def cancel_order(self, order_id: str, symbol: str) -> bool:
        """Cancel an order"""
        try:
            params = {
                "symbol": symbol,
                "orderId": order_id
            }
            
            response = await self._signed_request("DELETE", "/api/v3/order", params)
            return response['status'] == 'CANCELED'
        
        except Exception as e:
            logger.error(f"Error canceling order: {e}")
            return False
    
    async def get_order_status(self, order_id: str, symbol: str) -> OrderResult:
        """Get order status"""
        try:
            params = {
                "symbol": symbol,
                "orderId": order_id
            }
            
            response = await self._signed_request("GET", "/api/v3/order", params)
            
            return OrderResult(
                order_id=str(response['orderId']),
                symbol=response['symbol'],
                side=response['side'].lower(),
                quantity=float(response['origQty']),
                price=float(response.get('price', 0)),
                status=response['status'].lower(),
                filled_quantity=float(response.get('executedQty', 0)),
                avg_fill_price=float(response.get('price', 0)) if response.get('price') else None,
                timestamp=datetime.fromtimestamp(response['time'] / 1000)
            )
        
        except Exception as e:
            logger.error(f"Error getting order status: {e}")
            raise
    
    async def get_balance(self) -> Dict[str, float]:
        """Get account balance"""
        try:
            account = await self.get_account_info()
            
            total_btc = 0.0
            total_usdt = 0.0
            
            for balance in account['balances']:
                free = float(balance['free'])
                locked = float(balance['locked'])
                
                if balance['asset'] == 'USDT':
                    total_usdt = free + locked
                elif balance['asset'] == 'BTC':
                    total_btc = free + locked
            
            # For simplicity, return USDT balance
            # In production, convert all assets to base currency
            return {
                "cash": total_usdt,
                "total": total_usdt + (total_btc * await self.get_current_price("BTCUSDT")),
                "pnl": 0.0,  # Calculate from initial balance
                "pnl_pct": 0.0
            }
        
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            raise
    
    async def get_positions(self) -> List[Dict]:
        """Get open positions"""
        try:
            account = await self.get_account_info()
            positions = []
            
            for balance in account['balances']:
                free = float(balance['free'])
                locked = float(balance['locked'])
                total = free + locked
                
                if total > 0 and balance['asset'] != 'USDT':
                    symbol = f"{balance['asset']}USDT"
                    try:
                        current_price = await self.get_current_price(symbol)
                        
                        positions.append({
                            "symbol": symbol,
                            "quantity": total,
                            "avg_price": 0.0,  # Not available from spot API
                            "current_price": current_price,
                            "value": total * current_price,
                            "pnl": 0.0,
                            "pnl_pct": 0.0
                        })
                    except:
                        # Skip if can't get price
                        pass
            
            return positions
        
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            raise