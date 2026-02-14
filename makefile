.PHONY: help install lint format type-check test test-cov clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make lint       - Run linter (ruff)"
	@echo "  make format     - Format code (black)"
	@echo "  make type-check - Run type checker (mypy)"
	@echo "  make test       - Run tests"
	@echo "  make test-cov   - Run tests with coverage"
	@echo "  make check      - Run all checks (lint + type-check + test)"
	@echo "  make clean      - Clean up temporary files"

# Install dependencies
install:
	poetry install --with dev

# Linting
lint:
	poetry run ruff check .

# Format code
format:
	poetry run black .

# Type checking
type-check:
	poetry run mypy .

# Run tests
test:
	poetry run pytest tests/

# Run tests with coverage
test-cov:
	poetry run pytest --cov=core tests/

# Run all checks
check: lint type-check test

# Auto-fix linting and formatting issues
fix:
	poetry run ruff check --fix
	poetry run black .

# Run all checks with auto-fix first
check-fix: fix type-check test

# Development workflow with auto-fix
dev-fix: install check-fix

# Clean up
clean:
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Development workflow
dev: install check