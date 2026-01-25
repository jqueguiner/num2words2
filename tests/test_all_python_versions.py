#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

"""
Local testing script for num2words2 across multiple Python versions

This script helps test the package locally on Python 3.8, 3.9, 3.10, 3.11,
3.12, and 3.13
using pyenv or Docker to manage different Python versions.

Usage:
    python test_all_python_versions.py [--method pyenv|docker] [--versions
    3.8,3.9,3.10,3.11,3.12,3.13]

Requirements:
    - For pyenv method: pyenv installed with target Python versions
    - For docker method: Docker installed
"""


def run_command(cmd, cwd=None, capture_output=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            timeout=300,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


def check_pyenv():
    """Check if pyenv is installed and working."""
    returncode, stdout, stderr = run_command("pyenv --version")
    if returncode == 0:
        print(f"✅ pyenv found: {stdout.strip()}")
        return True
    else:
        print("❌ pyenv not found. Install pyenv first:")
        print("   curl https://pyenv.run | bash")
        return False


def check_docker():
    """Check if Docker is installed and working."""
    returncode, stdout, stderr = run_command("docker --version")
    if returncode == 0:
        print(f"✅ Docker found: {stdout.strip()}")
        return True
    else:
        print("❌ Docker not found. Install Docker first:")
        print("   https://docs.docker.com/get-docker/")
        return False


def get_available_python_versions_pyenv():
    """Get available Python versions from pyenv."""
    returncode, stdout, stderr = run_command("pyenv versions --bare")
    if returncode != 0:
        return []

    versions = []
    for line in stdout.strip().split("\n"):
        line = line.strip()
        if line and not line.startswith("system") and "/" not in line:
            versions.append(line)
    return versions


def install_python_version_pyenv(version):
    """Install a Python version using pyenv."""
    print(f"📦 Installing Python {version} with pyenv...")
    returncode, stdout, stderr = run_command(f"pyenv install -s {version}")
    if returncode == 0:
        print(f"✅ Python {version} installed successfully")
        return True
    else:
        print(f"❌ Failed to install Python {version}: {stderr}")
        return False


def run_python_version_test_pyenv(version, project_dir):
    """Test the package with a specific Python version using pyenv."""
    print(f"\n🧪 Testing with Python {version} (pyenv)")
    print("=" * 50)

    # Create a temporary directory for this test
    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy project files to temp directory
        temp_project = Path(temp_dir) / "num2words2"
        shutil.copytree(
            project_dir,
            temp_project,
            ignore=shutil.ignore_patterns(
                ".git", "__pycache__", "*.pyc", ".tox", "venv", "env"
            ),
        )

        # Set Python version for this directory
        cmd = f"pyenv local {version}"
        returncode, stdout, stderr = run_command(cmd, cwd=temp_project)
        if returncode != 0:
            print(f"❌ Failed to set Python version {version}: {stderr}")
            return False

        # Verify Python version
        returncode, stdout, stderr = run_command("python --version", cwd=temp_project)
        if returncode != 0:
            print(f"❌ Failed to get Python version: {stderr}")
            return False

        actual_version = stdout.strip()
        print(f"🐍 Using Python: {actual_version}")

        # Create virtual environment
        print("📦 Creating virtual environment...")
        returncode, stdout, stderr = run_command(
            "python -m venv venv", cwd=temp_project
        )
        if returncode != 0:
            print(f"❌ Failed to create virtual environment: {stderr}")
            return False

        # Activate virtual environment and install dependencies
        venv_python = temp_project / "venv" / "bin" / "python"
        venv_pip = temp_project / "venv" / "bin" / "pip"

        if not venv_python.exists():
            # Windows
            venv_python = temp_project / "venv" / "Scripts" / "python.exe"
            venv_pip = temp_project / "venv" / "Scripts" / "pip.exe"

        print("📦 Installing package in development mode...")
        cmd = f'"{venv_pip}" install -e .'
        returncode, stdout, stderr = run_command(cmd, cwd=temp_project)
        if returncode != 0:
            print(f"❌ Failed to install package: {stderr}")
            return False

        # Install test dependencies if they exist
        test_requirements = temp_project / "requirements-test.txt"
        if test_requirements.exists():
            print("📦 Installing test dependencies...")
            cmd = f'"{venv_pip}" install -r requirements-test.txt'
            returncode, stdout, stderr = run_command(cmd, cwd=temp_project)
            if returncode != 0:
                msg = "⚠️  Warning: Failed to install test requirements:"
                msg += f" {stderr}"
                print(msg)

        # Run tests
        print("🧪 Running tests...")
        cmd = f'"{venv_python}" -m pytest tests/ -v'
        returncode, stdout, stderr = run_command(cmd, cwd=temp_project)

        if returncode == 0:
            print(f"✅ All tests passed for Python {version}")
            return True
        else:
            print(f"❌ Tests failed for Python {version}")
            print(f"Error output: {stderr}")
            return False


def run_python_version_test_docker(version, project_dir):
    """Test the package with a specific Python version using Docker."""
    print(f"\n🧪 Testing with Python {version} (Docker)")
    print("=" * 50)

    # Create Dockerfile content
    dockerfile_content = f"""
FROM python:{version}-slim

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
RUN if [ -f requirements-test.txt ]; then \\
    pip install -r requirements-test.txt; fi

# Run tests
CMD ["python", "-m", "pytest", "tests/", "-v"]
"""

    # Create temporary Dockerfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".dockerfile", delete=False) as f:
        f.write(dockerfile_content)
        dockerfile_path = f.name

    try:
        # Build Docker image
        image_name = f"num2words2-test-py{version.replace('.', '')}"
        print(f"🔨 Building Docker image for Python {version}...")

        returncode, stdout, stderr = run_command(
            f"docker build -f {dockerfile_path} -t {image_name} {project_dir}",
            capture_output=False,
        )

        if returncode != 0:
            print(f"❌ Failed to build Docker image for Python {version}")
            return False

        # Run tests in container
        print("🧪 Running tests in Docker container...")
        returncode, stdout, stderr = run_command(
            f"docker run --rm {image_name}", capture_output=False
        )

        # Cleanup image
        run_command(f"docker rmi {image_name}")

        if returncode == 0:
            print(f"✅ All tests passed for Python {version}")
            return True
        else:
            print(f"❌ Tests failed for Python {version}")
            return False

    finally:
        # Cleanup Dockerfile
        os.unlink(dockerfile_path)


def main():
    desc = "Test num2words2 across multiple Python versions"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--method",
        choices=["pyenv", "docker"],
        default="pyenv",
        help="Method to use for testing (default: pyenv)",
    )
    parser.add_argument(
        "--versions",
        default="3.8,3.9,3.10,3.11,3.12,3.13",
        help="Comma-separated list of Python versions to test",
    )
    parser.add_argument(
        "--project-dir",
        default=".",
        help="Project directory (default: current directory)",
    )

    args = parser.parse_args()

    project_dir = os.path.abspath(args.project_dir)
    versions = [v.strip() for v in args.versions.split(",")]

    print("🚀 num2words2 Multi-Python Version Testing")
    print("=" * 50)
    print(f"Method: {args.method}")
    print(f"Versions: {', '.join(versions)}")
    print(f"Project: {project_dir}")
    print()

    # Check prerequisites
    if args.method == "pyenv":
        if not check_pyenv():
            sys.exit(1)
        available_versions = get_available_python_versions_pyenv()
    elif args.method == "docker":
        if not check_docker():
            sys.exit(1)
        available_versions = None

    # Test each Python version
    results = {}

    for version in versions:
        if args.method == "pyenv":
            # Check if version is available, install if needed
            if available_versions and version not in available_versions:
                if not install_python_version_pyenv(version):
                    results[version] = False
                    continue

            success = run_python_version_test_pyenv(version, project_dir)
        elif args.method == "docker":
            success = run_python_version_test_docker(version, project_dir)

        results[version] = success

    # Print summary
    print("\n" + "=" * 50)
    print("📊 TESTING SUMMARY")
    print("=" * 50)

    passed = 0
    failed = 0

    for version, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"Python {version}: {status}")
        if success:
            passed += 1
        else:
            failed += 1

    total = len(results)
    msg = f"\n📈 Results: {passed} passed, {failed} failed"
    msg += f" out of {total} versions"
    print(msg)

    if failed > 0:
        print("\n💡 To debug failures, run individual tests:")
        for version, success in results.items():
            if not success:
                if args.method == "pyenv":
                    cmd = f"   pyenv local {version} && "
                    cmd += "python -m pytest tests/ -v"
                    print(cmd)
                elif args.method == "docker":
                    print(f"   # Check Docker logs for Python {version}")
        sys.exit(1)
    else:
        print("\n🎉 All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
