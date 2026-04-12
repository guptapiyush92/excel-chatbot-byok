# Excel Chatbot for Actuarial Life Data

A powerful chatbot system designed to query and analyze large Excel datasets (100k+ rows) using natural language. Built with LangChain, Claude API, and ChromaDB for efficient semantic search and retrieval.

## Features

- **Large Dataset Support**: Handles Excel files with 100,000+ rows efficiently
- **Semantic Search**: Uses vector embeddings for intelligent data retrieval
- **Natural Language Queries**: Ask questions in plain English about your data
- **Multi-file Analysis**: Understands relationships between multiple Excel files
- **Fast Performance**: Optimized chunking and caching strategies
- **Interactive UI**: Simple web interface built with Streamlit

## Architecture

```
Excel Files → Data Loader → Chunking → Embeddings → Vector DB (ChromaDB)
                                                            ↓
User Query → Claude API ← Context Retrieval ← Vector Search
```

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage

### Command Line Interface
```bash
python chatbot_cli.py
```

### Web Interface
```bash
streamlit run chatbot_ui.py
```

## Data Files

The system works with two actuarial life data Excel files:
- `actuarial_life_data_file1.xlsx`
- `actuarial_life_data_file2.xlsx`

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

## Example Queries

- "What is the average premium for policies issued in 2023?"
- "Show me all policies with surrender values greater than $50,000"
- "Compare mortality rates between male and female policyholders"
- "What's the relationship between policy duration and claim amounts?"

## License

MIT
