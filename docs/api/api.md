# API Documentation

This document provides detailed information about the QuantumTrade API endpoints.

## Overview

The QuantumTrade API is built using FastAPI and provides RESTful endpoints for all trading operations. The API follows standard REST conventions and includes automatic OpenAPI documentation.

## Base URL

-   **Development**: http://localhost:8000
-   **Production**: https://api.yourdomain.com

## Authentication

Most endpoints require authentication using JWT tokens obtained through Supabase Auth.

### Headers

```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

## API Endpoints

### Health Check

```
GET /health
```

Returns the health status of the API.

**Response:**

```json
{
    "status": "ok",
    "uptime": "2h30m"
}
```

### Agent Management

```
GET /agents
```

List all available trading agents.

**Response:**

```json
{
    "agents": [
        "data_agent",
        "strategy_agent",
        "risk_agent",
        "portfolio",
        "execution_agent"
    ]
}
```

### Market Data

```
GET /data/price?symbol=BTC-USD
```

Get current price for a symbol.

**Parameters:**

-   symbol (string, required): Trading symbol

**Response:**

```json
{
    "symbol": "BTC-USD",
    "price": 45000.0,
    "timestamp": "2023-10-01T12:00:00Z"
}
```

```
GET /data/historical?symbol=BTC-USD&days=30
```

Get historical market data.

**Parameters:**

-   symbol (string, required): Trading symbol
-   days (integer, optional, default=30): Number of days of history

**Response:**

```json
{
    "symbol": "BTC-USD",
    "data": [
        {
            "timestamp": "2023-10-01T12:00:00Z",
            "open": 45000.0,
            "high": 45500.0,
            "low": 44800.0,
            "close": 45200.0,
            "volume": 125000000
        }
    ]
}
```

### Strategy Operations

```
GET /strategy/signal?symbol=BTC-USD
```

Generate trading signal for a symbol.

**Parameters:**

-   symbol (string, required): Trading symbol

**Response:**

```json
{
    "symbol": "BTC-USD",
    "signal": "BUY",
    "confidence": 0.85,
    "strategy": "moving_average",
    "timestamp": "2023-10-01T12:00:00Z"
}
```

### Portfolio Management

```
GET /portfolio/list
```

List all portfolio positions.

**Response:**

```json
{
    "positions": [
        {
            "symbol": "BTC-USD",
            "size": 0.5,
            "avg_price": 42000.0,
            "current_price": 45000.0,
            "pnl": 1500.0
        }
    ]
}
```

```
POST /portfolio/add
```

Add a position to the portfolio.

**Request Body:**

```json
{
    "symbol": "BTC-USD",
    "size": 0.5,
    "price": 42000.0
}
```

**Response:**

```json
{
    "status": "success",
    "message": "Position added successfully"
}
```

### Risk Management

```
GET /risk/assess?position_size=1000&account_balance=10000
```

Assess risk for a proposed position.

**Parameters:**

-   position_size (float, required): Size of proposed position
-   account_balance (float, required): Current account balance

**Response:**

```json
{
    "position_size": 1000,
    "account_balance": 10000,
    "risk_percent": 10.0,
    "status": "OK",
    "reason": "Risk within acceptable limits"
}
```

### Trade Execution

```
POST /execute/trade
```

Execute a trade.

**Request Body:**

```json
{
    "symbol": "BTC-USD",
    "action": "BUY",
    "size": 0.1
}
```

**Response:**

```json
{
    "status": "success",
    "message": "Trade executed successfully",
    "trade_id": "1234567890"
}
```

### Supabase Integration Endpoints

#### Trade History

```
GET /trades/history
```

Get user's trade history from Supabase.

**Headers:**

-   X-User-Id (string, required): User ID

**Parameters:**

-   symbol (string, optional): Filter by symbol
-   days (integer, optional, default=30): Number of days
-   limit (integer, optional, default=100): Maximum results

**Response:**

```json
{
    "status": "success",
    "trades": [
        {
            "id": "1234567890",
            "user_id": "user123",
            "asset": "BTC-USD",
            "trade_type": "BUY",
            "amount": 0.1,
            "price": 45000.0,
            "timestamp": "2023-10-01T12:00:00Z"
        }
    ],
    "count": 1
}
```

#### Portfolio Management

```
GET /portfolio/supabase
```

Get user's portfolio from Supabase.

**Headers:**

-   X-User-Id (string, required): User ID

**Response:**

```json
{
    "status": "success",
    "portfolio": [
        {
            "id": "1234567890",
            "user_id": "user123",
            "asset": "BTC-USD",
            "quantity": 0.5,
            "avg_price": 42000.0
        }
    ]
}
```

#### Strategy Configuration

```
GET /strategies/config
```

Get user's strategy configurations.

**Headers:**

-   X-User-Id (string, required): User ID

**Response:**

```json
{
    "status": "success",
    "configurations": [
        {
            "id": "1234567890",
            "user_id": "user123",
            "strategy_name": "moving_average",
            "asset": "BTC-USD",
            "is_active": true,
            "config": {
                "period": 20,
                "confidence_threshold": 0.8
            }
        }
    ]
}
```

```
POST /strategies/config
```

Update strategy configuration.

**Headers:**

-   X-User-Id (string, required): User ID

**Request Body:**

```json
{
    "strategy_name": "moving_average",
    "asset": "BTC-USD",
    "is_active": true,
    "config": {
        "period": 20,
        "confidence_threshold": 0.8
    }
}
```

**Response:**

```json
{
    "status": "success",
    "message": "Configuration updated successfully"
}
```

### Backtesting

```
POST /backtest/run
```

Run a backtest.

**Request Body:**

```json
{
    "symbol": "BTC-USD",
    "strategy": "moving_average",
    "start_date": "2023-01-01",
    "end_date": "2023-10-01",
    "initial_capital": 10000
}
```

**Response:**

```json
{
    "status": "success",
    "results": {
        "total_return": 15.5,
        "sharpe_ratio": 1.2,
        "max_drawdown": 5.2,
        "win_rate": 0.65,
        "total_trades": 45
    }
}
```

## Error Handling

### Common Error Responses

**400 Bad Request**

```json
{
    "detail": "Invalid request parameters"
}
```

**401 Unauthorized**

```json
{
    "detail": "Missing or invalid authentication token"
}
```

**403 Forbidden**

```json
{
    "detail": "Insufficient permissions"
}
```

**404 Not Found**

```json
{
    "detail": "Resource not found"
}
```

**500 Internal Server Error**

```json
{
    "detail": "Internal server error"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

-   100 requests per minute per IP
-   1000 requests per hour per user

Exceeding limits will result in a 429 Too Many Requests response.

## Data Models

### Trade

```json
{
    "id": "string",
    "user_id": "string",
    "asset": "string",
    "trade_type": "BUY|SELL",
    "amount": "number",
    "price": "number",
    "timestamp": "datetime"
}
```

### Portfolio Position

```json
{
    "id": "string",
    "user_id": "string",
    "asset": "string",
    "quantity": "number",
    "avg_price": "number"
}
```

### Strategy Configuration

```json
{
    "id": "string",
    "user_id": "string",
    "strategy_name": "string",
    "asset": "string",
    "is_active": "boolean",
    "config": "object",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

## WebSockets (Real-time Updates)

### Trade Updates

```
WebSocket: /ws/trades
```

Receive real-time trade updates.

### Portfolio Updates

```
WebSocket: /ws/portfolio
```

Receive real-time portfolio updates.

## Monitoring Endpoints

### Metrics

```
GET /metrics
```

Prometheus metrics endpoint.

### Health

```
GET /health
```

Health check endpoint.

## CORS Policy

The API allows CORS requests from:

-   http://localhost:5173 (development)
-   https://yourdomain.com (production)

## Versioning

The API follows semantic versioning. Breaking changes will result in a new major version.

## Changelog

### v1.0.0

-   Initial release
-   Core trading functionality
-   Supabase integration
-   Backtesting capabilities

### v1.1.0

-   Added real-time updates
-   Enhanced portfolio management
-   Improved error handling

## SDKs and Libraries

### Python Client

```python
from quantumtrade import QuantumTradeClient

client = QuantumTradeClient(api_key="your-api-key")
price = client.get_price("BTC-USD")
```

### JavaScript Client

```javascript
import { QuantumTradeClient } from "@quantumtrade/client";

const client = new QuantumTradeClient({ apiKey: "your-api-key" });
const price = await client.getPrice("BTC-USD");
```

## Testing

### API Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test market data endpoint
curl "http://localhost:8000/data/price?symbol=BTC-USD"

# Test with authentication
curl -H "Authorization: Bearer your-token" \
     http://localhost:8000/portfolio/list
```

### Integration Testing

The API includes comprehensive integration tests in the `tests/` directory.

## Documentation

### OpenAPI Specification

The complete OpenAPI specification is available at:

```
GET /openapi.json
```

### Interactive Documentation

Interactive API documentation is available at:

```
GET /docs
```

## Support

For API support, please:

1. Check the documentation
2. Review error messages
3. Contact support@quantumtrade.com
4. Open a GitHub issue

This API documentation provides comprehensive information for integrating with the QuantumTrade platform.
