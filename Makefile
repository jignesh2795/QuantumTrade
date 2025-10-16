.PHONY: install test run clean lint format

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

run:
	python main.py

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

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies"
	@echo "  make test     - Run tests"
	@echo "  make run      - Run the trading bot"
	@echo "  make clean    - Clean cache files"
	@echo "  make lint     - Lint code with ruff"
	@echo "  make format   - Format code with black"
	@echo "  make setup    - Initial setup"