#!/bin/bash

# Bitcoin Puzzle Solver - Test Runner Script
# Supports multiple platforms and testing methods

set -e

echo "============================================================"
echo "🧪 Bitcoin Puzzle Solver - Test Runner"
echo "============================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check Python installation
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
print_status "Python $PYTHON_VERSION found"

# Check and install dependencies
print_info "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_status "Dependencies installed"
else
    print_warning "requirements.txt not found"
fi

echo ""
echo "============================================================"
echo "🧪 Running Test Suite"
echo "============================================================"
echo ""

# Run main test suite
python3 test_bitcoin_puzzle.py

echo ""
echo "============================================================"
echo "🐳 Docker Testing (if available)"
echo "============================================================"
echo ""

# Check if Docker is available
if command -v docker &> /dev/null; then
    print_info "Docker detected. Building container..."
    docker build -t bitcoin-puzzle-solver .
    print_status "Docker image built successfully"
    
    print_info "Running tests in Docker container..."
    docker run --rm bitcoin-puzzle-solver
    print_status "Docker tests passed"
else
    print_warning "Docker not installed. Skipping Docker tests."
    print_info "To install Docker: https://docs.docker.com/get-docker/"
fi

echo ""
echo "============================================================"
echo "📊 Test Summary"
echo "============================================================"
echo ""

print_status "All tests completed successfully!"
echo ""
echo "Next steps:"
echo "  1. Run locally:      python3 test_bitcoin_puzzle.py"
echo "  2. Run in Docker:    docker build -t bitcoin . && docker run bitcoin"
echo "  3. Run on Colab:     https://colab.research.google.com"
echo "  4. GitHub Actions:   Commits trigger auto-testing"
echo ""
