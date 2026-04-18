# Excel Chatbot - Multi-Provider AI

A powerful chatbot for querying Excel data using natural language. Supports **Anthropic Claude**, **Google Gemini**, and **OpenAI GPT**.

## ⚡ Quick Start

```bash
# 1. Clone repository
git clone https://github.com/guptapiyush92/excel-chatbot-byok.git
cd excel-chatbot-byok

# 2. Setup
bash scripts/quick_setup.sh        # macOS/Linux
scripts\quick_setup.bat            # Windows

# 3. Run FastAPI (Corporate-friendly, no WebSocket)
bash scripts/run_api.sh            # macOS/Linux
scripts\run_api.bat                # Windows

# OR Run Streamlit (Rapid development)
bash scripts/run_streamlit.sh      # macOS/Linux
scripts\run_streamlit.bat          # Windows
```

---

## 🎯 Two Versions Available

### FastAPI Version (Recommended for Corporate)
- ✅ No WebSocket - works behind any firewall
- ✅ Rich markdown formatting (tables, code highlighting)
- ✅ REST API endpoints
- ✅ Production-ready
- **Run:** `bash scripts/run_api.sh`
- **URL:** http://localhost:8000

### Streamlit Version (Rapid Development)
- ✅ Quick prototyping
- ✅ Built-in widgets
- ✅ Simpler code
- **Run:** `bash scripts/run_streamlit.sh`
- **URL:** http://localhost:8501

---

## 📁 Project Structure

```
excel_chatbot/
├── api/                 # FastAPI application
│   ├── main.py         # FastAPI server
│   ├── config.py       # Configuration
│   └── templates/      # HTML templates
├── ui/                  # Streamlit applications
│   ├── chatbot_byok_ui.py      # BYOK version
│   └── chatbot_upload_ui.py    # Proxy version
├── src/                 # Core business logic
│   ├── data_loader.py  # Excel file processing
│   ├── vector_store.py # ChromaDB integration
│   └── llm_provider.py # Multi-provider LLM
├── deployment/          # Deployment configurations
│   ├── docker/         # Docker configs
│   ├── kubernetes/     # K8s configs
│   └── nginx/          # Nginx configs
├── docs/               # Documentation
│   ├── guides/         # User guides
│   ├── api/            # API documentation
│   └── architecture/   # Architecture docs
├── scripts/            # Helper scripts
│   ├── quick_setup.sh  # Setup script
│   ├── run_api.sh      # Run FastAPI
│   └── run_streamlit.sh# Run Streamlit
├── tools/              # Development tools
└── tests/              # Test files
```

---

## 🔑 AI Providers

| Provider | Models | Free Tier | API Key |
|----------|--------|-----------|---------|
| 🟢 **Google Gemini** | Gemini 2.0 Flash, 1.5 Pro | ✅ Yes | [Get Key](https://makersuite.google.com/app/apikey) |
| 🔷 **Anthropic Claude** | Claude Sonnet 4, Opus 4 | Limited | [Get Key](https://console.anthropic.com/) |
| 🟦 **OpenAI GPT** | GPT-4o, GPT-4 Turbo | Limited | [Get Key](https://platform.openai.com/api-keys) |

---

## 📚 Documentation

- **[Quick Start Guide](docs/guides/QUICKSTART.md)** - Fast setup
- **[Setup From Scratch](docs/guides/SETUP_FROM_SCRATCH.md)** - Complete beginner guide
- **[FastAPI Deployment](docs/guides/FASTAPI_DEPLOYMENT.md)** - Corporate deployment
- **[Railway Deployment](docs/guides/RAILWAY_QUICKSTART.md)** - Free cloud hosting
- **[Corporate Deployment](docs/guides/CORPORATE_DEPLOYMENT.md)** - Enterprise guide
- **[Proxy Setup](docs/guides/PROXY_SETUP.md)** - Configure local proxy
- **[Troubleshooting](docs/guides/TROUBLESHOOTING_404.md)** - Fix common issues

---

## 🚀 Deployment Options

### Local Development
```bash
bash scripts/run_api.sh
```

### Docker
```bash
cd deployment/docker
docker-compose up -d
```

### Railway.app (Free Cloud)
1. Go to https://railway.app/
2. Deploy from GitHub
3. Set start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### Corporate Server
See [Corporate Deployment Guide](docs/guides/CORPORATE_DEPLOYMENT.md)

---

## ✨ Features

- 🤖 **Multi-Provider AI** - Claude, Gemini, GPT
- 🔑 **BYOK** - Users provide their own API keys
- 📊 **Large Datasets** - Handle 100k+ rows
- 🔍 **Semantic Search** - Vector-based retrieval
- 💬 **Natural Language** - Ask questions in plain English
- 📁 **Multiple Files** - Upload and query multiple Excel files
- 🎨 **Rich Formatting** - Tables, code blocks, syntax highlighting
- 🏢 **Firewall-Friendly** - FastAPI version works everywhere

---

## 💡 Example Queries

- "Show me the top 5 customers by revenue in a table"
- "What's the average sales by region?"
- "List all policies that matured in 2024"
- "Calculate total premium for segment S07"
- "Show me the SQL query to get this data"

---

## 🔧 Requirements

- Python 3.10+
- 4GB RAM (8GB recommended)
- 2GB disk space
- Internet connection (for AI API calls)

---

## 🛠️ Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
pytest tests/
```

### Code Structure
- `src/` - Core business logic (shared by both versions)
- `api/` - FastAPI-specific code
- `ui/` - Streamlit-specific code

---

## 📊 Comparison

| Feature | FastAPI | Streamlit |
|---------|---------|-----------|
| **WebSocket** | ❌ No | ✅ Yes |
| **Firewall** | ✅ Works | ⚠️ May block |
| **Formatting** | ✅ Rich | ⚠️ Limited |
| **API** | ✅ Yes | ❌ No |
| **Setup** | ⭐⭐ Moderate | ⭐ Easy |
| **Production** | ✅ Ready | ⚠️ Needs config |

**Recommendation:** Use FastAPI for corporate/production, Streamlit for quick demos.

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
export API_PORT=8001  # Use different port
bash scripts/run_api.sh
```

### Module Not Found
```bash
source venv/bin/activate  # Activate venv first
pip install -r requirements.txt
```

### WebSocket Errors (Streamlit)
Switch to FastAPI version - no WebSocket issues!

See [Troubleshooting Guide](docs/guides/TROUBLESHOOTING_404.md) for more.

---

## 📄 License

MIT

---

## 🤝 Contributing

Pull requests welcome! Please ensure:
- Code follows existing style
- Tests pass
- Documentation updated

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/guptapiyush92/excel-chatbot-byok/issues)
- **Docs:** See `docs/` folder
- **Guides:** See `docs/guides/`

---

**Built with ❤️ for analyzing Excel data with AI**
