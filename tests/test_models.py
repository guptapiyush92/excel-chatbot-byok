#!/usr/bin/env python3
"""
Test which Claude models are available through your API endpoint.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# Common Claude model names to try
models_to_try = [
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "claude-2.1",
    "claude-2.0",
    "claude-instant-1.2",
    # Simplified names
    "claude-3-opus",
    "claude-3-sonnet",
    "claude-3-haiku",
    "claude-sonnet",
    "claude-opus",
]

print("="*70)
print("Testing Available Claude Models")
print("="*70)
print()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

for model in models_to_try:
    try:
        print(f"Testing: {model}...", end=" ")
        response = client.messages.create(
            model=model,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"✅ WORKS")
        print(f"   Response: {response.content[0].text}")
        break  # Found a working model
    except Exception as e:
        error_msg = str(e)
        if "Invalid model" in error_msg or "INVALID_MODEL" in error_msg:
            print(f"❌ Not supported")
        else:
            print(f"⚠️  Error: {error_msg[:50]}...")

print()
print("="*70)
print("Check the SAP documentation for supported models:")
print("https://url.sap/vxs9sw")
print("="*70)
