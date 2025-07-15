#!/bin/bash

# Automatic Report System - Quick Start Script
echo "🚀 Starting Automatic Report System Setup..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Make main.py executable
chmod +x main.py

echo "✅ Setup complete!"
echo ""
echo "🎯 Quick Commands:"
echo "  Generate sample reports:    ./quick_start.sh sample"
echo "  Start interactive mode:     ./quick_start.sh interactive"
echo "  Start scheduler:            ./quick_start.sh scheduler"
echo "  Check system status:        ./quick_start.sh status"
echo ""

# Handle command line arguments
if [ "$1" = "sample" ]; then
    echo "📊 Generating sample reports..."
    python main.py --sample
elif [ "$1" = "interactive" ]; then
    echo "💻 Starting interactive mode..."
    python main.py --interactive
elif [ "$1" = "scheduler" ]; then
    echo "⏰ Starting scheduler mode..."
    python main.py --scheduler
elif [ "$1" = "status" ]; then
    echo "📋 Checking system status..."
    python main.py --status
elif [ "$1" = "" ]; then
    echo "💻 Starting interactive mode (default)..."
    python main.py --interactive
else
    echo "❌ Unknown option: $1"
    echo "Available options: sample, interactive, scheduler, status"
fi