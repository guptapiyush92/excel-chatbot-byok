"""
Vector store module for managing embeddings and similarity search.
Uses ChromaDB for efficient vector storage and retrieval.
"""

from typing import List, Dict, Any, Optional
import logging
import os
from pathlib import Path
import json

# Optional imports for semantic search
try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logger_temp = logging.getLogger(__name__)
    logger_temp.warning("ChromaDB and/or sentence-transformers not available. Semantic search disabled.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:
    """Manages vector embeddings and similarity search for Excel data."""

    def __init__(
        self,
        collection_name: str = "excel_data",
        persist_directory: str = "./chroma_db",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        """
        Initialize the vector store.

        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the database
            embedding_model: Model to use for generating embeddings
        """
        if not CHROMADB_AVAILABLE:
            logger.warning("Semantic search not available - ChromaDB/sentence-transformers not installed")
            self.enabled = False
            return

        self.enabled = True
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model

        # Create persist directory if it doesn't exist
        Path(persist_directory).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            logger.info(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(name=collection_name)
            logger.info(f"Created new collection: {collection_name}")

        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        logger.info("Embedding model loaded successfully")

    def generate_embeddings(self, texts: List[str], batch_size: int = 16) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings
            batch_size: Number of texts to process at once

        Returns:
            List of embedding vectors
        """
        if not self.enabled:
            return []

        logger.info(f"Generating embeddings for {len(texts)} texts")
        embeddings = []

        # Truncate very long texts to avoid memory issues
        max_length = 512  # Max tokens for the model
        truncated_texts = []
        for text in texts:
            # Split by newlines and truncate
            lines = text.split('\n')
            truncated = '\n'.join(lines[:50])  # Keep first 50 lines
            if len(truncated) > 5000:  # Also limit by character count
                truncated = truncated[:5000]
            truncated_texts.append(truncated)

        # Process in batches for efficiency
        for i in range(0, len(truncated_texts), batch_size):
            try:
                batch = truncated_texts[i:i + batch_size]
                batch_embeddings = self.embedding_model.encode(
                    batch,
                    show_progress_bar=False,  # Disable progress bar to avoid pipe issues
                    convert_to_numpy=True,
                    batch_size=batch_size
                )
                embeddings.extend(batch_embeddings.tolist())
                logger.info(f"Processed batch {i//batch_size + 1}/{(len(truncated_texts)-1)//batch_size + 1}")
            except Exception as e:
                logger.error(f"Error processing batch {i//batch_size + 1}: {e}")
                # Process individually as fallback
                for text in batch:
                    try:
                        emb = self.embedding_model.encode(
                            text,
                            show_progress_bar=False,
                            convert_to_numpy=True
                        )
                        embeddings.append(emb.tolist())
                    except Exception as e2:
                        logger.error(f"Error processing individual text: {e2}")
                        # Use zero vector as last resort
                        embeddings.append([0.0] * 384)

        return embeddings

    def add_documents(
        self,
        documents: List[Dict[str, Any]],
        batch_size: int = 100
    ) -> None:
        """
        Add documents to the vector store.

        Args:
            documents: List of documents with 'text' and 'metadata' keys
            batch_size: Number of documents to add at once
        """
        if not self.enabled:
            logger.warning("Semantic search disabled - cannot add documents")
            return
        logger.info(f"Adding {len(documents)} documents to vector store")

        # Extract texts and metadata
        texts = [doc['text'] for doc in documents]

        # Sanitize metadata - convert all values to strings for ChromaDB compatibility
        metadatas = []
        for doc in documents:
            sanitized_meta = {}
            for key, value in doc['metadata'].items():
                # Convert to string, handling None values
                sanitized_meta[key] = str(value) if value is not None else ""
            metadatas.append(sanitized_meta)

        # Generate embeddings
        embeddings = self.generate_embeddings(texts)

        # Create unique IDs
        ids = [f"doc_{i}" for i in range(len(documents))]

        # Add to collection in batches
        for i in range(0, len(documents), batch_size):
            end_idx = min(i + batch_size, len(documents))

            self.collection.add(
                embeddings=embeddings[i:end_idx],
                documents=texts[i:end_idx],
                metadatas=metadatas[i:end_idx],
                ids=ids[i:end_idx]
            )
            logger.info(f"Added batch {i//batch_size + 1}: {end_idx - i} documents")

        logger.info(f"Successfully added all {len(documents)} documents")

    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search for similar documents.

        Args:
            query: Search query text
            n_results: Number of results to return
            filter_metadata: Optional metadata filter

        Returns:
            Dictionary containing results
        """
        if not self.enabled:
            return {"results": [], "query": query}
        logger.info(f"Searching for: {query}")

        # Generate query embedding
        query_embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True
        ).tolist()

        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )

        logger.info(f"Found {len(results['ids'][0])} results")

        return {
            'ids': results['ids'][0],
            'documents': results['documents'][0],
            'metadatas': results['metadatas'][0],
            'distances': results['distances'][0]
        }

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.

        Returns:
            Dictionary of statistics
        """
        if not self.enabled:
            return {"count": 0, "enabled": False}
        count = self.collection.count()

        return {
            'collection_name': self.collection_name,
            'document_count': count,
            'persist_directory': self.persist_directory,
            'embedding_model': self.embedding_model_name
        }

    def delete_collection(self) -> None:
        """Delete the current collection."""
        if not self.enabled:
            return
        self.client.delete_collection(name=self.collection_name)
        logger.info(f"Deleted collection: {self.collection_name}")

    def reset_collection(self) -> None:
        """Reset the collection by deleting and recreating it."""
        if not self.enabled:
            return
        try:
            self.delete_collection()
        except:
            pass
        self.collection = self.client.create_collection(name=self.collection_name)
        logger.info(f"Reset collection: {self.collection_name}")


class VectorStoreManager:
    """Higher-level manager for vector store operations."""

    def __init__(self, vector_store: VectorStore):
        """
        Initialize the manager.

        Args:
            vector_store: VectorStore instance
        """
        self.vector_store = vector_store

    def index_excel_data(self, documents: List[Dict[str, Any]]) -> None:
        """
        Index Excel data documents into the vector store.

        Args:
            documents: List of documents from ExcelDataLoader
        """
        if not self.vector_store.enabled:
            logger.info("Vector store disabled - skipping indexing")
            return

        logger.info("Starting indexing process")

        # Reset collection for fresh start
        self.vector_store.reset_collection()

        # Add documents
        self.vector_store.add_documents(documents)

        # Print statistics
        stats = self.vector_store.get_collection_stats()
        logger.info(f"Indexing complete: {stats}")

    def search_with_context(
        self,
        query: str,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """
        Search and return results with enhanced context.

        Args:
            query: Search query
            n_results: Number of results

        Returns:
            Enhanced results with context
        """
        if not self.vector_store.enabled:
            return {
                'query': query,
                'num_results': 0,
                'results': []
            }

        results = self.vector_store.search(query, n_results)

        # Enhance results with additional context
        enhanced_results = {
            'query': query,
            'num_results': len(results['ids']),
            'results': []
        }

        for i in range(len(results['ids'])):
            enhanced_results['results'].append({
                'id': results['ids'][i],
                'document': results['documents'][i],
                'metadata': results['metadatas'][i],
                'relevance_score': 1 - results['distances'][i],  # Convert distance to similarity
                'source': f"{results['metadatas'][i].get('file', 'unknown')}:{results['metadatas'][i].get('sheet', 'unknown')}"
            })

        return enhanced_results


if __name__ == "__main__":
    # Example usage
    from data_loader import ExcelDataLoader

    # Load data
    print("="*60)
    print("LOADING DATA")
    print("="*60)
    loader = ExcelDataLoader([
        "actuarial_life_data_file1.xlsx",
        "actuarial_life_data_file2.xlsx"
    ])

    # Prepare documents
    documents = loader.prepare_documents_for_embedding(max_rows_per_chunk=50)
    print(f"Prepared {len(documents)} documents")

    # Initialize vector store
    print("\n" + "="*60)
    print("INITIALIZING VECTOR STORE")
    print("="*60)
    vector_store = VectorStore()

    # Index documents
    print("\n" + "="*60)
    print("INDEXING DOCUMENTS")
    print("="*60)
    manager = VectorStoreManager(vector_store)
    manager.index_excel_data(documents)

    # Test search
    print("\n" + "="*60)
    print("TESTING SEARCH")
    print("="*60)
    test_query = "What are the policy details?"
    results = manager.search_with_context(test_query, n_results=3)

    import json
    print(json.dumps(results, indent=2, default=str))
