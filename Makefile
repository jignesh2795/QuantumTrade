.PHONY: install test run clean lint format setup test-connection test-risk test-agents help

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=backend

test-connection:
	python scripts/test_binance_connection.py

test-risk:
	python scripts/check_risk_limits.py

test-agents:
	python scripts/test_agents.py

run:
	python main.py

run-paper:
	TRADING_MODE=paper python main.py

run-testnet:
	TRADING_MODE=live USE_TESTNET=true python main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

lint:
	ruff check backend/

format:
	black backend/ tests/

setup:
	chmod +x scripts/setup.sh
	./scripts/setup.sh

verify:
	@echo "Running verification tests..."
	@make test-connection
	@make test-risk
	@make test-agents
	@echo "✅ All verifications passed!"

help:
	@echo "Available commands:"
	@echo "  make install         - Install dependencies"
	@echo "  make test           - Run all tests"
	@echo "  make test-connection - Test Binance connection"
	@echo "  make test-risk      - Test risk management"
	@echo "  make test-agents    - Test AI agents"
	@echo "  make run            - Run the trading bot"
	@echo "  make run-paper      - Run in paper mode"
	@echo "  make run-testnet    - Run with testnet"
	@echo "  make clean          - Clean cache files"
	@echo "  make lint           - Lint code with ruff"
	@echo "  make format         - Format code with black"
	@echo "  make setup          - Initial setup"
	@echo "  make verify         - Run all verification tests"