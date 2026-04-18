#!/bin/bash

# Run FastAPI Application

echo "================================================"
echo "  Starting Excel Chatbot FastAPI Server"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: bash quick_setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if FastAPI is installed
if ! python -c "import fastapi" &> /dev/null; then
    echo "📦 Installing FastAPI requirements..."
    pip install -r requirements-api.txt
fi

# Set environment variables
export API_HOST=${API_HOST:-0.0.0.0}
export API_PORT=${API_PORT:-8000}

echo "🚀 Starting server..."
echo "   URL: http://localhost:${API_PORT}"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run with uvicorn
cd api
python -m uvicorn main:app --host $API_HOST --port $API_PORT --reload
