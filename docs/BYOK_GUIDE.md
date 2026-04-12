# Multi-Provider BYOK (Bring Your Own Key) Guide

## 🎯 Overview

The Excel Chatbot now supports **multiple AI providers**! Users can bring their own API keys and choose from:

- **🔷 Anthropic Claude** - Claude Sonnet 4, Claude Opus 4
- **🟢 Google Gemini** - Gemini 2.0 Flash, Gemini 1.5 Pro
- **🟦 OpenAI GPT** - GPT-4o, GPT-4 Turbo

Perfect for deployment where users have different AI provider preferences!

---

## 🚀 Quick Start

### Run the BYOK Interface

```bash
./scripts/start_byok.sh
```

Or directly:
```bash
streamlit run ui/chatbot_byok_ui.py
```

---

## 🔑 Getting API Keys

### Anthropic Claude
1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key
5. Copy and save it securely

**Models Available:**
- `claude-sonnet-4-20250514` (recommended)
- `claude-opus-4-20250514`
- `claude-3-5-sonnet-20241022`
- `claude-3-5-haiku-20241022`

### Google Gemini
1. Go to: https://aistudio.google.com/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

**Models Available:**
- `gemini-2.0-flash-exp` (recommended - fast & free)
- `gemini-1.5-pro`
- `gemini-1.5-flash`

### OpenAI GPT
1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy and save it

**Models Available:**
- `gpt-4o` (recommended)
- `gpt-4o-mini`
- `gpt-4-turbo`
- `gpt-3.5-turbo`

---

## 📖 How to Use

### Step 1: Configure AI Provider

1. Open the sidebar
2. Select your preferred AI provider
3. Enter your API key
4. Choose a model (or use default)
5. Click **"Initialize AI"**

### Step 2: Upload Excel Files

1. Once AI is initialized
2. Use the file uploader
3. Select one or more Excel files
4. Click **"Process Files"**

### Step 3: Query Your Data

1. Use the chat interface
2. Ask questions in natural language
3. Get intelligent answers from your chosen AI!

---

## 🏢 Corporate Proxy Support

For Anthropic and OpenAI, you can use custom base URLs (for corporate proxies):

1. Check **"Use Custom Base URL"**
2. Enter your proxy endpoint
3. Example: `https://your-proxy.com/v1`

This is useful for:
- Corporate/enterprise deployments
- Azure OpenAI endpoints
- Custom API gateways

---

## 💰 Cost Comparison

### Free Tier / Credits

| Provider | Free Tier | Notes |
|----------|-----------|-------|
| **Gemini** | ✅ Generous free tier | Best for testing |
| **Anthropic** | ⚠️ Limited credits | New accounts get $5 |
| **OpenAI** | ⚠️ Limited credits | New accounts get $5 |

### Pricing (Approximate)

| Provider | Input ($/1M tokens) | Output ($/1M tokens) |
|----------|---------------------|----------------------|
| **Gemini 2.0 Flash** | Free / $0.075 | Free / $0.30 |
| **Claude Sonnet 4** | $3.00 | $15.00 |
| **GPT-4o** | $2.50 | $10.00 |

**Recommendation:** Start with Gemini for testing (free tier), then choose based on your needs.

---

## 🎨 Features

### All Providers Support:

✅ Natural language queries
✅ Multi-file Excel analysis
✅ Semantic search
✅ Context-aware responses
✅ Chat history
✅ Large file handling (100k+ rows)

### Provider-Specific Advantages:

**Anthropic Claude:**
- Excellent at analysis and reasoning
- Long context windows
- Great for complex queries

**Google Gemini:**
- Very fast response times
- Generous free tier
- Cost-effective for production

**OpenAI GPT:**
- Industry standard
- Reliable and consistent
- Well-documented

---

## 🔧 Installation

### Install Additional Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

This installs:
- `anthropic` - Anthropic Claude SDK
- `google-generativeai` - Google Gemini SDK
- `openai` - OpenAI GPT SDK

---

## 🌐 Deployment Options

### Option 1: Personal Use (Current)
- Users provide their own API keys
- No API costs for you
- Users choose their preferred provider

### Option 2: Shared API Key
- Set environment variables:
  ```bash
  export ANTHROPIC_API_KEY=your_key
  export GEMINI_API_KEY=your_key
  export OPENAI_API_KEY=your_key
  ```
- Users select provider (no key needed)
- You pay for API usage

### Option 3: Hybrid
- Allow both options
- Users can use their key OR use shared key
- Implement usage limits if using shared key

---

## 🔒 Security Best Practices

### For Users:
1. **Never share your API keys**
2. Store keys securely
3. Rotate keys periodically
4. Monitor API usage in provider dashboard
5. Set spending limits in provider dashboard

### For Deployment:
1. API keys are never stored on server
2. Keys only exist in session state
3. Use HTTPS in production
4. Implement rate limiting
5. Add user authentication if needed

---

## 📊 Architecture

```
User Interface (Streamlit)
        ↓
    API Key Input
        ↓
src/llm_provider.py (MultiProviderLLM)
        ↓
    ┌────────┬────────┬────────┐
    ↓        ↓        ↓        ↓
Anthropic  Gemini  OpenAI  (Future providers)
    ↓        ↓        ↓
  Response unified and returned
```

The `MultiProviderLLM` class abstracts away provider differences, giving a unified interface.

---

## 🆚 Comparison: BYOK vs Proxy-Based

| Feature | BYOK | Proxy-Based |
|---------|------|-------------|
| **API Costs** | Users pay | You pay |
| **Provider Choice** | User decides | You decide |
| **Setup** | User needs key | No user setup |
| **Scalability** | Free to scale | Costs increase |
| **Control** | Less control | Full control |
| **Best For** | Public apps | Internal tools |

---

## 🧪 Testing

Test each provider:

```bash
# Test Anthropic
python -c "from src.llm_provider import create_llm_client; client = create_llm_client('anthropic', 'your-key'); print(client.generate([{'role': 'user', 'content': 'Hi'}]))"

# Test Gemini
python -c "from src.llm_provider import create_llm_client; client = create_llm_client('gemini', 'your-key'); print(client.generate([{'role': 'user', 'content': 'Hi'}]))"

# Test OpenAI
python -c "from src.llm_provider import create_llm_client; client = create_llm_client('openai', 'your-key'); print(client.generate([{'role': 'user', 'content': 'Hi'}]))"
```

---

## 🐛 Troubleshooting

### "API key not found" error
- Make sure you entered the key correctly
- Check for extra spaces
- Verify key is active in provider dashboard

### "Invalid model" error
- Use one of the listed models
- Check provider documentation for latest models

### "Rate limit exceeded"
- Wait a few seconds and try again
- Check your usage limits in provider dashboard
- Consider upgrading your plan

### Corporate proxy issues
- Enter the full base URL with `/v1` endpoint
- Check with IT for correct proxy URL
- Some proxies may require additional headers (not supported yet)

---

## 🚀 Next Steps

1. **Try it out:** Start with Gemini (free tier)
2. **Compare providers:** Test with same queries
3. **Choose best fit:** Based on cost, speed, quality
4. **Deploy:** Use BYOK for public deployment

---

## 📞 Support

- **API Issues:** Contact the respective provider
- **App Issues:** Check logs, review error messages
- **Feature Requests:** Open an issue on GitHub

---

**Ready to use?** Run:
```bash
bash scripts/start_byok.sh
```

Choose your provider and start chatting with your Excel data! 🎉
