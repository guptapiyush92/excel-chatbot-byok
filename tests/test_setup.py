#!/usr/bin/env python3
"""
Test script to verify the Excel Chatbot setup.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import sys
from pathlib import Path


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import pandas
        import openpyxl
        import chromadb
        from sentence_transformers import SentenceTransformer
        import anthropic
        import langchain
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_excel_files():
    """Test that Excel files exist and are readable."""
    print("\nTesting Excel files...")
    files = [
        "actuarial_life_data_file1.xlsx",
        "actuarial_life_data_file2.xlsx"
    ]

    all_exist = True
    for file in files:
        if Path(file).exists():
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} not found")
            all_exist = False

    return all_exist


def test_data_loader():
    """Test data loader functionality."""
    print("\nTesting data loader...")
    try:
        from data_loader import ExcelDataLoader

        loader = ExcelDataLoader([
            "actuarial_life_data_file1.xlsx",
            "actuarial_life_data_file2.xlsx"
        ])

        # Analyze structure
        analysis = loader.analyze_structure()
        print(f"✅ Data structure analyzed successfully")
        print(f"   - Files: {len(analysis)}")

        total_rows = sum(data['total_rows'] for data in analysis.values())
        print(f"   - Total rows: {total_rows}")

        # Detect relationships
        relationships = loader.detect_relationships()
        print(f"✅ Relationships detected: {len(relationships)}")

        return True
    except Exception as e:
        print(f"❌ Data loader test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_vector_store():
    """Test vector store initialization."""
    print("\nTesting vector store...")
    try:
        from vector_store import VectorStore

        # Initialize without adding data
        vector_store = VectorStore(
            collection_name="test_collection",
            persist_directory="./test_chroma_db"
        )

        print(f"✅ Vector store initialized successfully")
        print(f"   - Collection: {vector_store.collection_name}")
        print(f"   - Embedding model: {vector_store.embedding_model_name}")

        # Clean up
        vector_store.delete_collection()
        import shutil
        shutil.rmtree("./test_chroma_db", ignore_errors=True)

        return True
    except Exception as e:
        print(f"❌ Vector store test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_environment():
    """Test environment configuration."""
    print("\nTesting environment...")
    import os
    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key and len(api_key) > 10:
        print(f"✅ ANTHROPIC_API_KEY found (length: {len(api_key)})")
        return True
    else:
        print(f"⚠️  ANTHROPIC_API_KEY not found or invalid")
        print(f"   Please add your API key to .env file")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("Excel Chatbot - System Test")
    print("="*60)
    print()

    results = {
        "Imports": test_imports(),
        "Excel Files": test_excel_files(),
        "Data Loader": test_data_loader(),
        "Vector Store": test_vector_store(),
        "Environment": test_environment()
    }

    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)

    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20s} : {status}")
        if not passed:
            all_passed = False

    print("="*60)

    if all_passed:
        print("\n🎉 All tests passed! Your system is ready to use.")
        print("\nNext steps:")
        print("1. Run the CLI: python chatbot_cli.py")
        print("2. Run the web UI: streamlit run chatbot_ui.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
