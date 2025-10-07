# QuantumTrade Testing Guide

This guide provides comprehensive information about testing practices, frameworks, and procedures for the QuantumTrade platform.

## Testing Philosophy

QuantumTrade follows a comprehensive testing approach that includes:

-   **Unit Testing**: Individual function and component testing
-   **Integration Testing**: Testing interactions between components
-   **End-to-End Testing**: Full system workflow testing
-   **Performance Testing**: Load and stress testing
-   **Security Testing**: Vulnerability and penetration testing

## Testing Frameworks

### Backend Testing

-   **pytest**: Primary testing framework for Python
-   **pytest-asyncio**: For asynchronous testing
-   **pytest-cov**: Code coverage reporting
-   **unittest**: For standard library compatibility

### Frontend Testing

-   **Jest**: JavaScript testing framework
-   **React Testing Library**: For React component testing
-   **Cypress**: End-to-end testing
-   **@testing-library/jest-dom**: Custom Jest matchers

## Test Organization

### Backend Test Structure

```
backend/tests/
├── unit/                 # Unit tests
│   ├── agents/           # Agent tests
│   ├── api/              # API endpoint tests
│   ├── core/             # Core module tests
│   ├── database/         # Database tests
│   └── utils/            # Utility function tests
├── integration/          # Integration tests
│   ├── api/              # API integration tests
│   ├── database/         # Database integration tests
│   └── services/         # Service integration tests
├── e2e/                  # End-to-end tests
│   ├── trading/          # Trading workflow tests
│   └── auth/             # Authentication tests
├── fixtures/             # Test data and mocks
│   ├── sample_data.py    # Sample data generators
│   └── mock_services.py  # Mock service implementations
└── conftest.py          # pytest configuration
```

### Frontend Test Structure

```
frontend/src/
├── __tests__/            # Unit and integration tests
│   ├── components/       # Component tests
│   ├── services/         # Service tests
│   ├── hooks/            # Hook tests
│   └── utils/            # Utility tests
├── __mocks__/            # Mock implementations
│   ├── axios.js          # Mock HTTP client
│   └── supabase.js       # Mock Supabase client
└── test-utils/           # Test utilities and helpers
```

## Writing Unit Tests

### Backend Unit Tests

#### Testing Agents

```python
# tests/unit/agents/test_strategy_agent.py
import pytest
from src.agents.strategy_agent import StrategyAgent

class TestStrategyAgent:
    def test_moving_average_signal_buy(self):
        """Test moving average strategy generates buy signal"""
        agent = StrategyAgent("BTC-USD")
        data = {
            "prices": [40000, 41000, 42000, 43000, 44000],
            "short_ma": 43500,
            "long_ma": 42000
        }

        signal = agent.moving_average_signal(data)

        assert signal["action"] == "BUY"
        assert signal["confidence"] > 0.5

    def test_moving_average_signal_sell(self):
        """Test moving average strategy generates sell signal"""
        agent = StrategyAgent("BTC-USD")
        data = {
            "prices": [44000, 43000, 42000, 41000, 40000],
            "short_ma": 40500,
            "long_ma": 42000
        }

        signal = agent.moving_average_signal(data)

        assert signal["action"] == "SELL"
        assert signal["confidence"] > 0.5
```

#### Testing API Endpoints

```python
# tests/unit/api/test_market_routes.py
import pytest
from fastapi.testclient import TestClient
from src.api.server import app

client = TestClient(app)

class TestMarketRoutes:
    def test_get_price_success(self):
        """Test successful price retrieval"""
        response = client.get("/data/price?symbol=BTC-USD")

        assert response.status_code == 200
        assert "price" in response.json()
        assert "symbol" in response.json()

    def test_get_price_missing_symbol(self):
        """Test price retrieval with missing symbol"""
        response = client.get("/data/price")

        assert response.status_code == 422
```

#### Testing Database Operations

```python
# tests/unit/database/test_trade_repository.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Trade
from src.database.repositories import TradeRepository

class TestTradeRepository:
    @pytest.fixture
    def db_session(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()

    def test_create_trade(self, db_session):
        """Test trade creation"""
        repo = TradeRepository(db_session)
        trade_data = {
            "symbol": "BTC-USD",
            "action": "BUY",
            "size": 0.1,
            "price": 45000.0
        }

        trade = repo.create_trade(trade_data)

        assert trade.symbol == "BTC-USD"
        assert trade.action == "BUY"
        assert trade.size == 0.1
        assert trade.price == 45000.0
```

### Frontend Unit Tests

#### Testing Components

```javascript
// src/components/__tests__/TradeCard.test.js
import { render, screen } from "@testing-library/react";
import TradeCard from "../TradeCard";

describe("TradeCard", () => {
    const mockTrade = {
        symbol: "BTC-USD",
        action: "BUY",
        size: 0.1,
        price: 45000,
        timestamp: "2023-01-01T12:00:00Z",
    };

    test("renders trade information correctly", () => {
        render(<TradeCard trade={mockTrade} />);

        expect(screen.getByText("BTC-USD")).toBeInTheDocument();
        expect(screen.getByText("BUY")).toBeInTheDocument();
        expect(screen.getByText("0.1")).toBeInTheDocument();
        expect(screen.getByText("$45,000.00")).toBeInTheDocument();
    });

    test("applies correct styling for buy action", () => {
        render(<TradeCard trade={mockTrade} />);

        const actionElement = screen.getByText("BUY");
        expect(actionElement).toHaveClass("buy-action");
    });
});
```

#### Testing Hooks

```javascript
// src/hooks/__tests__/usePortfolio.test.js
import { renderHook, act } from "@testing-library/react";
import usePortfolio from "../usePortfolio";

describe("usePortfolio", () => {
    test("initializes with empty portfolio", () => {
        const { result } = renderHook(() => usePortfolio());

        expect(result.current.portfolio).toEqual([]);
        expect(result.current.totalValue).toBe(0);
    });

    test("adds position to portfolio", () => {
        const { result } = renderHook(() => usePortfolio());

        act(() => {
            result.current.addPosition({
                symbol: "BTC-USD",
                size: 0.1,
                price: 45000,
            });
        });

        expect(result.current.portfolio).toHaveLength(1);
        expect(result.current.portfolio[0].symbol).toBe("BTC-USD");
    });
});
```

## Writing Integration Tests

### Backend Integration Tests

#### API Integration Tests

```python
# tests/integration/api/test_trading_workflow.py
import pytest
from fastapi.testclient import TestClient
from src.api.server import app
from src.database.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

class TestTradingWorkflow:
    @pytest.fixture(autouse=True)
    def setup_database(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        # Setup test database connection
        yield
        # Cleanup

    def test_full_trading_workflow(self):
        """Test complete trading workflow"""
        # 1. Get market data
        price_response = client.get("/data/price?symbol=BTC-USD")
        assert price_response.status_code == 200

        # 2. Generate trading signal
        signal_response = client.get("/strategy/signal?symbol=BTC-USD")
        assert signal_response.status_code == 200

        # 3. Assess risk
        risk_response = client.get("/risk/assess?position_size=1000&account_balance=10000")
        assert risk_response.status_code == 200

        # 4. Execute trade
        trade_response = client.post("/execute/trade", json={
            "symbol": "BTC-USD",
            "action": "BUY",
            "size": 0.1
        })
        assert trade_response.status_code == 200
```

#### Database Integration Tests

```python
# tests/integration/database/test_portfolio_integration.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Position
from src.database.repositories import PortfolioRepository

class TestPortfolioIntegration:
    @pytest.fixture
    def db_session(self):
        engine = create_engine("postgresql://test:test@localhost:5432/testdb")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.rollback()
        session.close()

    def test_portfolio_lifecycle(self, db_session):
        """Test complete portfolio position lifecycle"""
        repo = PortfolioRepository(db_session)

        # Create position
        position = repo.create_position("user123", "BTC-USD", 0.1, 45000)
        assert position.id is not None

        # Update position
        updated = repo.update_position(position.id, 0.2, 46000)
        assert updated.quantity == 0.2
        assert updated.avg_price == 46000

        # Get positions
        positions = repo.get_user_positions("user123")
        assert len(positions) == 1

        # Delete position
        repo.delete_position(position.id)
        positions = repo.get_user_positions("user123")
        assert len(positions) == 0
```

### Frontend Integration Tests

#### Service Integration Tests

```javascript
// src/services/__tests__/tradingService.test.js
import { getMarketData, executeTrade } from "../tradingService";
import axios from "axios";

jest.mock("axios");

describe("tradingService", () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test("fetches market data successfully", async () => {
        const mockData = {
            symbol: "BTC-USD",
            price: 45000,
            timestamp: "2023-01-01T12:00:00Z",
        };

        axios.get.mockResolvedValue({ data: mockData });

        const result = await getMarketData("BTC-USD");

        expect(axios.get).toHaveBeenCalledWith(
            "/api/data/price?symbol=BTC-USD"
        );
        expect(result).toEqual(mockData);
    });

    test("handles API errors gracefully", async () => {
        axios.get.mockRejectedValue(new Error("Network error"));

        await expect(getMarketData("BTC-USD")).rejects.toThrow("Network error");
    });
});
```

## Writing End-to-End Tests

### Cypress E2E Tests

#### Authentication Flow

```javascript
// cypress/e2e/auth.spec.js
describe("Authentication", () => {
    beforeEach(() => {
        cy.visit("/");
    });

    it("allows user to sign up", () => {
        cy.get('[data-testid="signup-button"]').click();
        cy.get('[data-testid="email-input"]').type("test@example.com");
        cy.get('[data-testid="password-input"]').type("password123");
        cy.get('[data-testid="confirm-password-input"]').type("password123");
        cy.get('[data-testid="submit-button"]').click();

        cy.url().should("include", "/dashboard");
        cy.get('[data-testid="user-menu"]').should("be.visible");
    });

    it("allows user to log in", () => {
        cy.get('[data-testid="login-button"]').click();
        cy.get('[data-testid="email-input"]').type("test@example.com");
        cy.get('[data-testid="password-input"]').type("password123");
        cy.get('[data-testid="submit-button"]').click();

        cy.url().should("include", "/dashboard");
        cy.get('[data-testid="portfolio-value"]').should("be.visible");
    });
});
```

#### Trading Workflow

```javascript
// cypress/e2e/trading.spec.js
describe("Trading Workflow", () => {
    beforeEach(() => {
        // Login before each test
        cy.login("test@example.com", "password123");
        cy.visit("/trading");
    });

    it("allows user to execute a trade", () => {
        cy.get('[data-testid="symbol-selector"]').select("BTC-USD");
        cy.get('[data-testid="buy-button"]').click();
        cy.get('[data-testid="quantity-input"]').type("0.1");
        cy.get('[data-testid="execute-trade-button"]').click();

        cy.get('[data-testid="trade-confirmation"]').should("be.visible");
        cy.get('[data-testid="trade-history"]').should("contain", "BTC-USD");
    });

    it("displays portfolio updates in real-time", () => {
        cy.get('[data-testid="portfolio-value"]').then(($value) => {
            const initialValue = $value.text();

            // Execute a trade
            cy.executeTrade("BTC-USD", "BUY", 0.1);

            // Check for portfolio update
            cy.get('[data-testid="portfolio-value"]').should(
                "not.contain",
                initialValue
            );
        });
    });
});
```

## Test Fixtures and Mocks

### Sample Data Fixtures

```python
# tests/fixtures/sample_data.py
import pytest
from datetime import datetime, timedelta

class SampleData:
    @staticmethod
    def btc_usd_price_data():
        """Generate sample BTC-USD price data"""
        return {
            "symbol": "BTC-USD",
            "prices": [45000, 45500, 44800, 46200, 45900],
            "timestamps": [
                datetime.now() - timedelta(hours=i)
                for i in range(5, 0, -1)
            ]
        }

    @staticmethod
    def sample_trades():
        """Generate sample trade data"""
        return [
            {
                "symbol": "BTC-USD",
                "action": "BUY",
                "size": 0.1,
                "price": 45000,
                "timestamp": datetime.now() - timedelta(hours=2)
            },
            {
                "symbol": "ETH-USD",
                "action": "SELL",
                "size": 1.0,
                "price": 3000,
                "timestamp": datetime.now() - timedelta(hours=1)
            }
        ]

    @staticmethod
    def user_portfolio():
        """Generate sample portfolio data"""
        return [
            {
                "symbol": "BTC-USD",
                "quantity": 0.5,
                "avg_price": 42000,
                "current_price": 45000
            },
            {
                "symbol": "ETH-USD",
                "quantity": 2.0,
                "avg_price": 2800,
                "current_price": 3000
            }
        ]

@pytest.fixture
def sample_price_data():
    return SampleData.btc_usd_price_data()

@pytest.fixture
def sample_trades():
    return SampleData.sample_trades()

@pytest.fixture
def sample_portfolio():
    return SampleData.user_portfolio()
```

### Mock Services

```python
# tests/fixtures/mock_services.py
import pytest
from unittest.mock import Mock, AsyncMock

class MockServices:
    @staticmethod
    def mock_data_agent():
        """Create mock data agent"""
        mock = Mock()
        mock.get_price.return_value = 45000.0
        mock.get_historical_data.return_value = {
            "symbol": "BTC-USD",
            "data": [
                {"timestamp": "2023-01-01", "close": 45000},
                {"timestamp": "2023-01-02", "close": 45500}
            ]
        }
        return mock

    @staticmethod
    def mock_strategy_agent():
        """Create mock strategy agent"""
        mock = Mock()
        mock.generate_signal.return_value = {
            "symbol": "BTC-USD",
            "signal": "BUY",
            "confidence": 0.85
        }
        return mock

@pytest.fixture
def mock_data_agent():
    return MockServices.mock_data_agent()

@pytest.fixture
def mock_strategy_agent():
    return MockServices.mock_strategy_agent()
```

## Running Tests

### Backend Test Commands

```bash
# Run all tests
cd backend
pytest

# Run specific test file
pytest tests/unit/agents/test_strategy_agent.py

# Run tests with coverage
pytest --cov=src --cov-report=html tests/

# Run integration tests only
pytest -m integration tests/

# Run tests in parallel
pytest -n auto tests/

# Run tests with verbose output
pytest -v tests/
```

### Frontend Test Commands

```bash
# Run all tests
cd frontend
npm test

# Run tests in watch mode
npm run test:watch

# Run specific test file
npm test -- src/components/__tests__/TradeCard.test.js

# Run tests with coverage
npm run test:coverage

# Run end-to-end tests
npm run test:e2e
```

### Continuous Integration

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
    test:
        runs-on: ubuntu-latest
        services:
            postgres:
                image: postgres:15
                env:
                    POSTGRES_PASSWORD: postgres
                options: >-
                    --health-cmd pg_isready
                    --health-interval 10s
                    --health-timeout 5s
                    --health-retries 5
        steps:
            - uses: actions/checkout@v2
            - name: Set up Python
              uses: actions/setup-python@v2
              with:
                  python-version: 3.11
            - name: Install dependencies
              run: |
                  cd backend
                  pip install -r requirements.txt
            - name: Run tests
              run: |
                  cd backend
                  pytest --cov=src --cov-report=xml
            - name: Upload coverage
              uses: codecov/codecov-action@v1
```

## Test Coverage and Quality

### Coverage Requirements

-   **Unit Tests**: Minimum 80% coverage
-   **Integration Tests**: Minimum 70% coverage
-   **Critical Paths**: 100% coverage

### Code Quality Checks

```bash
# Run linting
cd backend
flake8 src/

# Run type checking
mypy src/

# Run security checks
bandit -r src/
```

### Performance Testing

```python
# tests/performance/test_api_performance.py
import pytest
import time
from fastapi.testclient import TestClient
from src.api.server import app

client = TestClient(app)

class TestAPIPerformance:
    def test_price_endpoint_response_time(self):
        """Test price endpoint response time under 100ms"""
        start_time = time.time()
        response = client.get("/data/price?symbol=BTC-USD")
        end_time = time.time()

        response_time = (end_time - start_time) * 1000  # Convert to milliseconds

        assert response.status_code == 200
        assert response_time < 100, f"Response time {response_time}ms exceeds 100ms limit"

    def test_concurrent_requests(self):
        """Test API handles concurrent requests"""
        import concurrent.futures

        def make_request():
            return client.get("/data/price?symbol=BTC-USD")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            responses = [future.result() for future in futures]

        # All requests should succeed
        assert all(response.status_code == 200 for response in responses)
```

## Debugging Test Issues

### Common Test Problems

#### Database Test Issues

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base

@pytest.fixture(scope="function")
def db_session():
    """Create a database session for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)
```

#### Mocking External Services

```python
# tests/unit/services/test_external_service.py
import pytest
from unittest.mock import patch, Mock
from src.services.market_data import MarketDataService

class TestMarketDataService:
    @patch('src.services.market_data.requests.get')
    def test_fetch_external_data_success(self, mock_get):
        """Test successful external data fetch"""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {"price": 45000}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = MarketDataService()

        # Act
        result = service.fetch_external_data("BTC-USD")

        # Assert
        assert result["price"] == 45000
        mock_get.assert_called_once_with(
            "https://api.external.com/price/BTC-USD"
        )

    @patch('src.services.market_data.requests.get')
    def test_fetch_external_data_failure(self, mock_get):
        """Test external data fetch failure"""
        # Arrange
        mock_get.side_effect = Exception("Network error")

        service = MarketDataService()

        # Act & Assert
        with pytest.raises(Exception, match="Network error"):
            service.fetch_external_data("BTC-USD")
```

## Best Practices

### Test Design Principles

1. **Independent Tests**: Each test should be independent and not rely on other tests
2. **Fast Tests**: Tests should run quickly to encourage frequent execution
3. **Clear Assertions**: Tests should have clear, specific assertions
4. **Descriptive Names**: Test names should clearly describe what is being tested
5. **Proper Setup/Teardown**: Use fixtures for proper test setup and cleanup

### Anti-Patterns to Avoid

1. **Testing Implementation Details**: Focus on behavior, not implementation
2. **Over-Mocking**: Only mock what's necessary
3. **Flaky Tests**: Tests should produce consistent results
4. **Slow Tests**: Optimize test performance
5. **Incomplete Coverage**: Ensure critical paths are covered

This testing guide provides a comprehensive framework for ensuring the quality and reliability of the QuantumTrade platform through systematic testing practices.
