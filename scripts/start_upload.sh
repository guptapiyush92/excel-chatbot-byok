#!/bin/bash
# Launch the Hybrid Excel Chatbot with File Upload

echo "🚀 Starting Excel Chatbot with File Upload..."
echo ""
echo "Features:"
echo "  📤 Upload your own Excel files"
echo "  ✅ Automatic processing and vectorization"
echo "  🎯 Structured + Semantic queries"
echo "  📊 Handles KBs to MBs of data"
echo ""
echo "Opening at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop"
echo ""

source venv/bin/activate
streamlit run ui/chatbot_upload_ui.py
