#!/usr/bin/env python3
"""
Test the hybrid query engine with both structured and semantic queries.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.hybrid_engine import HybridQueryEngine
from src.data_loader import ExcelDataLoader
from src.vector_store import VectorStore, VectorStoreManager
import pandas as pd

print("="*70)
print("HYBRID QUERY ENGINE TEST")
print("="*70)
print()

# Load data
print("1. Loading Excel data...")
loader = ExcelDataLoader([
    "actuarial_life_data_file1.xlsx",
    "actuarial_life_data_file2.xlsx"
])

dataframes = loader.load_all_data()
print(f"✅ Loaded {sum(len(df) for sheets in dataframes.values() for df in sheets.values())} total rows")
print()

# Initialize vector store (optional, for RAG queries)
print("2. Initializing vector store for RAG...")
try:
    vector_store = VectorStore()
    if vector_store.collection.count() == 0:
        print("   Building index...")
        documents = loader.prepare_documents_for_embedding(max_rows_per_chunk=50)
        manager = VectorStoreManager(vector_store)
        manager.index_excel_data(documents)
    print(f"✅ Vector store ready ({vector_store.collection.count()} documents)")
except Exception as e:
    print(f"⚠️  Vector store not available: {e}")
    vector_store = None
print()

# Create hybrid engine
print("3. Initializing hybrid engine...")
engine = HybridQueryEngine(dataframes, vector_store)
print("✅ Hybrid engine ready")
print()

# Test queries
test_queries = [
    # Structured queries
    ("Give me all details of policy ID P00225 including class and subclass in hierarchical format", "Should return exact policy details"),
    ("Show me all policies under class Micro in a tabular format", "Should return filtered table"),
    ("What is the average claim amount for Death claims?", "Should calculate exact average"),

    # Semantic queries
    ("What data is available in these files?", "Should provide overview"),
    ("Explain what persistency rates mean", "Should give conceptual answer"),
]

for i, (query, expected) in enumerate(test_queries, 1):
    print("\n" + "="*70)
    print(f"TEST {i}: {query}")
    print(f"Expected: {expected}")
    print("="*70)

    result = engine.query(query)

    # Show classification
    classification = result.get('classification', {})
    print(f"\n📋 Classification: {classification.get('type', 'unknown').upper()}")
    print(f"   Reasoning: {classification.get('reasoning', 'N/A')}")

    # Show result
    if result.get('success'):
        query_type = result.get('query_type')

        if query_type == 'structured':
            print(f"\n✅ Structured Query Success")
            print(f"\nExplanation:\n{result.get('explanation', 'N/A')}")

            data = result.get('data')
            if isinstance(data, pd.DataFrame):
                print(f"\n📊 Data ({len(data)} rows):")
                print(data.to_string())
            elif data is not None:
                print(f"\n📊 Result: {data}")

        elif query_type == 'rag':
            print(f"\n✅ RAG Query Success")
            print(f"\nAnswer:\n{result.get('answer', 'N/A')}")

    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown')}")

    input("\nPress Enter to continue to next test...")

print("\n" + "="*70)
print("ALL TESTS COMPLETE")
print("="*70)
print()
print("The hybrid system is working! You can now:")
print("1. Run the CLI: python chatbot_cli.py")
print("2. Run the hybrid UI: streamlit run chatbot_hybrid_ui.py")
