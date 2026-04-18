# FastAPI Corporate Deployment Guide

## 🏢 Why FastAPI Version?

The FastAPI version of the Excel Chatbot is specifically designed for **corporate environments** where:

- ✅ **WebSocket connections are blocked** by firewalls
- ✅ **Traditional HTTP/HTTPS only** is allowed
- ✅ **No streaming connections** permitted
- ✅ **Standard REST API** patterns required
- ✅ **Behind corporate proxies** or VPNs

Unlike Streamlit which relies on WebSocket connections, **FastAPI uses standard HTTP requests** that work with any firewall configuration.

---

## 🚀 Quick Start

### 1. Setup (First Time Only)

```bash
# Clone the repository
git clone YOUR_GITHUB_REPO_URL
cd excel_chatbot

# Run setup
bash quick_setup.sh        # macOS/Linux
quick_setup.bat            # Windows

# Install FastAPI requirements
pip install -r requirements-api.txt
```

### 2. Run the Application

```bash
# macOS/Linux
bash run_api.sh

# Windows
run_api.bat
```

### 3. Access the Application

Open your browser and go to:
```
http://localhost:8000
```

That's it! No WebSocket connections, no firewall issues.

---

## 📋 Features

### Corporate-Friendly Architecture

- **Standard HTTP/HTTPS** - No WebSocket requirements
- **RESTful API** - Industry-standard API design
- **Simple Deployment** - Single command to start
- **Firewall Compatible** - Works behind any corporate firewall
- **Proxy Friendly** - Compatible with corporate proxies

### Multi-Provider Support

- 🔷 **Anthropic Claude** - Claude Sonnet 4, Opus 4
- 🟢 **Google Gemini** - Gemini 2.0 Flash (Free!), 1.5 Pro
- 🟦 **OpenAI GPT** - GPT-4o, GPT-4 Turbo

### BYOK (Bring Your Own Key)

- Users provide their own API keys
- No cost to the organization
- Each user controls their own usage
- Support for corporate API key management

---

## 🏗️ Architecture

```
┌─────────────┐
│   Browser   │ ← Standard HTTP Requests (No WebSocket!)
│  (HTML/JS)  │
└──────┬──────┘
       │
       ↓ HTTP REST API
┌─────────────────┐
│  FastAPI Server │
│   (Python)      │
├─────────────────┤
│ • File Upload   │
│ • Data Processing│
│ • Vector Store  │
│ • LLM Interface │
└──────┬──────────┘
       │
       ↓
┌──────────────────┐
│  AI Providers    │
│ Claude/Gemini/GPT│
└──────────────────┘
```

**Key Difference from Streamlit:**
- Streamlit: Uses WebSocket for real-time updates
- FastAPI: Uses standard HTTP POST/GET requests

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file (optional):

```bash
# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1

# CORS (for production, restrict this)
CORS_ORIGINS=*

# Session Settings
SESSION_TIMEOUT=3600

# Max upload size (bytes)
MAX_UPLOAD_SIZE=52428800

# Logging
LOG_LEVEL=INFO
```

### Corporate Proxy Configuration

If behind a corporate proxy, set these environment variables:

```bash
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1
```

Windows:
```cmd
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080
set NO_PROXY=localhost,127.0.0.1
```

---

## 🌐 Production Deployment

### Option 1: Internal Server (Recommended for Corporate)

Deploy on an internal company server:

```bash
# Install dependencies
pip install -r requirements-api.txt

# Run with production settings
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Option 2: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t excel-chatbot-api .
docker run -p 8000:8000 excel-chatbot-api
```

### Option 3: Behind Nginx (Corporate Standard)

Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Option 4: Windows Server (IIS)

1. Install Python on Windows Server
2. Use `wfastcgi` or `HttpPlatformHandler`
3. Configure IIS to proxy to FastAPI

---

## 🔒 Security Considerations

### For Production Deployment

1. **CORS Configuration**
   ```python
   # In api/main.py, update CORS origins:
   allow_origins=["https://your-domain.com"]
   ```

2. **API Key Validation**
   - Implement rate limiting
   - Add authentication/authorization
   - Use API key encryption

3. **File Upload Limits**
   - Already configured (50MB default)
   - Adjust `MAX_UPLOAD_SIZE` as needed

4. **HTTPS Only**
   - Use reverse proxy (Nginx) with SSL
   - Obtain SSL certificate (Let's Encrypt or corporate CA)

5. **Session Management**
   - Currently in-memory (fine for single instance)
   - For production: Use Redis or database

---

## 📊 Monitoring & Logs

### View Logs

Development:
```bash
# Logs appear in terminal
```

Production:
```bash
# Configure logging in api/config.py
LOG_LEVEL=INFO
LOG_FILE=/var/log/excel-chatbot.log
```

### Health Check Endpoint

```bash
curl http://localhost:8000/api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-04-18T12:00:00"
}
```

### API Documentation

FastAPI automatically generates interactive API docs:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🔄 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main HTML interface |
| GET | `/api/health` | Health check |
| GET | `/api/providers` | Available AI providers |
| POST | `/api/initialize` | Initialize AI with API key |
| POST | `/api/upload` | Upload Excel files |
| POST | `/api/query` | Query the data |
| GET | `/api/session/{id}` | Get session info |
| DELETE | `/api/session/{id}` | Delete session |
| GET | `/api/messages/{id}` | Get chat history |

### Example API Usage

**Initialize AI:**
```bash
curl -X POST http://localhost:8000/api/initialize \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "anthropic",
    "api_key": "sk-ant-...",
    "model": "claude-sonnet-4-20250514"
  }'
```

**Upload Files:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "session_id=your-session-id" \
  -F "files=@data.xlsx"
```

**Query Data:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "query": "What is the total revenue?"
  }'
```

---

## 🛠️ Troubleshooting

### Port Already in Use

```bash
# Use different port
export API_PORT=8001
bash run_api.sh
```

### Module Not Found

```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements-api.txt
```

### CORS Errors in Browser

Update CORS settings in `api/main.py`:
```python
allow_origins=["http://localhost:8000"]
```

### Session Not Persisting

For production, implement Redis-based sessions:
```bash
pip install redis
```

Update session storage in `api/main.py` to use Redis instead of dict.

### Large File Upload Timeout

Increase timeout in uvicorn:
```bash
uvicorn main:app --timeout-keep-alive 300
```

---

## 📈 Performance Tuning

### For High Traffic

1. **Multiple Workers**
   ```bash
   uvicorn main:app --workers 4
   ```

2. **Use Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Redis for Sessions**
   - Store sessions in Redis instead of memory
   - Enables horizontal scaling

4. **Database for Persistent Storage**
   - PostgreSQL for structured data
   - S3 for file storage

---

## 🔄 Comparison: Streamlit vs FastAPI

| Feature | Streamlit | FastAPI |
|---------|-----------|---------|
| **Connection Type** | WebSocket | HTTP |
| **Firewall Friendly** | ❌ Often blocked | ✅ Always works |
| **Corporate Proxy** | ❌ Issues | ✅ Compatible |
| **Deployment** | Complex | Simple |
| **API Access** | ❌ No | ✅ Yes |
| **Custom Frontend** | ❌ Limited | ✅ Full control |
| **Production Ready** | ⚠️ With config | ✅ Built-in |
| **Setup Complexity** | Easy | Moderate |

**When to use each:**

- **Streamlit**: Internal demos, rapid prototyping, development
- **FastAPI**: Production, corporate environments, strict firewall

---

## 🚀 Next Steps

1. **Development**: Run locally with `bash run_api.sh`
2. **Test**: Upload sample Excel files
3. **Production**: Deploy to internal server
4. **Scale**: Add workers, Redis, load balancer
5. **Monitor**: Set up logging and health checks
6. **Secure**: Configure CORS, add authentication

---

## 📞 Support

For issues specific to corporate deployment:

1. Check firewall allows port 8000 (or configured port)
2. Verify proxy settings if behind corporate proxy
3. Ensure Python and dependencies installed correctly
4. Check logs for detailed error messages

---

**Your FastAPI Excel Chatbot is now ready for corporate deployment!** 🎉

No WebSocket issues, no firewall problems, just reliable HTTP-based chat with your Excel data.
