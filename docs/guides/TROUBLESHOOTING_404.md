# Troubleshooting 404 Proxy Errors

## 🔴 Error: "anthropic.NotFoundError: 404 page not found"

This error means the application is trying to reach an API endpoint that doesn't exist at your proxy URL.

---

## 🔍 Quick Diagnosis

### Run the Diagnostic Tool

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Run diagnostic
python test_proxy_config.py
```

This will test your proxy and tell you exactly what's wrong!

---

## 🎯 Common Causes & Solutions

### Cause 1: Wrong Base URL Format

**Problem:** You entered the full endpoint path instead of just the base URL

❌ **Wrong:**
```
http://localhost:8000/v1/messages  (Too specific!)
```

✅ **Correct:**
```
http://localhost:8000/v1           (Just the base!)
```

**Solution:** Remove `/messages` from the end of your URL

---

### Cause 2: Missing `/v1` in Path

**Problem:** Your proxy expects `/v1` but you didn't include it

❌ **Wrong:**
```
http://localhost:8000
```

✅ **Correct:**
```
http://localhost:8000/v1
```

**Solution:** Add `/v1` to the end

---

### Cause 3: Proxy Not Running

**Problem:** You configured a proxy URL but the proxy isn't actually running

**Test:**
```bash
curl http://localhost:8000
```

If you get "Connection refused", the proxy isn't running.

**Solution:** Start your proxy first:

**For LiteLLM:**
```bash
pip install 'litellm[proxy]'
litellm --model claude-sonnet-4-20250514 \
        --api_key sk-ant-YOUR-KEY \
        --port 8000
```

**For other proxies:** Check their documentation

---

### Cause 4: Wrong Proxy Path

**Problem:** Your proxy uses a different path structure

Some proxies use different paths:
- Standard: `/v1/messages`
- Alternative 1: `/anthropic/v1/messages`
- Alternative 2: `/api/v1/messages`
- Alternative 3: `/messages`

**Solution:** Try these base URLs in order:

1. `http://localhost:8000/v1`
2. `http://localhost:8000`
3. `http://localhost:8000/anthropic/v1`
4. `http://localhost:8000/api/v1`

---

### Cause 5: You Don't Actually Need a Proxy

**Problem:** You're trying to use a proxy but you should connect directly to Anthropic

**Solution:** If you're not using a corporate proxy or local gateway:

1. **Uncheck** "Use Custom Base URL (for proxy)"
2. Just enter your Anthropic API key
3. The app will connect directly to Anthropic

This is the **simplest option** if you don't need a proxy!

---

## 🔧 Step-by-Step Fix

### Option A: Direct Connection (No Proxy) - RECOMMENDED

If you don't need a proxy:

1. Open http://localhost:8000
2. Select **Anthropic Claude**
3. Enter your API key from https://console.anthropic.com/
4. Select model: **Claude Sonnet 4**
5. **DON'T check** "Use Custom Base URL"
6. Click **"Initialize AI"**
7. Done! ✅

### Option B: Fix Proxy Configuration

If you do need a proxy:

1. **Verify proxy is running:**
   ```bash
   curl http://localhost:YOUR_PORT
   ```

2. **Test with diagnostic tool:**
   ```bash
   python test_proxy_config.py
   ```

3. **Use the URL it suggests:**
   - The tool will test multiple endpoint formats
   - Use the one that returns ✅ SUCCESS

4. **Configure in app:**
   - ✅ Check "Use Custom Base URL"
   - Enter the working URL (e.g., `http://localhost:8000/v1`)
   - Enter your API key
   - Click "Initialize AI"

---

## 📊 Decision Tree

```
Do you have a corporate proxy requirement?
│
├─ NO → Use direct connection (uncheck "Use Custom Base URL")
│
└─ YES → Do you know your proxy URL?
         │
         ├─ NO → Contact your IT department
         │        Ask for: "Anthropic API proxy endpoint"
         │
         └─ YES → Is your proxy running?
                  │
                  ├─ NO → Start proxy first
                  │        (e.g., litellm --model ... --api_key ...)
                  │
                  └─ YES → Run: python test_proxy_config.py
                           Use the URL it suggests
```

---

## 🧪 Manual Testing

If the diagnostic tool doesn't work, test manually:

### Test 1: Can you reach the proxy?
```bash
curl http://localhost:YOUR_PORT
```

Expected: Some response (even error is OK)
If fails: Proxy not running

### Test 2: Test the full endpoint
```bash
curl -X POST http://localhost:YOUR_PORT/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk-ant-YOUR-KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**If you get 200 OK:** Your proxy works!
  - Base URL to use: `http://localhost:YOUR_PORT/v1`

**If you get 404:** Wrong path
  - Try without `/v1`: `http://localhost:YOUR_PORT`
  - Or try: `http://localhost:YOUR_PORT/anthropic/v1`

**If you get 401:** API key issue
  - Check your API key is correct
  - Verify it's registered with the proxy

---

## 🚀 Working Example: LiteLLM

Here's a complete working example:

### Terminal 1: Start LiteLLM Proxy
```bash
# Install LiteLLM
pip install 'litellm[proxy]'

# Start proxy on port 4000 (to avoid conflict with FastAPI on 8000)
litellm --model claude-sonnet-4-20250514 \
        --api_key sk-ant-YOUR-REAL-KEY \
        --port 4000

# You should see: "Uvicorn running on http://0.0.0.0:4000"
```

### Terminal 2: Start Excel Chatbot
```bash
cd excel_chatbot
source venv/bin/activate
bash run_api.sh

# Will start on port 8000
```

### Browser: Configure
1. Open: http://localhost:8000
2. Provider: Anthropic Claude
3. API Key: `sk-ant-YOUR-REAL-KEY`
4. Model: Claude Sonnet 4
5. ✅ Use Custom Base URL: **CHECKED**
6. Base URL: `http://localhost:4000`  (Note: No `/v1` for LiteLLM!)
7. Click "Initialize AI"

Should work! ✅

---

## 💡 Still Not Working?

### Check Logs

**FastAPI logs (Terminal where you ran `run_api.sh`):**
Look for lines like:
```
INFO:     Initializing anthropic with model claude-sonnet-4-20250514
INFO:     Using custom base URL: http://localhost:8000/v1
ERROR:    anthropic.NotFoundError: 404 page not found
```

The logs show exactly what URL it's trying to hit.

### Get Help

1. **Run diagnostic:**
   ```bash
   python test_proxy_config.py
   ```

2. **Share output** with the error message

3. **Include:**
   - Proxy software you're using (LiteLLM, custom, corporate?)
   - Base URL you're trying
   - Full error message from logs

---

## ✅ Success Checklist

- [ ] Proxy is actually running (curl test passes)
- [ ] Base URL format is correct (just base, not full endpoint)
- [ ] API key is valid (test at console.anthropic.com)
- [ ] Using correct port number
- [ ] Tried diagnostic tool: `python test_proxy_config.py`

---

## 🎯 Most Common Solution

**90% of 404 errors are fixed by:**

1. **Using direct connection** (no proxy)
   - Uncheck "Use Custom Base URL"
   - Just enter API key
   - Most people don't actually need a proxy!

2. **Fixing the base URL format:**
   - ❌ `http://localhost:8000/v1/messages`
   - ✅ `http://localhost:8000/v1`

3. **Starting the proxy first:**
   - Make sure it's running before configuring it!

---

**Try the simplest solution first: Direct connection (no proxy)!** 🚀
