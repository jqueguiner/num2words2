# Local Testing Guide for num2words2

This guide explains how to test num2words2 locally across multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12, 3.13).

## Quick Start

### Option 1: Using Make (Recommended)
```bash
# Setup development environment
make dev-setup

# Run tests on all Python versions (using pyenv)
make test-all

# Run tests with tox
make test-tox

# Run tests with Docker
make test-docker

# See all available commands
make help
```

### Option 2: Using Test Scripts Directly
```bash
# Using pyenv (recommended for development)
./test_local.sh pyenv

# Using tox (simpler, good for CI-like testing)
./test_local.sh tox

# Using Docker (isolated environments)
./test_local.sh docker

# Using the Python script (most features)
python test_all_python_versions.py --method pyenv
python test_all_python_versions.py --method docker
```

### Option 3: Manual Testing with tox
```bash
# Install tox
pip install tox

# Run all environments
tox

# Run specific Python version
tox -e py39

# Run with verbose output
tox -v
```

## Prerequisites

### For pyenv method:
1. **Install pyenv:**
   ```bash
   # macOS
   brew install pyenv
   
   # Linux/WSL
   curl https://pyenv.run | bash
   ```

2. **Install Python versions:**
   ```bash
   pyenv install 3.8.19
   pyenv install 3.9.19  
   pyenv install 3.10.14
   pyenv install 3.11.9
   pyenv install 3.12.4
   pyenv install 3.13.0
   ```

3. **Add to shell configuration (.bashrc, .zshrc):**
   ```bash
   export PATH="$HOME/.pyenv/bin:$PATH"
   eval "$(pyenv init -)"
   ```

### For Docker method:
1. **Install Docker:**
   - Visit: https://docs.docker.com/get-docker/
   - Follow installation instructions for your OS

### For tox method:
1. **Install tox:**
   ```bash
   pip install tox
   ```

## Testing Methods Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **pyenv** | Fast, local, reuses environments | Requires setup, platform dependent | Development |
| **tox** | Simple, standardized, widely used | Limited Python version management | CI-like testing |
| **Docker** | Isolated, reproducible, works anywhere | Slower, requires Docker | Production-like testing |

## Available Commands

### Make Commands
- `make test` - Run tests with current Python version
- `make test-all` - Test all versions with pyenv
- `make test-tox` - Test with tox
- `make test-docker` - Test with Docker
- `make test-quick` - Quick tests (current Python + basic checks)
- `make lint` - Run linting checks
- `make clean` - Clean build artifacts
- `make dev-setup` - Setup development environment

### Script Options

#### test_local.sh
```bash
./test_local.sh pyenv      # Test with pyenv (default)
./test_local.sh tox        # Test with tox 
./test_local.sh docker     # Test with Docker
```

#### test_all_python_versions.py
```bash
python test_all_python_versions.py --help
python test_all_python_versions.py --method pyenv --versions 3.9,3.10,3.11
python test_all_python_versions.py --method docker --versions 3.12,3.13
```

## Troubleshooting

### pyenv issues:
```bash
# Check pyenv installation
pyenv --version

# Check available versions  
pyenv versions

# Install missing version
pyenv install 3.11.9

# Set global Python version
pyenv global 3.11.9
```

### tox issues:
```bash
# Recreate environments
tox -r

# Run with verbose output
tox -v

# Test specific environment
tox -e py39 -- -v
```

### Docker issues:
```bash
# Check Docker installation
docker --version

# Clean up Docker images
docker system prune -f

# Check available Python images
docker search python
```

### Common Test Failures:
1. **Import errors**: Check if package is installed correctly
2. **Missing dependencies**: Install requirements-test.txt
3. **Version conflicts**: Use fresh virtual environments
4. **Permission issues**: Check file permissions on scripts

## CI Integration

The local testing setup matches the CI configuration:

```bash
# Run same tests as CI
make ci-test

# Or with tox
tox -e py38,py39,py310,py311,py312,py313
```

## Performance Tips

1. **Use pyenv for fastest testing** (reuses environments)
2. **Use tox for standardized testing** (creates fresh environments)  
3. **Use Docker for maximum isolation** (slower but most reliable)
4. **Run `make test-quick` for rapid feedback** during development
5. **Use `make test-all` before commits** to catch version issues

## Example Workflow

```bash
# 1. Setup development environment (once)
make dev-setup

# 2. During development - quick checks
make test-quick

# 3. Before committing - full test
make pre-commit

# 4. Before release - comprehensive test
make release-check
```

## Getting Help

```bash
# Show available make commands
make help

# Show help for scripts
./test_local.sh
python test_all_python_versions.py --help

# Check installed tools
make show-python-versions
```

For issues or questions, please check:
- [GitHub Issues](https://github.com/jqueguiner/num2words/issues)
- [GitHub Discussions](https://github.com/jqueguiner/num2words/discussions)