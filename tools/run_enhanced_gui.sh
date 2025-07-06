#!/bin/bash

# Enhanced Homework 1 GUI Launcher
# This script launches the enhanced GUI with integrated figure display

echo "🎯 Launching Enhanced Homework 1 GUI..."
echo "========================================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "   Run: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if enhanced GUI file exists
if [ ! -f "src/homework1/enhanced_gui.py" ]; then
    echo "❌ Enhanced GUI file not found: src/homework1/enhanced_gui.py"
    exit 1
fi

# Set matplotlib backend to avoid Qt threading issues
export MPLBACKEND=Agg

# Launch the enhanced GUI
echo "🚀 Starting Enhanced GUI with Integrated Figure Display..."
echo "   - All figures will be displayed in tabs within the same window"
echo "   - No separate figure windows will open"
echo "   - Qt warnings are expected and harmless"
echo ""

python src/homework1/enhanced_gui.py

echo ""
echo "✅ Enhanced GUI application closed successfully!" 