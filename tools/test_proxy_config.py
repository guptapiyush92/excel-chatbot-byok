"""
Proxy Configuration Helper
Run this to test and diagnose your proxy setup
"""

import sys
import requests
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_proxy_connection():
    """Interactive proxy configuration tester."""

    print("=" * 60)
    print("  Anthropic Proxy Configuration Helper")
    print("=" * 60)
    print()

    # Get configuration
    print("Please provide your proxy details:")
    print()

    proxy_url = input("Proxy Base URL (e.g., http://localhost:8000): ").strip()
    if not proxy_url:
        print("❌ Proxy URL is required!")
        return

    api_key = input("Anthropic API Key (sk-ant-...): ").strip()
    if not api_key:
        print("❌ API key is required!")
        return

    print()
    print("=" * 60)
    print("Testing Configuration...")
    print("=" * 60)
    print()

    # Test 1: Basic connectivity
    print("Test 1: Checking if proxy is reachable...")
    try:
        response = requests.get(proxy_url, timeout=5)
        print(f"✅ Proxy is reachable (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {proxy_url}")
        print("   - Is the proxy running?")
        print("   - Check the URL and port number")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    print()

    # Test 2: Try common Anthropic endpoints
    print("Test 2: Testing Anthropic API endpoints...")
    print()

    endpoints_to_try = [
        f"{proxy_url}/v1/messages",
        f"{proxy_url}/messages",
        f"{proxy_url}/anthropic/v1/messages",
        f"{proxy_url}/api/v1/messages",
    ]

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "Hello"}]
    }

    working_endpoint = None

    for endpoint in endpoints_to_try:
        print(f"Trying: {endpoint}")
        try:
            response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")

            if response.status_code == 200:
                print(f"  ✅ SUCCESS!")
                working_endpoint = endpoint
                break
            elif response.status_code == 404:
                print(f"  ❌ 404 Not Found - Wrong path")
            elif response.status_code == 401:
                print(f"  ❌ 401 Unauthorized - Check API key")
            elif response.status_code == 403:
                print(f"  ❌ 403 Forbidden - Access denied")
            else:
                print(f"  ⚠️  Unexpected status")
                print(f"  Response: {response.text[:200]}")

        except Exception as e:
            print(f"  ❌ Error: {e}")
        print()

    print("=" * 60)
    print("Results")
    print("=" * 60)
    print()

    if working_endpoint:
        # Extract base URL
        if "/v1/messages" in working_endpoint:
            correct_base_url = working_endpoint.replace("/messages", "")
        elif "/messages" in working_endpoint:
            correct_base_url = working_endpoint.replace("/messages", "")
        else:
            correct_base_url = proxy_url

        print("✅ SUCCESS! Your proxy is working!")
        print()
        print("Configuration for Excel Chatbot:")
        print("-" * 60)
        print(f"  Provider: Anthropic Claude")
        print(f"  API Key: {api_key[:20]}...")
        print(f"  Model: claude-sonnet-4-20250514")
        print(f"  ✅ Use Custom Base URL: YES")
        print(f"  Base URL: {correct_base_url}")
        print("-" * 60)
        print()
        print("Steps to use:")
        print("  1. Run: bash run_api.sh")
        print("  2. Open: http://localhost:8000")
        print("  3. Check 'Use Custom Base URL (for proxy)'")
        print(f"  4. Enter: {correct_base_url}")
        print("  5. Enter your API key")
        print("  6. Click 'Initialize AI'")

    else:
        print("❌ Could not find working endpoint")
        print()
        print("Troubleshooting steps:")
        print()
        print("1. Verify your proxy is running:")
        print(f"   curl {proxy_url}")
        print()
        print("2. Check proxy documentation for correct endpoint path")
        print()
        print("3. Common proxy setups:")
        print()
        print("   LiteLLM Proxy:")
        print("     Start: litellm --model claude-sonnet-4 --api_key YOUR_KEY")
        print("     Base URL: http://localhost:8000")
        print()
        print("   Direct Anthropic (no proxy):")
        print("     Leave 'Use Custom Base URL' unchecked")
        print("     API will go directly to Anthropic")
        print()
        print("4. Test without proxy first:")
        print("   - Uncheck 'Use Custom Base URL'")
        print("   - Enter just your API key")
        print("   - This will connect directly to Anthropic")

    print()

if __name__ == "__main__":
    try:
        test_proxy_connection()
    except KeyboardInterrupt:
        print("\n\nAborted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
