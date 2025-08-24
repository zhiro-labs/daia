.PHONY: help install test lint format clean coverage

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	uv sync --dev

test: ## Run tests
	uv run pytest -v

test-cov: ## Run tests with coverage
	uv run coverage run -m pytest
	uv run coverage report --show-missing

lint: ## Run linting
	uv run ruff check .

format: ## Format code
	uv run ruff format .

format-check: ## Check code formatting
	uv run ruff format --check .

clean: ## Clean up cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -f .coverage
	rm -f coverage.xml

ci: lint format-check test ## Run all CI checks locally

all: install lint format test ## Install, lint, format, and test