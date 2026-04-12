#!/bin/bash
# Start the BYOK (Bring Your Own Key) Multi-Provider chatbot

echo "🤖 Starting Multi-Provider BYOK Excel Chatbot..."
echo ""
echo "Supported providers:"
echo "  🔷 Anthropic Claude"
echo "  🟢 Google Gemini"
echo "  🟦 OpenAI GPT"
echo ""

source venv/bin/activate
streamlit run ui/chatbot_byok_ui.py
