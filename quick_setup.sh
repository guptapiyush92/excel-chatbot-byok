#!/bin/bash

# Quick Setup Script for Excel Chatbot
# This script automates the setup process

echo "================================================"
echo "  Excel Chatbot - Automated Setup"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed."
    echo "Please install Python 3.10+ from https://www.python.org/downloads/"
    echo "Then run this script again."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q

# Install requirements
echo "📥 Installing dependencies (this may take 5-10 minutes)..."
echo ""
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ All dependencies installed successfully!"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Edit it to add your API keys if using proxy mode."
    echo ""
fi

echo "================================================"
echo "  🎉 Setup Complete!"
echo "================================================"
echo ""
echo "To run the application:"
echo ""
echo "  BYOK Mode (users provide their own keys):"
echo "    source venv/bin/activate"
echo "    streamlit run ui/chatbot_byok_ui.py"
echo ""
echo "  Proxy Mode (you provide the key):"
echo "    source venv/bin/activate"
echo "    streamlit run ui/chatbot_upload_ui.py"
echo ""
echo "Then open http://localhost:8501 in your browser"
echo ""
echo "================================================"
