# Deployment Options

Your Excel Chatbot now supports **two deployment modes**!

## 🔷 Option 1: Proxy-Based (Current Setup)

**Best for:** Internal company tools, controlled environments

### How it works:
- You configure API key in `.env` file
- Users don't need their own keys
- You pay for all API usage
- Full control over which AI provider is used

### To run:
```bash
./run.sh
# or
streamlit run ui/chatbot_upload_ui.py
```

### Configuration:
```bash
# .env file
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_BASE_URL=https://your-proxy.com/v1  # optional
```

---

## 🌟 Option 2: BYOK Multi-Provider (New!)

**Best for:** Public apps, SaaS, user-facing applications

### How it works:
- Users provide their own API keys
- Users choose: Anthropic Claude, Google Gemini, or OpenAI GPT
- Each user pays for their own usage
- Zero API costs for you!

### To run:
```bash
bash scripts/start_byok.sh
# or
streamlit run ui/chatbot_byok_ui.py
```

### Supported Providers:
- **🔷 Anthropic Claude** - Claude Sonnet 4, Opus 4
- **🟢 Google Gemini** - Gemini 2.0 Flash (FREE tier!), 1.5 Pro
- **🟦 OpenAI GPT** - GPT-4o, GPT-4 Turbo

---

## 📊 Comparison

| Feature | Proxy-Based | BYOK Multi-Provider |
|---------|-------------|---------------------|
| **User Setup** | None | Enter API key |
| **API Costs** | You pay | User pays |
| **Provider Choice** | Fixed | User chooses |
| **Best For** | Internal | Public/SaaS |
| **Scalability** | Limited by your budget | Unlimited |
| **Control** | Full | Less |

---

## 💰 Cost Implications

### Proxy-Based Costs (You pay):
- 100 users × 1000 queries/month × $0.015/query = **$1,500/month**

### BYOK Costs (Users pay):
- You: **$0/month** 🎉
- Users: Pay only for what they use

---

## 🎯 Recommendations

### Use Proxy-Based When:
- Internal company tool
- Small user base (<50 users)
- Need full control
- Budget for API costs available
- Corporate proxy requirements

### Use BYOK When:
- Public-facing application
- Large/unknown number of users
- Want to offer multi-provider choice
- Zero API cost requirement
- SaaS or commercial product

### Use Both When:
- Offer "free tier" with shared key (rate limited)
- Offer "premium" with user's own key (unlimited)
- Internal users use proxy, external use BYOK

---

## 🚀 Quick Start

### Current (Proxy-Based):
```bash
# Already configured
./run.sh
```

### New (BYOK):
```bash
# First time: install providers
pip install anthropic google-generativeai openai

# Run
bash scripts/start_byok.sh
```

---

## 📖 Documentation

- **Proxy-Based:** See `HOW_TO_RUN.md`
- **BYOK:** See `docs/BYOK_GUIDE.md`

---

## 🔄 Switching Between Modes

You can run both simultaneously on different ports!

```bash
# Terminal 1: Proxy-based on port 8501
./run.sh

# Terminal 2: BYOK on port 8502
streamlit run ui/chatbot_byok_ui.py --server.port 8502
```

---

## 🌐 Production Deployment

### Proxy-Based Production:
```bash
streamlit run ui/chatbot_upload_ui.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true
```

### BYOK Production:
```bash
streamlit run ui/chatbot_byok_ui.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true
```

Add authentication, rate limiting, and monitoring as needed!

---

**Choose the deployment mode that fits your needs!** 🎉
