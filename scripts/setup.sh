#!/bin/bash

# Setup script for Excel Chatbot

echo "================================"
echo "Excel Chatbot Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✅ Python is installed"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ Dependencies installed successfully"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your ANTHROPIC_API_KEY"
    echo ""
fi

# Check for Excel files
echo "Checking for Excel files..."
if [ -f "actuarial_life_data_file1.xlsx" ] && [ -f "actuarial_life_data_file2.xlsx" ]; then
    echo "✅ Excel files found"
else
    echo "⚠️  Warning: Excel files not found. Please ensure the following files exist:"
    echo "   - actuarial_life_data_file1.xlsx"
    echo "   - actuarial_life_data_file2.xlsx"
fi

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your ANTHROPIC_API_KEY"
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "3. Run the chatbot:"
echo "   python chatbot_cli.py     # For CLI interface"
echo "   streamlit run chatbot_ui.py  # For web interface"
echo ""
