#!/bin/bash

# Proxy Testing Script
# This script helps diagnose proxy connection issues

echo "=========================================="
echo "  Anthropic Proxy Connection Tester"
echo "=========================================="
echo ""

# Get user input
read -p "Enter your proxy base URL (e.g., http://localhost:8000): " PROXY_URL
read -p "Enter your Anthropic API key: " API_KEY

echo ""
echo "Testing connection to: $PROXY_URL"
echo ""

# Test 1: Check if proxy is reachable
echo "Test 1: Checking if proxy is reachable..."
if curl -s --connect-timeout 5 "$PROXY_URL" > /dev/null 2>&1; then
    echo "✅ Proxy is reachable"
else
    echo "❌ Cannot reach proxy. Is it running?"
    exit 1
fi

echo ""

# Test 2: Try /v1/messages endpoint
echo "Test 2: Testing Anthropic API endpoint..."
RESPONSE=$(curl -s -w "\n%{http_code}" "$PROXY_URL/v1/messages" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Say hello"}]
  }')

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

echo "HTTP Status Code: $HTTP_CODE"
echo ""

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ SUCCESS! Proxy is working correctly"
    echo "Response preview:"
    echo "$BODY" | head -n 10
    echo ""
    echo "✅ Your configuration is correct!"
    echo "   Base URL to use in Excel Chatbot: $PROXY_URL/v1"
elif [ "$HTTP_CODE" = "404" ]; then
    echo "❌ 404 Not Found - Wrong endpoint path"
    echo ""
    echo "Common fixes:"
    echo "  1. Try: $PROXY_URL/anthropic/v1/messages"
    echo "  2. Try: $PROXY_URL/api/v1/messages"
    echo "  3. Check your proxy documentation for correct path"
    echo ""
    echo "Response:"
    echo "$BODY"
elif [ "$HTTP_CODE" = "401" ]; then
    echo "❌ 401 Unauthorized - API key issue"
    echo "  - Check your API key is correct"
    echo "  - Verify key is registered with proxy"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "❌ Connection failed - proxy not responding"
    echo "  - Is the proxy running?"
    echo "  - Check the URL and port"
else
    echo "⚠️  Unexpected response code: $HTTP_CODE"
    echo "Response:"
    echo "$BODY"
fi

echo ""
echo "=========================================="
