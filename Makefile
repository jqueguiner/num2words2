# Makefile for num2words2 development and testing

.PHONY: help test test-all test-pyenv test-tox test-docker clean lint format install dev-install

# Default Python version for development
PYTHON ?= python3

help:  ## Show this help message
	@echo "🚀 num2words2 Development Commands"
	@echo "================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in development mode
	$(PYTHON) -m pip install -e .

dev-install:  ## Install package with development dependencies
	$(PYTHON) -m pip install -e .
	$(PYTHON) -m pip install -r requirements-test.txt

test:  ## Run tests with current Python version
	$(PYTHON) -m pytest tests/ -v

test-coverage:  ## Run tests with coverage report
	$(PYTHON) -m coverage run -m pytest tests/
	$(PYTHON) -m coverage report --fail-under=75 --omit=.tox/*,tests/*,/usr/*

test-all:  ## Run tests on all Python versions (default: pyenv)
	@echo "🧪 Testing with all Python versions using pyenv..."
	./test_local.sh pyenv

test-pyenv:  ## Test with multiple Python versions using pyenv
	@echo "🧪 Testing with pyenv..."
	./test_local.sh pyenv

test-tox:  ## Test with tox (all configured environments)
	@echo "🧪 Testing with tox..."
	tox

test-docker:  ## Test with multiple Python versions using Docker
	@echo "🧪 Testing with Docker..."
	./test_local.sh docker

test-quick:  ## Quick test using current Python and a few versions via tox
	@echo "🚀 Running quick tests..."
	$(PYTHON) -m pytest tests/ -x --tb=short
	@echo "✅ Quick tests completed"

lint:  ## Run linting checks
	@echo "🔍 Running linting checks..."
	flake8 num2words2 tests
	isort --check-only --float-to-top --diff num2words2 tests

format:  ## Format code with isort and black (if available)
	@echo "🎨 Formatting code..."
	isort num2words2 tests
	@if command -v black >/dev/null 2>&1; then \
		echo "Running black formatter..."; \
		black num2words2 tests; \
	else \
		echo "Black not found, skipping..."; \
	fi

clean:  ## Clean build artifacts and cache files
	@echo "🧹 Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .tox/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✅ Cleanup completed"

build:  ## Build package for distribution
	@echo "📦 Building package..."
	$(PYTHON) setup.py sdist bdist_wheel
	@echo "✅ Build completed"

check-build:  ## Check package build for PyPI
	@echo "🔍 Checking package build..."
	$(PYTHON) -m twine check dist/*
	@echo "✅ Build check completed"

install-tools:  ## Install development tools
	@echo "🛠️  Installing development tools..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install tox flake8 isort coverage pytest twine
	@if ! command -v pyenv >/dev/null 2>&1; then \
		echo "⚠️  Consider installing pyenv for multi-version testing:"; \
		echo "   curl https://pyenv.run | bash"; \
	fi
	@echo "✅ Development tools installed"

ci-test:  ## Run the same tests as in CI
	@echo "🔄 Running CI-equivalent tests..."
	tox -e py38,py39,py310,py311,py312,py313
	@echo "✅ CI tests completed"

migration-test:  ## Test the migration script
	@echo "🔄 Testing migration script..."
	$(PYTHON) migrate_to_num2words2.py --dry-run tests/
	@echo "✅ Migration script test completed"

# Development workflow targets
dev-setup: install-tools dev-install  ## Set up development environment
	@echo "✅ Development environment setup completed"

pre-commit: lint test  ## Run pre-commit checks
	@echo "✅ Pre-commit checks completed"

release-check: clean build check-build test-all  ## Full release readiness check
	@echo "🚀 Release readiness check completed"

# Quick access targets
quick: test-quick  ## Alias for test-quick
all: test-all     ## Alias for test-all
tox: test-tox     ## Alias for test-tox

# Show available Python versions
show-python-versions:  ## Show available Python versions
	@echo "🐍 Available Python versions:"
	@if command -v pyenv >/dev/null 2>&1; then \
		echo "pyenv versions:"; \
		pyenv versions --bare | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$$' | sort -V; \
	else \
		echo "pyenv not found"; \
	fi
	@echo ""
	@echo "Current Python: $(shell $(PYTHON) --version)"

.DEFAULT_GOAL := help