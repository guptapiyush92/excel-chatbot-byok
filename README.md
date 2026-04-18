# Excel Chatbot - Multi-Provider AI

A powerful chatbot system designed to query and analyze Excel datasets using natural language. Supports **Anthropic Claude**, **Google Gemini**, and **OpenAI GPT** with a flexible BYOK (Bring Your Own Key) architecture.

## ⚡ Quick Start

**New to development?** → [Complete Setup Guide (From Scratch)](SETUP_FROM_SCRATCH.md)

**Have Python installed?** → [Quick Start Guide](QUICKSTART.md)

**Ready to go?**
```bash
bash quick_setup.sh        # macOS/Linux
quick_setup.bat            # Windows
```

Then run:
```bash
streamlit run ui/chatbot_byok_ui.py
```

## Features

- 🤖 **Multi-Provider Support**: Choose between Claude, Gemini, or GPT
- 🔑 **BYOK Architecture**: Users provide their own API keys (zero cost to you!)
- 📊 **Large Dataset Support**: Handles Excel files with 100,000+ rows efficiently
- 🔍 **Semantic Search**: Uses vector embeddings for intelligent data retrieval
- 💬 **Natural Language Queries**: Ask questions in plain English about your data
- 📁 **Multi-file Analysis**: Upload and query multiple Excel files simultaneously
- ⚡ **Fast Performance**: Optimized chunking and caching strategies
- 🎨 **Interactive UI**: Simple web interface built with Streamlit

## Architecture

```
Excel Files → Data Loader → Chunking → Embeddings → Vector DB (ChromaDB)
                                                            ↓
User Query → Claude API ← Context Retrieval ← Vector Search
```

## 📚 Documentation

- 🚀 **[Quick Start Guide](QUICKSTART.md)** - Fast setup for experienced developers
- 📖 **[Complete Setup Guide](SETUP_FROM_SCRATCH.md)** - Step-by-step for beginners (no Python/Git required)
- 🔄 **[Deployment Options](DEPLOYMENT_OPTIONS.md)** - BYOK vs Proxy mode comparison
- 🌐 **[How to Run](HOW_TO_RUN.md)** - Detailed usage instructions

## Installation

### Automated Setup (Recommended)

**macOS/Linux:**
```bash
bash quick_setup.sh
```

**Windows:**
```bash
quick_setup.bat
```

### Manual Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up environment variables for proxy mode:
```bash
cp .env.example .env
# Edit .env and add your API key
```

## Usage

### BYOK Mode (Recommended)
Users provide their own API keys through the UI:
```bash
streamlit run ui/chatbot_byok_ui.py
```

### Proxy Mode
You provide the API key via `.env` file:
```bash
streamlit run ui/chatbot_upload_ui.py
```

Then open **http://localhost:8501** in your browser.

## 🎯 Use Cases

- 📊 Actuarial life data analysis
- 💼 Business intelligence queries
- 📈 Financial data exploration
- 🔬 Research data analysis
- 📋 Any Excel-based dataset analysis

## 🔑 Supported AI Providers

| Provider | Models | Free Tier | API Key Link |
|----------|--------|-----------|--------------|
| 🟢 **Google Gemini** | Gemini 2.0 Flash, 1.5 Pro | ✅ Yes | [Get Key](https://makersuite.google.com/app/apikey) |
| 🔷 **Anthropic Claude** | Claude Sonnet 4, Opus 4 | Limited | [Get Key](https://console.anthropic.com/) |
| 🟦 **OpenAI GPT** | GPT-4o, GPT-4 Turbo | Limited | [Get Key](https://platform.openai.com/api-keys) |

## How It Works

1. **Data Loading**: Reads Excel files in chunks to handle large datasets
2. **Embedding Generation**: Converts data rows into vector embeddings
3. **Vector Storage**: Stores embeddings in ChromaDB for fast retrieval
4. **Query Processing**: User queries are embedded and matched against stored vectors
5. **Context Retrieval**: Most relevant data chunks are retrieved
6. **Answer Generation**: Claude API generates natural language answers based on retrieved context

## Performance Optimization

- Chunked data loading for memory efficiency
- Vector indexing for fast similarity search
- Query caching to avoid redundant processing
- Batch processing for embedding generation

## 💡 Example Queries

- "What is the average premium for policies issued in 2023?"
- "Show me all policies with surrender values greater than $50,000"
- "Compare mortality rates between male and female policyholders"
- "What's the relationship between policy duration and claim amounts?"
- "Summarize the data in Sheet 1"
- "How many unique customers are there?"

## 🔧 Troubleshooting

### Corporate Firewall Blocking Streamlit Cloud?
**Solution**: Run locally! Follow the [Setup Guide](SETUP_FROM_SCRATCH.md) to run the app on your local machine, bypassing network restrictions.

### WebSocket Connection Errors?
When running **locally**, WebSocket issues are eliminated since everything runs on your machine.

### Common Issues
- **Python not found**: Make sure Python is installed and added to PATH
- **Module not found**: Activate virtual environment first
- **Port already in use**: Use `--server.port 8502` flag
- **Memory errors**: Process smaller files or upgrade system RAM

See [SETUP_FROM_SCRATCH.md](SETUP_FROM_SCRATCH.md) for detailed troubleshooting.

## License

MIT
