#!/bin/bash

# Excel Chatbot - FastAPI Version Launcher
# Runs the corporate-friendly FastAPI application

echo "================================================"
echo "  Starting Excel Chatbot (FastAPI)"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: bash scripts/quick_setup.sh"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Check if FastAPI is installed
if ! python -c "import fastapi" &> /dev/null; then
    echo "📦 Installing required dependencies..."
    pip install -r requirements.txt
fi

# Set environment variables
export API_HOST=${API_HOST:-0.0.0.0}
export API_PORT=${API_PORT:-8000}

echo "🚀 Starting FastAPI server..."
echo "   URL: http://localhost:${API_PORT}"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run with uvicorn
python -m uvicorn api.main:app --host $API_HOST --port $API_PORT --reload
