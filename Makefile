# AWS Athena MCP Server - Makefile
# Automates common development tasks

.PHONY: help install install-dev test test-unit test-integration lint format type-check clean build run docs

# Default target
help:
	@echo "AWS Athena MCP Server - Available Commands:"
	@echo ""
	@echo "Installation:"
	@echo "  install      - Install package in production mode"
	@echo "  install-dev  - Install development dependencies"
	@echo ""
	@echo "Tests:"
	@echo "  test         - Run all tests"
	@echo "  test-unit    - Run only unit tests"
	@echo "  test-integration - Run integration tests"
	@echo "  test-cov     - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black and isort"
	@echo "  type-check   - Check types with mypy"
	@echo "  check-all    - Run all checks"
	@echo ""
	@echo "Utilities:"
	@echo "  clean        - Remove temporary files and cache"
	@echo "  build        - Build package for distribution"
	@echo "  run          - Run MCP server"
	@echo "  docs         - Generate documentation"

# Installation
install:
	pip install .

install-dev:
	pip install -e .[dev]

# Tests
test:
	python3 -m pytest tests/ -v

test-unit:
	python3 -m pytest tests/unit/ -v

test-integration:
	python3 -m pytest tests/integration/ -v

test-cov:
	python3 -m pytest tests/ --cov=src/athena_mcp --cov-report=html --cov-report=term-missing

# Code quality
lint:
	flake8 src/ tests/
	python3 -m pylint src/athena_mcp/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/

check-all: lint type-check test

# Utilities
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

build: clean
	python3 -m build

run:
	python3 main.py

# Documentation
docs:
	@echo "Documentation available at:"
	@echo "  README.md - Main documentation"
	@echo "  docs/ENVIRONMENT_SETUP.md - Environment configuration"
	@echo "  TROUBLESHOOTING.md - Problem resolution"

# Dependency check
check-deps:
	pip check

# Dependency update (be careful in production)
update-deps:
	pip list --outdated

# Initial development setup
setup-dev: install-dev
	@echo "Development environment configured!"
	@echo "Run 'make help' to see available commands"

# Security check
security-check:
	bandit -r src/
	safety check

# Complete cleanup (including virtual env - be careful!)
clean-all: clean
	@echo "Removing pip cache..."
	pip cache purge