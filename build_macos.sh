#!/bin/bash
# Build script for creating WalletExporter.app on macOS
# Usage: ./build_macos.sh

set -e  # Exit on any error

echo "==================================="
echo "WalletExporter macOS Build Script"
echo "==================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11"

echo "Checking Python version..."
echo "Found: Python $PYTHON_VERSION"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
    echo "❌ ERROR: Python 3.11+ required (found: $PYTHON_VERSION)"
    exit 1
fi

echo "✓ Python version OK"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Clean previous builds
if [ -d "dist" ]; then
    echo "Cleaning previous build artifacts..."
    rm -rf dist build *.spec
    echo "✓ Clean complete"
    echo ""
fi

# Run PyInstaller
echo "Building WalletExporter.app..."
echo "(This may take a minute or two...)"
echo ""

pyinstaller WalletExporter.spec

echo ""
echo "==================================="
echo "✓ Build Successful!"
echo "==================================="
echo ""
echo "Location: dist/WalletExporter.app"
echo ""
echo "To run the application:"
echo "  open dist/WalletExporter.app"
echo ""
echo "Or navigate to Finder and double-click: dist/WalletExporter.app"
echo ""
echo "Note: On first run, you may see a security warning."
echo "Right-click → Open to allow running the app."
echo ""
