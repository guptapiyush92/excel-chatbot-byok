"""
FastAPI Backend for Excel Chatbot
Corporate-friendly version with no WebSocket dependencies
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
from pathlib import Path
import tempfile
import shutil
import logging
import uuid
import time
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader import ExcelDataLoader
from src.vector_store import VectorStore, VectorStoreManager
from src.llm_provider import MultiProviderLLM, create_llm_client

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Excel Chatbot API",
    description="Corporate-friendly Excel chatbot with multi-provider AI support",
    version="1.0.0"
)

# CORS middleware - configure appropriately for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage (in-memory for now, use Redis/database for production)
sessions: Dict[str, Dict[str, Any]] = {}

# Models
class InitializeAIRequest(BaseModel):
    provider: str
    api_key: str
    model: str
    base_url: Optional[str] = None

class QueryRequest(BaseModel):
    session_id: str
    query: str

class SessionResponse(BaseModel):
    session_id: str
    provider: str
    model: str
    stats: Optional[Dict[str, int]] = None

# Routes

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page"""
    html_file = Path(__file__).parent / "templates" / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>Excel Chatbot API</h1><p>Access /docs for API documentation</p>")

@app.get("/test-markdown", response_class=HTMLResponse)
async def test_markdown():
    """Test page for markdown rendering"""
    html_file = Path(__file__).parent / "templates" / "test_markdown.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>Test page not found</h1>")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/providers")
async def get_providers():
    """Get available AI providers"""
    providers = MultiProviderLLM.get_available_providers()
    return {"providers": providers}

@app.post("/api/initialize")
async def initialize_ai(request: InitializeAIRequest):
    """Initialize AI provider with API key"""
    try:
        # Log configuration (without exposing full API key)
        masked_key = request.api_key[:15] + "..." if len(request.api_key) > 15 else "***"
        logger.info(f"Initializing {request.provider} with model {request.model}")
        if request.base_url:
            logger.info(f"Using custom base URL: {request.base_url}")

        # Create LLM client
        llm_client = create_llm_client(
            provider=request.provider,
            api_key=request.api_key,
            model=request.model,
            base_url=request.base_url
        )

        # Create session
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "llm_client": llm_client,
            "provider": request.provider,
            "model": request.model,
            "base_url": request.base_url,
            "created_at": time.time(),
            "vector_store": None,
            "dataframes": None,
            "stats": None,
            "temp_dir": None,
            "messages": []
        }

        logger.info(f"Created session {session_id} with {request.provider}/{request.model}")

        return {
            "success": True,
            "session_id": session_id,
            "provider": request.provider,
            "model": request.model
        }

    except Exception as e:
        logger.error(f"Error initializing AI: {e}", exc_info=True)
        error_msg = str(e)

        # Provide more helpful error messages
        if "404" in error_msg or "Not Found" in error_msg:
            error_msg = f"404 Not Found - Check your base URL. The endpoint might be incorrect. Error: {error_msg}"
        elif "401" in error_msg or "Unauthorized" in error_msg:
            error_msg = f"401 Unauthorized - Check your API key is correct and valid for this proxy. Error: {error_msg}"
        elif "Connection" in error_msg:
            error_msg = f"Connection failed - Is your proxy running? Check the base URL. Error: {error_msg}"

        raise HTTPException(status_code=400, detail=error_msg)

@app.post("/api/upload")
async def upload_files(
    session_id: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """Upload and process Excel files"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    if "llm_client" not in session:
        raise HTTPException(status_code=400, detail="AI not initialized")

    try:
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        file_paths = []

        # Save uploaded files
        for file in files:
            if not file.filename.endswith(('.xlsx', '.xls')):
                shutil.rmtree(temp_dir, ignore_errors=True)
                raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}")

            file_path = Path(temp_dir) / file.filename
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            file_paths.append(str(file_path))

        logger.info(f"Processing {len(file_paths)} files for session {session_id}")

        # Load data
        loader = ExcelDataLoader(file_paths)
        analysis = loader.analyze_structure()
        dataframes = loader.load_all_data()

        # Prepare documents
        documents = loader.prepare_documents_for_embedding(max_rows_per_chunk=25)

        # Create vector store
        collection_name = f"excel_data_{session_id}"
        vector_store = VectorStore(collection_name=collection_name)

        # Index documents
        manager = VectorStoreManager(vector_store)
        manager.index_excel_data(documents)

        # Calculate stats
        total_rows = sum(len(df) for sheets in dataframes.values() for df in sheets.values())
        total_sheets = sum(len(sheets) for sheets in dataframes.values())

        # Update session
        session["vector_store"] = vector_store
        session["dataframes"] = dataframes
        session["temp_dir"] = temp_dir
        session["stats"] = {
            "total_files": len(file_paths),
            "total_sheets": total_sheets,
            "total_rows": total_rows,
            "total_documents": len(documents)
        }
        session["messages"] = []

        logger.info(f"Successfully processed files for session {session_id}")

        return {
            "success": True,
            "stats": session["stats"]
        }

    except Exception as e:
        logger.error(f"Error processing files: {e}", exc_info=True)
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query")
async def query_data(request: QueryRequest):
    """Query the uploaded data"""
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[request.session_id]

    if not session.get("vector_store"):
        raise HTTPException(status_code=400, detail="No data uploaded")

    try:
        # Search vector store
        results = session["vector_store"].search(request.query, n_results=5)

        # Build context - handle both enabled and disabled vector store
        context_parts = []
        if 'documents' in results and 'metadatas' in results:
            # VectorStore enabled - has documents and metadatas
            for doc, metadata in zip(results['documents'], results['metadatas']):
                context_parts.append(f"From {metadata['file']} - {metadata['sheet']}:\n{doc}\n")
        # else: VectorStore disabled - results only has 'results' and 'query', no context available

        context = "\n".join(context_parts) if context_parts else "No semantic search context available (searching across all data)."

        # Build schema info
        schema_info = []
        for file_name, sheets in session["dataframes"].items():
            schema_info.append(f"File: {file_name}")
            for sheet_name, df in sheets.items():
                schema_info.append(f"  Sheet: {sheet_name} ({len(df)} rows)")
                schema_info.append(f"  Columns: {', '.join(df.columns.tolist())}")

        schema_text = "\n".join(schema_info)

        # Create messages
        messages = [
            {
                "role": "system",
                "content": f"""You are an expert data analyst helping users understand their Excel data.

Available Data:
{schema_text}

Response Formatting Guidelines:
- Use **bold** for emphasis and important numbers
- Use tables (markdown format) when presenting structured data
- Use bullet points or numbered lists for multiple items
- Use code blocks with ``` for formulas, SQL, or technical content
- Use headings (##, ###) to organize longer responses
- Be clear and well-formatted for readability

Use the provided context to answer questions accurately. If you're not sure, say so."""
            },
            {
                "role": "user",
                "content": f"""Context from data:
{context}

Question: {request.query}

Please provide a clear, well-formatted answer based on the data. Use markdown formatting (tables, lists, bold text) to make your response easy to read."""
            }
        ]

        # Generate response
        response = session["llm_client"].generate(messages, max_tokens=2048, temperature=0.7)

        # Store in message history
        session["messages"].append({"role": "user", "content": request.query})
        session["messages"].append({"role": "assistant", "content": response})

        return {
            "success": True,
            "answer": response,
            "context": context[:500] + "..." if len(context) > 500 else context
        }

    except Exception as e:
        logger.error(f"Error querying data: {e}", exc_info=True)

        # Provide more helpful error messages
        error_msg = str(e)
        if "404" in error_msg or "Not Found" in error_msg:
            base_url = session.get("base_url", "default Anthropic endpoint")
            error_msg = f"404 Not Found - The proxy endpoint is incorrect. Base URL used: {base_url}. Check your proxy configuration."
        elif "401" in error_msg or "Unauthorized" in error_msg:
            error_msg = f"401 Unauthorized - API key authentication failed. Verify your API key is correct."
        elif "Connection" in error_msg:
            base_url = session.get("base_url", "Anthropic")
            error_msg = f"Connection failed to {base_url}. Is your proxy running?"

        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    return {
        "session_id": session_id,
        "provider": session.get("provider"),
        "model": session.get("model"),
        "stats": session.get("stats"),
        "has_data": session.get("vector_store") is not None,
        "message_count": len(session.get("messages", []))
    }

@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session and clean up resources"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    # Clean up temp directory
    if session.get("temp_dir"):
        shutil.rmtree(session["temp_dir"], ignore_errors=True)

    # Remove session
    del sessions[session_id]

    logger.info(f"Deleted session {session_id}")

    return {"success": True, "message": "Session deleted"}

@app.get("/api/messages/{session_id}")
async def get_messages(session_id: str):
    """Get message history for a session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    return {
        "messages": session.get("messages", [])
    }

# Mount static files (for serving HTML/CSS/JS)
try:
    static_path = Path(__file__).parent / "static"
    if static_path.exists():
        app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
except Exception as e:
    logger.warning(f"Could not mount static files: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
