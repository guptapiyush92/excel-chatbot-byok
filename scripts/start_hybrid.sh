#!/bin/bash
# Launch the Hybrid Excel Chatbot

echo "🚀 Starting Hybrid Excel Chatbot..."
echo ""
echo "Features:"
echo "  ✅ Structured queries for precise data"
echo "  ✅ Semantic search for insights"
echo "  ✅ Automatic query routing"
echo ""
echo "Opening at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop"
echo ""

source venv/bin/activate
streamlit run ui/chatbot_hybrid_ui.py
