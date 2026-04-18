# Excel Chatbot Architecture

## Overview

This document explains the architecture of both versions of the Excel Chatbot.

---

## System Architecture

### Common Components (Shared by Both Versions)

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                  │
│           (Streamlit UI or HTML/JS Frontend)             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                  Application Layer                       │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────────┐ │
│  │ Data Loader  │  │ Vector Store│  │  LLM Provider  │ │
│  │ (Excel→Data) │  │  (ChromaDB) │  │ (Multi-Model)  │ │
│  └──────────────┘  └─────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                   External Services                      │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────────┐ │
│  │   Anthropic  │  │   Google    │  │     OpenAI     │ │
│  │    Claude    │  │   Gemini    │  │      GPT       │ │
│  └──────────────┘  └─────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Streamlit Version Architecture

```
┌──────────────────┐
│   User Browser   │
└────────┬─────────┘
         │ WebSocket (WS/WSS)
         │ Bidirectional, Persistent
         ↓
┌─────────────────────────────────────┐
│      Streamlit Server (Python)      │
│                                     │
│  ┌─────────────────────────────┐  │
│  │  chatbot_byok_ui.py         │  │
│  │  - Session State Management │  │
│  │  - File Upload Widget       │  │
│  │  - Chat Interface           │  │
│  │  - Real-time Updates        │  │
│  └───────────┬─────────────────┘  │
│              │                     │
│              ↓                     │
│  ┌─────────────────────────────┐  │
│  │  Core Business Logic        │  │
│  │  (src/ folder)              │  │
│  │                             │  │
│  │  • ExcelDataLoader          │  │
│  │  • VectorStore              │  │
│  │  • MultiProviderLLM         │  │
│  └─────────────────────────────┘  │
└─────────────────────────────────────┘
         │
         ↓
    AI Providers
```

**Key Characteristics:**
- Single Python process
- WebSocket for real-time communication
- Built-in session management
- Hot reload during development

---

## FastAPI Version Architecture

```
┌──────────────────┐
│   User Browser   │
│   (HTML/JS/CSS)  │
└────────┬─────────┘
         │ HTTP/HTTPS
         │ Request/Response
         │
         ↓
┌─────────────────────────────────────┐
│      FastAPI Server (Python)        │
│                                     │
│  ┌─────────────────────────────┐  │
│  │  api/main.py                │  │
│  │  - REST API Endpoints       │  │
│  │  - Session Management       │  │
│  │  - File Upload Handler      │  │
│  │  - Query Processor          │  │
│  └───────────┬─────────────────┘  │
│              │                     │
│              ↓                     │
│  ┌─────────────────────────────┐  │
│  │  Core Business Logic        │  │
│  │  (src/ folder)              │  │
│  │                             │  │
│  │  • ExcelDataLoader          │  │
│  │  • VectorStore              │  │
│  │  • MultiProviderLLM         │  │
│  └─────────────────────────────┘  │
└─────────────────────────────────────┘
         │
         ↓
    AI Providers
```

**Key Characteristics:**
- Separate frontend and backend
- RESTful API architecture
- Stateless HTTP requests
- Can scale horizontally

---

## Data Flow

### 1. File Upload Flow

```
User uploads Excel file
         │
         ↓
    [Save to temp]
         │
         ↓
  [ExcelDataLoader]
    • Read Excel file
    • Analyze structure
    • Extract data
         │
         ↓
 [Prepare Documents]
    • Chunk data (25 rows)
    • Add metadata
         │
         ↓
   [VectorStore]
    • Generate embeddings
    • Index in ChromaDB
         │
         ↓
 [Ready for queries]
```

### 2. Query Flow

```
User asks question
         │
         ↓
 [Embed question]
  (same model)
         │
         ↓
[Vector similarity search]
    • Find top 5 matches
    • Retrieve context
         │
         ↓
  [Build LLM prompt]
    • System message
    • Context
    • Question
         │
         ↓
  [Call AI Provider]
    Claude/Gemini/GPT
         │
         ↓
 [Return answer]
    Display to user
```

---

## Component Details

### ExcelDataLoader (`src/data_loader.py`)

**Responsibilities:**
- Read Excel files (.xlsx, .xls)
- Analyze structure (sheets, columns, rows)
- Load data into pandas DataFrames
- Prepare documents for embedding

**Key Methods:**
```python
load_all_data()          # Load all sheets from all files
analyze_structure()      # Get metadata about files
prepare_documents()      # Create embeddable chunks
```

### VectorStore (`src/vector_store.py`)

**Responsibilities:**
- Initialize ChromaDB
- Generate embeddings
- Index documents
- Similarity search

**Key Methods:**
```python
add_documents()          # Index new data
search()                 # Find similar content
get_collection()         # Access stored data
```

### MultiProviderLLM (`src/llm_provider.py`)

**Responsibilities:**
- Abstract multiple AI providers
- Handle API calls
- Normalize responses

**Supported Providers:**
```python
- Anthropic Claude (claude-sonnet-4, claude-opus-4)
- Google Gemini (gemini-2.0-flash, gemini-1.5-pro)
- OpenAI GPT (gpt-4o, gpt-4-turbo)
```

---

## Session Management

### Streamlit Version

```python
# Built-in session state
st.session_state.llm_client = llm_client
st.session_state.vector_store = vector_store
st.session_state.messages = []

# Persists across reruns
# Lives in server memory
# Tied to browser session
```

### FastAPI Version

```python
# Custom session dictionary
sessions = {
    "session_id": {
        "llm_client": client,
        "vector_store": store,
        "messages": [],
        "created_at": time.time()
    }
}

# Can use Redis for production
# Can share across servers
# Explicitly managed
```

---

## Network Communication

### Streamlit (WebSocket)

```
Initial:  Browser ──[HTTP GET]──> Server
          Browser <──[HTTP 200]──  Server

Upgrade:  Browser ──[Upgrade: websocket]──> Server
          Browser <──[101 Switching]───────  Server

Active:   Browser ⇄ [WebSocket Messages] ⇄ Server

          (Persistent, bidirectional)
```

**Problems in Corporate Environments:**
- Firewall may block WebSocket upgrade
- Proxy may not support WebSocket
- Security scans may flag persistent connections

### FastAPI (HTTP)

```
Request:  Browser ──[POST /api/query]──> Server
          Browser <──[200 OK + JSON]───  Server

Request:  Browser ──[POST /api/upload]──> Server
          Browser <──[200 OK + JSON]────  Server

(Each request is independent, stateless)
```

**Works in Corporate Environments:**
- Standard HTTP/HTTPS
- All firewalls allow HTTP
- Proxies handle HTTP well
- No persistent connections

---

## Deployment Models

### Local Development

Both versions:
```bash
# Streamlit
streamlit run ui/chatbot_byok_ui.py

# FastAPI
bash run_api.sh
```

### Docker Deployment

**Streamlit:**
```dockerfile
FROM python:3.11-slim
RUN pip install streamlit
CMD ["streamlit", "run", "ui/chatbot_byok_ui.py"]
```

**FastAPI:**
```dockerfile
FROM python:3.11-slim
RUN pip install fastapi uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
```

### Production Deployment

**Streamlit:**
- Streamlit Cloud (managed)
- Custom server with nginx
- Docker container

**FastAPI:**
- Any cloud provider (AWS, GCP, Azure)
- Behind nginx/Apache
- Docker + Kubernetes
- Serverless (with adaptations)

---

## Security Architecture

### Authentication (Optional, Add as Needed)

```
┌──────────────┐
│    User      │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│  API Key     │ ← Can add: JWT tokens
│  Validation  │           OAuth2
└──────┬───────┘           SSO
       │
       ↓
┌──────────────┐
│  Application │
└──────────────┘
```

### Data Flow Security

```
User Browser ─[HTTPS]→ Server ─[HTTPS]→ AI Provider
                │
                ↓
         [Temporary Storage]
         (Deleted after session)
```

---

## Scalability

### Streamlit Scaling

```
Limited horizontal scaling
Better for vertical scaling

Single Server:
  ├── Process 1 (User A)
  ├── Process 2 (User B)
  └── Process N (User N)

Max ~50 concurrent users per server
```

### FastAPI Scaling

```
Excellent horizontal scaling

Load Balancer
    │
    ├─→ Server 1 (Workers 1-4)
    ├─→ Server 2 (Workers 1-4)
    └─→ Server N (Workers 1-4)

Can handle thousands of concurrent users
```

---

## File Structure

```
excel_chatbot/
├── api/                      # FastAPI version
│   ├── main.py              # API endpoints
│   ├── config.py            # Configuration
│   └── templates/
│       └── index.html       # Frontend
├── ui/                       # Streamlit version
│   ├── chatbot_byok_ui.py  # BYOK UI
│   └── chatbot_upload_ui.py # Proxy UI
├── src/                      # Shared core logic
│   ├── data_loader.py       # Excel processing
│   ├── vector_store.py      # ChromaDB interface
│   ├── llm_provider.py      # Multi-provider LLM
│   ├── chatbot.py           # Chatbot logic
│   └── hybrid_engine.py     # Hybrid search
├── requirements.txt          # Streamlit deps
├── requirements-api.txt      # FastAPI deps
└── run_api.sh               # FastAPI launcher
```

---

## Performance Characteristics

### Streamlit

- **Startup:** Fast (~2 seconds)
- **First Query:** Moderate (loading time)
- **Subsequent Queries:** Fast
- **Memory Usage:** Higher (persistent state)
- **CPU Usage:** Moderate

### FastAPI

- **Startup:** Very Fast (~1 second)
- **First Query:** Fast
- **Subsequent Queries:** Very Fast
- **Memory Usage:** Lower (stateless)
- **CPU Usage:** Lower

---

## Summary

Both architectures share the same core business logic (`src/` folder) but differ in their communication layer:

- **Streamlit:** WebSocket-based, monolithic, rapid development
- **FastAPI:** HTTP-based, microservice-ready, production-grade

Choose based on your deployment environment and requirements!
