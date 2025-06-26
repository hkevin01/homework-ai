#!/bin/bash

# Homework 1 GUI Launcher Script
# This script activates the virtual environment and launches the PyQt GUI

echo "🚀 Starting Homework 1 GUI Application..."
echo "========================================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please run: python3 -m venv .venv"
    echo "Then run: source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if activation was successful
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to activate virtual environment!"
    exit 1
fi

echo "✅ Virtual environment activated successfully!"

# Check if GUI file exists
if [ ! -f "src/homework1/gui_app.py" ]; then
    echo "❌ Error: GUI application not found!"
    echo "Expected file: src/homework1/gui_app.py"
    exit 1
fi

echo "🎯 Launching Homework 1 GUI..."
echo "========================================"

# Run the GUI application
python src/homework1/gui_app.py

# Check if GUI ran successfully
if [ $? -ne 0 ]; then
    echo "❌ Error: GUI application failed to start!"
    echo "Make sure all dependencies are installed:"
    echo "pip install -r requirements.txt"
    exit 1
fi

echo "✅ GUI application closed successfully!" 