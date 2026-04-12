# Excel Chatbot - User Guide

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [Features](#features)
5. [Example Queries](#example-queries)
6. [Troubleshooting](#troubleshooting)
7. [Architecture](#architecture)

## Installation

### Quick Setup
```bash
# Run the setup script
./setup.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

Get your API key from: https://console.anthropic.com/

## Usage

### Option 1: Command-Line Interface (CLI)

```bash
# Activate virtual environment
source venv/bin/activate

# Run the CLI
python chatbot_cli.py
```

**CLI Commands:**
- Type your question and press Enter
- `quit` or `exit` - Exit the chatbot
- `clear` - Clear conversation history
- `summary` - Show available data summary

### Option 2: Web Interface (Streamlit)

```bash
# Activate virtual environment
source venv/bin/activate

# Run the web app
streamlit run chatbot_ui.py
```

The web interface will open in your browser at `http://localhost:8501`

## Features

### 1. Large Dataset Support
- Handles 100,000+ rows efficiently
- Chunked data loading to manage memory
- Batch processing for embeddings

### 2. Semantic Search
- Vector embeddings for intelligent data retrieval
- ChromaDB for fast similarity search
- Context-aware query understanding

### 3. Natural Language Queries
- Ask questions in plain English
- No SQL or Excel formulas needed
- Conversational interface

### 4. Multi-file Analysis
- Automatically detects relationships between files
- Joins data across multiple sheets
- Cross-references information

### 5. Powered by Claude AI
- Advanced natural language understanding
- Context-aware responses
- Detailed explanations and insights

## Example Queries

### Basic Information
```
"What data is available in these files?"
"How many policies are there?"
"What columns are in the Policy_Details sheet?"
```

### Statistical Queries
```
"What is the average premium amount?"
"Show me the distribution of policies by class"
"What's the total sum assured across all policies?"
```

### Filtering and Selection
```
"Show me all policies issued in 2021"
"Find policies with premiums greater than 40,000"
"List all claims with Approved status"
```

### Comparative Analysis
```
"Compare average claim amounts by claim type"
"What's the difference in mortality rates between males and females?"
"Show persistency rates across different segments"
```

### Complex Queries
```
"What's the relationship between age and premium amounts?"
"Which segments have the highest claim rejection rates?"
"Analyze the correlation between sum assured and reserves"
```

### Claims Analysis
```
"How many death claims were approved?"
"What's the average settlement time for claims?"
"Show claims with potential fraud flags"
```

### Actuarial Questions
```
"What mortality assumptions are used for 30-year-old males?"
"Compare actual vs expected mortality by segment"
"What's the reserve coverage ratio for each policy class?"
```

## Troubleshooting

### Issue: "ANTHROPIC_API_KEY not found"
**Solution:** Make sure you've created `.env` file with your API key

### Issue: "Excel files not found"
**Solution:** Ensure both Excel files are in the project directory:
- `actuarial_life_data_file1.xlsx`
- `actuarial_life_data_file2.xlsx`

### Issue: "Module not found" errors
**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Slow initial startup
**Reason:** First run downloads the embedding model (~90MB) and indexes all data.
**Solution:** Wait for initialization to complete. Subsequent runs will be faster.

### Issue: "Out of memory" errors
**Solution:** Reduce `chunk_size` in `data_loader.py` or `max_rows_per_chunk` parameter

### Issue: Inaccurate responses
**Solutions:**
- Ask more specific questions
- Reference specific columns or sheets
- Break complex queries into simpler parts
- Use the `clear` command to reset conversation context

## Architecture

### Data Flow
```
Excel Files
    ↓
ExcelDataLoader (chunked reading)
    ↓
Document Preparation (text conversion)
    ↓
Embedding Generation (SentenceTransformer)
    ↓
Vector Storage (ChromaDB)
    ↓
User Query → Semantic Search → Context Retrieval
    ↓
Claude API (RAG pipeline)
    ↓
Natural Language Answer
```

### Components

**1. data_loader.py**
- Loads Excel files efficiently
- Handles large datasets with chunking
- Detects relationships between sheets
- Prepares data for embedding

**2. vector_store.py**
- Manages ChromaDB vector database
- Generates embeddings using sentence-transformers
- Performs similarity search
- Handles document indexing

**3. chatbot.py**
- Integrates Claude API
- Implements RAG (Retrieval-Augmented Generation) pipeline
- Manages conversation history
- Generates contextual responses

**4. chatbot_cli.py**
- Command-line interface
- Interactive query loop
- Simple and fast

**5. chatbot_ui.py**
- Web interface using Streamlit
- Visual chat interface
- Sidebar with controls and examples

### Performance Optimizations

1. **Chunked Data Loading**: Processes 10,000 rows at a time
2. **Batch Embeddings**: Generates 32 embeddings per batch
3. **Vector Indexing**: Fast similarity search (O(log n))
4. **Conversation Caching**: Maintains context for follow-up questions
5. **Persistent Storage**: ChromaDB persists to disk, avoiding re-indexing

## Advanced Usage

### Rebuilding the Index
If your data changes, rebuild the vector index:

```python
from chatbot import ChatbotManager

chatbot = ChatbotManager.initialize_from_excel_files(
    file_paths=["file1.xlsx", "file2.xlsx"],
    reset_index=True  # Force rebuild
)
```

### Adjusting Search Parameters
Modify the number of context documents retrieved:

```python
result = chatbot.query(
    "Your question here",
    n_results=10  # Default is 5
)
```

### Custom Embedding Models
Edit `vector_store.py` to use a different model:

```python
vector_store = VectorStore(
    embedding_model="sentence-transformers/all-mpnet-base-v2"
)
```

## Best Practices

1. **Be Specific**: "Show policies issued in 2021 with premiums > 30000" is better than "Show some policies"

2. **Use Context**: The chatbot remembers conversation history, so you can ask follow-up questions

3. **Reference Sources**: Ask about specific sheets or columns when you know them

4. **Break Down Complex Queries**: Split complex analysis into multiple questions

5. **Clear History**: Use `clear` command when switching topics to avoid confusion

## Data Privacy

- All processing happens locally or through Anthropic's API
- No data is stored on third-party servers (except Anthropic for query processing)
- ChromaDB stores data locally in `./chroma_db/`
- Conversation history is session-only (not persisted)

## Support

For issues or questions:
1. Check this guide's Troubleshooting section
2. Review the data structure in `DATA_STRUCTURE.md`
3. Check the code comments in source files

## License

MIT License - See LICENSE file for details
