#!/usr/bin/env python3
"""
Quick test of the chatbot with a sample query.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.chatbot import ChatbotManager

print("="*70)
print("Initializing Excel Chatbot...")
print("="*70)
print()

# Initialize chatbot
chatbot = ChatbotManager.initialize_from_excel_files(
    file_paths=[
        "actuarial_life_data_file1.xlsx",
        "actuarial_life_data_file2.xlsx"
    ],
    reset_index=False  # Use existing index if available
)

print("\n" + "="*70)
print("Chatbot Ready! Testing with sample query...")
print("="*70)
print()

# Test query
query = "What data is available in these Excel files?"
print(f"Query: {query}\n")

result = chatbot.query(query, n_results=3)

print(f"Answer:\n{result['answer']}")
print()
print("="*70)
print("✅ Test successful! Your chatbot is working.")
print("="*70)
