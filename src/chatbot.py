"""
Chatbot module with Claude API integration and RAG pipeline.
Handles query processing, context retrieval, and answer generation.
"""

from anthropic import Anthropic
from typing import List, Dict, Any, Optional
import logging
import os
from dotenv import load_dotenv
from vector_store import VectorStore, VectorStoreManager
from data_loader import ExcelDataLoader
import json

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExcelChatbot:
    """Chatbot for querying Excel data using natural language."""

    def __init__(
        self,
        vector_store: VectorStore,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet"
    ):
        """
        Initialize the chatbot.

        Args:
            vector_store: VectorStore instance
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
            model: Claude model to use
        """
        self.vector_store = vector_store
        self.model = model

        # Initialize Anthropic client
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY must be provided or set in environment")

        # Get base URL for corporate proxy support
        base_url = os.getenv("ANTHROPIC_BASE_URL")

        if base_url:
            self.client = Anthropic(api_key=api_key, base_url=base_url)
            logger.info(f"Initialized chatbot with model: {model}, base_url: {base_url}")
        else:
            self.client = Anthropic(api_key=api_key)
            logger.info(f"Initialized chatbot with model: {model}")

        # Conversation history
        self.conversation_history = []

    def build_context(self, query: str, n_results: int = 5) -> str:
        """
        Retrieve relevant context for a query.

        Args:
            query: User query
            n_results: Number of results to retrieve

        Returns:
            Formatted context string
        """
        logger.info(f"Retrieving context for query: {query}")

        # Search vector store
        results = self.vector_store.search(query, n_results=n_results)

        # Build context string
        context_parts = ["# Relevant Data from Excel Files\n"]

        for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas']), 1):
            context_parts.append(f"\n## Context {i}")
            context_parts.append(f"Source: {metadata.get('file', 'unknown')} - {metadata.get('sheet', 'unknown')}")
            context_parts.append(f"Rows: {metadata.get('start_row', 'N/A')} to {metadata.get('end_row', 'N/A')}")
            context_parts.append(f"Content:\n{doc}\n")

        context = "\n".join(context_parts)
        logger.info(f"Built context with {len(results['documents'])} documents")

        return context

    def build_system_prompt(self) -> str:
        """
        Build the system prompt for Claude.

        Returns:
            System prompt string
        """
        return """You are an expert data analyst assistant specializing in actuarial and life insurance data.

Your role is to help users query and understand data from Excel files containing actuarial life insurance information.

Guidelines:
1. Analyze the provided context carefully to answer user questions
2. If the data shows specific numbers, provide them accurately
3. If you need to calculate or aggregate, explain your methodology
4. If the context doesn't contain enough information to fully answer the question, say so clearly
5. Provide insights and patterns when relevant
6. Format responses clearly with headings, bullet points, or tables when appropriate
7. When comparing data across files or sheets, note the sources
8. If you see relationships between data points, explain them

Remember:
- The context provided contains actual data from the Excel files
- Be precise with numbers and calculations
- Cite your sources (file and sheet names) when providing specific data points
"""

    def generate_response(
        self,
        query: str,
        context: str,
        include_history: bool = True
    ) -> str:
        """
        Generate a response using Claude API.

        Args:
            query: User query
            context: Retrieved context
            include_history: Whether to include conversation history

        Returns:
            Generated response
        """
        logger.info("Generating response with Claude API")

        # Build messages
        messages = []

        # Add conversation history if requested
        if include_history and self.conversation_history:
            messages.extend(self.conversation_history)

        # Add current query with context
        user_message = f"""Context from Excel files:
{context}

User Question: {query}

Please analyze the context and provide a detailed answer to the user's question."""

        messages.append({
            "role": "user",
            "content": user_message
        })

        # Call Claude API
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.build_system_prompt(),
                messages=messages
            )

            answer = response.content[0].text
            logger.info("Successfully generated response")

            # Update conversation history
            self.conversation_history.append({
                "role": "user",
                "content": query
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })

            # Keep only last 10 exchanges to manage token usage
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]

            return answer

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def query(
        self,
        user_query: str,
        n_results: int = 5,
        include_history: bool = True
    ) -> Dict[str, Any]:
        """
        Process a user query end-to-end.

        Args:
            user_query: User's question
            n_results: Number of context documents to retrieve
            include_history: Whether to include conversation history

        Returns:
            Dictionary with query, answer, and metadata
        """
        logger.info(f"Processing query: {user_query}")

        # Retrieve context
        context = self.build_context(user_query, n_results=n_results)

        # Generate response
        answer = self.generate_response(user_query, context, include_history)

        # Prepare result
        result = {
            'query': user_query,
            'answer': answer,
            'num_context_docs': n_results,
            'has_history': include_history
        }

        return result

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
        logger.info("Cleared conversation history")

    def get_data_summary(self) -> str:
        """
        Get a summary of available data.

        Returns:
            Summary string
        """
        stats = self.vector_store.get_collection_stats()

        summary = f"""# Available Data Summary

**Vector Store Statistics:**
- Collection: {stats['collection_name']}
- Total Documents: {stats['document_count']}
- Embedding Model: {stats['embedding_model']}

The data is indexed and ready for querying. You can ask questions about:
- Policy details and characteristics
- Policyholder demographics
- Premium amounts and payment patterns
- Claims and benefits
- Actuarial metrics
- Statistical summaries and comparisons
"""
        return summary


class ChatbotManager:
    """High-level manager for chatbot setup and operations."""

    @staticmethod
    def initialize_from_excel_files(
        file_paths: List[str],
        reset_index: bool = False
    ) -> ExcelChatbot:
        """
        Initialize chatbot from Excel files.

        Args:
            file_paths: Paths to Excel files
            reset_index: Whether to reset and rebuild the index

        Returns:
            Initialized ExcelChatbot instance
        """
        logger.info("Initializing chatbot from Excel files")

        # Load and prepare data
        loader = ExcelDataLoader(file_paths)

        # Analyze structure
        logger.info("Analyzing data structure...")
        analysis = loader.analyze_structure()
        logger.info(f"Found {len(analysis)} files")

        # Detect relationships
        relationships = loader.detect_relationships()
        logger.info(f"Detected {len(relationships)} potential relationships")

        # Prepare documents
        logger.info("Preparing documents for embedding...")
        documents = loader.prepare_documents_for_embedding(max_rows_per_chunk=50)

        # Initialize vector store
        logger.info("Initializing vector store...")
        vector_store = VectorStore()

        # Index documents if needed
        if reset_index or vector_store.collection.count() == 0:
            logger.info("Indexing documents...")
            manager = VectorStoreManager(vector_store)
            manager.index_excel_data(documents)
        else:
            logger.info(f"Using existing index with {vector_store.collection.count()} documents")

        # Create chatbot
        chatbot = ExcelChatbot(vector_store)
        logger.info("Chatbot initialized successfully")

        return chatbot


if __name__ == "__main__":
    # Example usage
    print("="*60)
    print("INITIALIZING CHATBOT")
    print("="*60)

    chatbot = ChatbotManager.initialize_from_excel_files(
        file_paths=[
            "actuarial_life_data_file1.xlsx",
            "actuarial_life_data_file2.xlsx"
        ],
        reset_index=True  # Set to False to use existing index
    )

    # Show data summary
    print("\n" + chatbot.get_data_summary())

    # Example queries
    example_queries = [
        "What data is available in these files?",
        "What are the average premium amounts?",
        "Show me information about policy durations",
    ]

    for query in example_queries:
        print("\n" + "="*60)
        print(f"QUERY: {query}")
        print("="*60)

        result = chatbot.query(query)
        print(f"\nANSWER:\n{result['answer']}")
