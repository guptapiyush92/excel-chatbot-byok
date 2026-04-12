#!/bin/bash
# Quick script to launch the Streamlit chatbot

echo "🚀 Starting Excel Chatbot Web Interface..."
echo ""
echo "The web interface will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

source venv/bin/activate
streamlit run ui/chatbot_ui.py
