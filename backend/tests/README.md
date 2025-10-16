# QuantumTrade Testing

This directory contains tests for the QuantumTrade application.

## Test Structure

```
tests/
├── unit/                 # Unit tests
│   ├── test_engine.py              # Basic engine tests
│   └── test_engine_comprehensive.py # Comprehensive engine tests
├── integration/          # Integration tests
├── e2e/                  # End-to-end tests
├── fixtures/             # Test fixtures and data
└── conftest.py           # pytest configuration
```

## Running Tests

### Run All Tests

```bash
# Activate conda environment
conda activate quantumtrade

# Run all tests
python -m pytest
```

### Run Specific Test Files

```bash
# Run basic engine test
python -m pytest backend/tests/unit/test_engine.py -v

# Run comprehensive engine tests
python -m pytest backend/tests/unit/test_engine_comprehensive.py -v

# Run tests with coverage
python -m pytest --cov=backend.core --cov-report=html
```

### Run Tests with Coverage

```bash
# Run tests with coverage report
python -m pytest --cov=backend --cov-report=term-missing

# Generate HTML coverage report
python -m pytest --cov=backend --cov-report=html

# Run tests and generate both terminal and HTML coverage reports
python -m pytest --cov=backend --cov-report=term --cov-report=html
```

## Test Types

### Unit Tests

Unit tests focus on individual components and functions:
- Test engine initialization
- Test trading cycle execution
- Test order execution
- Test shutdown procedures

### Integration Tests

Integration tests verify that multiple components work together:
- Engine with exchange integration
- Strategy with engine integration
- Database operations

### End-to-End Tests

E2E tests simulate real user scenarios:
- Complete trading cycles
- Multiple buy/sell operations
- Performance testing

## Writing Tests

### Test Structure

Tests follow the Arrange-Act-Assert pattern:

```python
def test_example():
    # Arrange - Set up test data and mocks
    mock_data = create_mock_data()
    
    # Act - Execute the function under test
    result = function_under_test(mock_data)
    
    # Assert - Verify the results
    assert result == expected_value
```

### Async Tests

For async functions, use the `@pytest.mark.asyncio` decorator:

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### Mocking

Use `unittest.mock` for mocking external dependencies:

```python
from unittest.mock import AsyncMock, Mock, patch

@patch('module.ClassName')
def test_with_mock(mock_class):
    mock_instance = Mock()
    mock_class.return_value = mock_instance
    
    # Test code here
```

## Test Fixtures

Common fixtures are defined in `conftest.py`:

- `mock_settings` - Mock application settings
- `mock_exchange` - Mock exchange interface
- `mock_strategy` - Mock trading strategy

## Continuous Integration

Tests are automatically run in the CI pipeline. All tests must pass before merging changes.

## Troubleshooting

### Common Issues

1. **Asyncio errors**: Make sure to use `@pytest.mark.asyncio` decorator
2. **Import errors**: Check that `sys.path` includes the backend directory
3. **Mock issues**: Ensure mocks return the expected data types

### Debugging Tests

```bash
# Run tests in verbose mode
python -m pytest -v

# Run tests with output capture disabled
python -m pytest -s

# Run a specific test function
python -m pytest path/to/test_file.py::test_function_name
```