# Using Anthropic Claude with Local Proxy

This guide explains how to use the Excel Chatbot with Anthropic Claude running through a local proxy or corporate endpoint.

---

## 🎯 What is a Local Proxy?

A local proxy is an intermediate server that:
- Routes API requests through your corporate network
- Manages API keys centrally
- Provides additional security/logging
- May be required by corporate IT policies

Common scenarios:
- Corporate proxy server (e.g., `http://proxy.company.com:8080`)
- Local development proxy (e.g., `http://localhost:8000/v1`)
- Custom Anthropic-compatible endpoint

---

## 🔑 Step 1: Get Your Anthropic API Key

Even with a proxy, you still need an Anthropic API key:

### Option A: Regular Anthropic Account
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to **Settings** → **API Keys**
4. Click **"Create Key"**
5. Copy the key (starts with `sk-ant-...`)

### Option B: Corporate Managed Key
If your company manages API keys:
1. Contact your IT department or API key administrator
2. Request an Anthropic API key for development
3. They'll provide you with the key and proxy endpoint

---

## 🌐 Step 2: Find Your Proxy URL

You need to know your proxy endpoint URL:

### Local Development Proxy
```
http://localhost:8000/v1
http://127.0.0.1:3000/v1
```

### Corporate Proxy
```
http://proxy.company.com:8080/v1
https://api-gateway.company.com/anthropic/v1
```

### Custom Endpoint
```
http://your-server.local:port/v1
```

**Important:** The URL should end with `/v1` (Anthropic API version)

---

## 🚀 Step 3: Configure in FastAPI App

### Using the Web Interface (Recommended)

1. **Start the FastAPI app:**
   ```bash
   bash run_api.sh        # macOS/Linux
   run_api.bat           # Windows
   ```

2. **Open browser:** http://localhost:8000

3. **Configure API settings in sidebar:**

   a. Select **"Anthropic Claude"** as provider

   b. Enter your **API Key** (the `sk-ant-...` key)

   c. Select your **Model** (e.g., Claude Sonnet 4)

   d. ✅ **Check "Use Custom Base URL (for proxy)"**

   e. Enter your **Base URL**:
      - Example: `http://localhost:8000/v1`
      - Or: `http://proxy.company.com:8080/v1`

   f. Click **"🚀 Initialize AI"**

4. **Upload Excel files and start chatting!**

---

## 📝 Example Configurations

### Example 1: Local LiteLLM Proxy

If you're using LiteLLM as a local proxy:

```bash
# Start LiteLLM proxy
litellm --model claude-sonnet-4 --api_key sk-ant-your-key

# In Excel Chatbot UI:
# Base URL: http://localhost:8000/v1
# API Key: sk-ant-your-key
```

### Example 2: Corporate API Gateway

```
Provider: Anthropic Claude
API Key: sk-ant-company-key-12345
Model: Claude Sonnet 4
Base URL: https://api-gateway.yourcompany.com/anthropic/v1
```

### Example 3: OpenAI-Compatible Proxy

If your proxy mimics OpenAI's API format:

```
Provider: OpenAI GPT  (yes, even for Claude!)
API Key: your-proxy-key
Model: claude-sonnet-4
Base URL: http://your-proxy:8080/v1
```

---

## 🔧 Environment Variables Method

Alternatively, set proxy via environment variables:

### macOS/Linux:

```bash
# Set environment variables
export ANTHROPIC_API_KEY="sk-ant-your-key"
export ANTHROPIC_BASE_URL="http://localhost:8000/v1"

# Or set proxy for all HTTP traffic
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"

# Run the app
source venv/bin/activate
bash run_api.sh
```

### Windows (Command Prompt):

```cmd
REM Set environment variables
set ANTHROPIC_API_KEY=sk-ant-your-key
set ANTHROPIC_BASE_URL=http://localhost:8000/v1

REM Or set proxy for all HTTP traffic
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080

REM Run the app
venv\Scripts\activate
run_api.bat
```

### Windows (PowerShell):

```powershell
# Set environment variables
$env:ANTHROPIC_API_KEY = "sk-ant-your-key"
$env:ANTHROPIC_BASE_URL = "http://localhost:8000/v1"

# Or set proxy
$env:HTTP_PROXY = "http://proxy.company.com:8080"
$env:HTTPS_PROXY = "http://proxy.company.com:8080"

# Run the app
venv\Scripts\Activate.ps1
bash run_api.sh
```

---

## 🧪 Testing Your Proxy Connection

### Test 1: Health Check

```bash
# Test proxy is running
curl http://localhost:8000/v1/health

# Should return success response
```

### Test 2: Direct API Call

```bash
curl http://localhost:8000/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk-ant-your-key" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Test 3: Through Excel Chatbot

1. Open http://localhost:8000
2. Configure with your proxy URL
3. Click "Initialize AI"
4. Look for success message

---

## 🛠️ Troubleshooting

### Problem: "Connection refused"

**Possible causes:**
- Proxy server not running
- Wrong port number
- Firewall blocking connection

**Solutions:**
1. Verify proxy is running: `curl http://localhost:PORT`
2. Check port number is correct
3. Try `127.0.0.1` instead of `localhost`
4. Check firewall settings

### Problem: "Invalid API key"

**Possible causes:**
- Wrong API key format
- Key not authorized for proxy
- Proxy expects different authentication

**Solutions:**
1. Verify key starts with `sk-ant-`
2. Check with IT if key is registered for proxy
3. Try without proxy to verify key works

### Problem: "404 Not Found"

**Possible causes:**
- Missing `/v1` in base URL
- Wrong endpoint path

**Solutions:**
1. Ensure URL ends with `/v1`
2. Check proxy documentation for correct path
3. Try these formats:
   - `http://proxy:port/v1`
   - `http://proxy:port/anthropic/v1`
   - `http://proxy:port/api/v1`

### Problem: "SSL/TLS errors"

**Possible causes:**
- Using `https://` with self-signed certificate
- Certificate validation issues

**Solutions:**
1. Use `http://` instead of `https://` for local testing
2. Contact IT to install proper certificates
3. For corporate proxies, use provided HTTPS endpoint

### Problem: "Timeout errors"

**Possible causes:**
- Proxy is slow
- Network latency
- Proxy queue is full

**Solutions:**
1. Increase timeout in browser
2. Check proxy logs for issues
3. Contact IT if corporate proxy

---

## 📊 Common Proxy Setups

### Setup 1: LiteLLM Proxy (Popular Choice)

**Install:**
```bash
pip install litellm[proxy]
```

**Run:**
```bash
litellm --model claude-sonnet-4-20250514 \
        --api_key sk-ant-your-key \
        --port 8000
```

**Configure in Excel Chatbot:**
- Base URL: `http://localhost:8000/v1`
- API Key: `sk-ant-your-key`

### Setup 2: OpenAI-Compatible Proxy

Many proxies mimic OpenAI's API format:

**Configure in Excel Chatbot:**
- Provider: OpenAI GPT
- Base URL: `http://your-proxy:port/v1`
- API Key: Your proxy key
- Model: claude-sonnet-4

### Setup 3: Direct Anthropic with Corporate Proxy

**Configure system proxy:**
```bash
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1
```

**Configure in Excel Chatbot:**
- Provider: Anthropic Claude
- Base URL: (leave empty, uses default Anthropic)
- API Key: Your Anthropic key

---

## 🔒 Security Considerations

### For Development:
- ✅ Use `http://` on localhost (faster)
- ✅ Keep API keys in environment variables
- ✅ Don't commit keys to git

### For Production:
- ✅ Use `https://` for proxy endpoints
- ✅ Implement authentication on proxy
- ✅ Use secrets management (Vault, AWS Secrets)
- ✅ Monitor API usage and costs
- ✅ Rotate keys regularly

---

## 📖 Related Documentation

- **FastAPI Deployment:** [FASTAPI_DEPLOYMENT.md](FASTAPI_DEPLOYMENT.md)
- **Setup Guide:** [SETUP_FROM_SCRATCH.md](SETUP_FROM_SCRATCH.md)
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 💡 Quick Reference

### Starting with Proxy

1. Get API key from https://console.anthropic.com/
2. Find your proxy URL (ask IT or use local proxy)
3. Run: `bash run_api.sh`
4. Open: http://localhost:8000
5. Check "Use Custom Base URL"
6. Enter proxy URL and API key
7. Click "Initialize AI"

### Common Proxy URLs

```
Local Development:
  http://localhost:8000/v1
  http://127.0.0.1:3000/v1

Corporate:
  http://proxy.company.com:8080/v1
  https://api-gateway.company.com/anthropic/v1

Custom:
  http://your-server.local:port/v1
```

---

**Need help?** Check the troubleshooting section or contact your IT department for corporate proxy details.
