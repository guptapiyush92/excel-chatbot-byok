#!/bin/bash

# Excel Chatbot - Streamlit Version Launcher
# Runs the Streamlit BYOK application

echo "================================================"
echo "  Starting Excel Chatbot (Streamlit)"
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

# Check if Streamlit is installed
if ! python -c "import streamlit" &> /dev/null; then
    echo "📦 Installing required dependencies..."
    pip install -r requirements.txt
fi

echo "🚀 Starting Streamlit server..."
echo "   URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run Streamlit
streamlit run ui/chatbot_byok_ui.py
