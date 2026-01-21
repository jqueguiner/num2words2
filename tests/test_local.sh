#!/bin/bash
#
# Simple shell script to test num2words2 locally with multiple Python versions
#
# This script provides a simple way to test the package using pyenv or tox.
#
# Usage:
#     ./test_local.sh [pyenv|tox|docker]
#
# Requirements:
#     - For pyenv: pyenv with desired Python versions installed
#     - For tox: tox package installed (pip install tox)
#     - For docker: Docker installed
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Python versions to test
PYTHON_VERSIONS=("3.8" "3.9" "3.10" "3.11" "3.12" "3.13")

echo -e "${BLUE}🚀 num2words2 Local Testing Script${NC}"
echo "=================================="

# Function to test with pyenv
test_with_pyenv() {
    echo -e "${BLUE}📦 Testing with pyenv${NC}"

    # Check if pyenv is available
    if ! command -v pyenv &> /dev/null; then
        echo -e "${RED}❌ pyenv not found. Please install pyenv first.${NC}"
        echo "Install: curl https://pyenv.run | bash"
        exit 1
    fi

    echo -e "${GREEN}✅ pyenv found: $(pyenv --version)${NC}"

    # Get available versions
    available_versions=$(pyenv versions --bare | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | cut -d. -f1,2 | sort -u)

    success_count=0
    fail_count=0

    for version in "${PYTHON_VERSIONS[@]}"; do
        echo ""
        echo -e "${YELLOW}🧪 Testing Python ${version}${NC}"
        echo "------------------------"

        # Check if version is available
        if echo "$available_versions" | grep -q "^${version}$"; then
            # Find the latest patch version
            latest_patch=$(pyenv versions --bare | grep -E "^${version}\.[0-9]+$" | sort -V | tail -1)

            if [ -n "$latest_patch" ]; then
                echo -e "Using Python ${latest_patch}"

                # Create temp directory and test
                temp_dir=$(mktemp -d)
                cp -r . "$temp_dir/num2words2"
                cd "$temp_dir/num2words2"

                # Set local Python version
                pyenv local "$latest_patch"

                # Create virtual environment
                echo "📦 Creating virtual environment..."
                python -m venv venv
                source venv/bin/activate

                # Install package and test dependencies
                echo "📦 Installing package..."
                pip install --upgrade pip > /dev/null 2>&1
                pip install -e . > /dev/null 2>&1

                if [ -f requirements-test.txt ]; then
                    pip install -r requirements-test.txt > /dev/null 2>&1
                fi

                # Run tests
                echo "🧪 Running tests..."
                if python -m pytest tests/ -q; then
                    echo -e "${GREEN}✅ Python ${version}: PASSED${NC}"
                    ((success_count++))
                else
                    echo -e "${RED}❌ Python ${version}: FAILED${NC}"
                    ((fail_count++))
                fi

                # Cleanup
                deactivate
                cd - > /dev/null
                rm -rf "$temp_dir"
            else
                echo -e "${YELLOW}⚠️  No patch version found for Python ${version}${NC}"
                ((fail_count++))
            fi
        else
            echo -e "${YELLOW}⚠️  Python ${version} not installed. Install with:${NC}"
            echo "   pyenv install ${version}.x"
            ((fail_count++))
        fi
    done

    echo ""
    echo "=================================="
    echo -e "${BLUE}📊 PYENV TESTING SUMMARY${NC}"
    echo -e "${GREEN}✅ Passed: ${success_count}${NC}"
    echo -e "${RED}❌ Failed: ${fail_count}${NC}"

    if [ $fail_count -eq 0 ]; then
        echo -e "${GREEN}🎉 All tests passed!${NC}"
        return 0
    else
        return 1
    fi
}

# Function to test with tox
test_with_tox() {
    echo -e "${BLUE}📦 Testing with tox${NC}"

    # Check if tox is available
    if ! command -v tox &> /dev/null; then
        echo -e "${YELLOW}⚠️  tox not found. Installing...${NC}"
        pip install tox
    fi

    echo -e "${GREEN}✅ tox found: $(tox --version)${NC}"

    echo "🧪 Running tox tests..."
    if tox; then
        echo -e "${GREEN}🎉 All tox tests passed!${NC}"
        return 0
    else
        echo -e "${RED}❌ Some tox tests failed${NC}"
        return 1
    fi
}

# Function to test with docker
test_with_docker() {
    echo -e "${BLUE}📦 Testing with Docker${NC}"

    # Check if docker is available
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ Docker found: $(docker --version)${NC}"

    success_count=0
    fail_count=0

    for version in "${PYTHON_VERSIONS[@]}"; do
        echo ""
        echo -e "${YELLOW}🧪 Testing Python ${version} with Docker${NC}"
        echo "--------------------------------"

        # Create Dockerfile
        cat > Dockerfile.test << EOF
FROM python:${version}-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Install package and dependencies
RUN pip install --upgrade pip
RUN pip install -e .

# Install test dependencies if they exist
RUN if [ -f requirements-test.txt ]; then pip install -r requirements-test.txt; fi

# Run tests
CMD ["python", "-m", "pytest", "tests/", "-v"]
EOF

        # Build and run
        image_name="num2words2-test-py$(echo $version | tr -d '.')"

        echo "🔨 Building Docker image..."
        if docker build -f Dockerfile.test -t "$image_name" . > /dev/null 2>&1; then
            echo "🧪 Running tests..."
            if docker run --rm "$image_name" > /dev/null 2>&1; then
                echo -e "${GREEN}✅ Python ${version}: PASSED${NC}"
                ((success_count++))
            else
                echo -e "${RED}❌ Python ${version}: FAILED${NC}"
                ((fail_count++))
            fi

            # Cleanup image
            docker rmi "$image_name" > /dev/null 2>&1
        else
            echo -e "${RED}❌ Failed to build image for Python ${version}${NC}"
            ((fail_count++))
        fi

        # Cleanup Dockerfile
        rm -f Dockerfile.test
    done

    echo ""
    echo "=================================="
    echo -e "${BLUE}📊 DOCKER TESTING SUMMARY${NC}"
    echo -e "${GREEN}✅ Passed: ${success_count}${NC}"
    echo -e "${RED}❌ Failed: ${fail_count}${NC}"

    if [ $fail_count -eq 0 ]; then
        echo -e "${GREEN}🎉 All tests passed!${NC}"
        return 0
    else
        return 1
    fi
}

# Main logic
case "${1:-pyenv}" in
    "pyenv")
        test_with_pyenv
        ;;
    "tox")
        test_with_tox
        ;;
    "docker")
        test_with_docker
        ;;
    *)
        echo "Usage: $0 [pyenv|tox|docker]"
        echo ""
        echo "Methods:"
        echo "  pyenv  - Use pyenv to test with different Python versions"
        echo "  tox    - Use tox for testing (simpler, requires tox.ini)"
        echo "  docker - Use Docker containers for isolated testing"
        echo ""
        echo "Examples:"
        echo "  $0 pyenv   # Test with pyenv (default)"
        echo "  $0 tox     # Test with tox"
        echo "  $0 docker  # Test with Docker"
        exit 1
        ;;
esac
