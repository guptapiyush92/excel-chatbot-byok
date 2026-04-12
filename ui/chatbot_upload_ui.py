"""
Enhanced Hybrid Streamlit interface with file upload capability.
Users can upload Excel files, which are then processed and vectorized on-the-fly.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from src.hybrid_engine import HybridQueryEngine
from src.data_loader import ExcelDataLoader
from src.vector_store import VectorStore, VectorStoreManager
import logging
import pandas as pd
import os
import tempfile
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Hybrid Excel Chatbot - Upload Files",
    page_icon="📊",
    layout="wide"
)


def save_uploaded_file(uploaded_file, temp_dir):
    """Save uploaded file to temporary directory."""
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def process_files(file_paths, progress_bar=None, status_text=None):
    """Process uploaded Excel files and create hybrid engine."""
    try:
        # Update status
        if status_text:
            status_text.text("📂 Loading Excel files...")
        if progress_bar:
            progress_bar.progress(0.2)

        # Load data
        loader = ExcelDataLoader(file_paths)

        if status_text:
            status_text.text("🔍 Analyzing structure...")
        if progress_bar:
            progress_bar.progress(0.3)

        # Analyze structure
        analysis = loader.analyze_structure()

        if status_text:
            status_text.text("📊 Loading data into memory...")
        if progress_bar:
            progress_bar.progress(0.4)

        # Load all data
        dataframes = loader.load_all_data()

        # Detect relationships
        relationships = loader.detect_relationships()

        if status_text:
            status_text.text("🧮 Preparing documents for vectorization...")
        if progress_bar:
            progress_bar.progress(0.5)

        # Prepare documents for embedding
        documents = loader.prepare_documents_for_embedding(max_rows_per_chunk=25)

        if status_text:
            status_text.text("🔤 Creating vector embeddings...")
        if progress_bar:
            progress_bar.progress(0.6)

        # Initialize vector store with unique collection name
        import time
        collection_name = f"excel_data_{int(time.time())}"
        vector_store = VectorStore(collection_name=collection_name)

        if status_text:
            status_text.text("📥 Indexing documents...")
        if progress_bar:
            progress_bar.progress(0.7)

        # Index documents
        manager = VectorStoreManager(vector_store)
        manager.index_excel_data(documents)

        if status_text:
            status_text.text("🤖 Initializing hybrid engine...")
        if progress_bar:
            progress_bar.progress(0.9)

        # Create hybrid engine
        engine = HybridQueryEngine(dataframes, vector_store)

        if progress_bar:
            progress_bar.progress(1.0)

        # Calculate statistics
        total_rows = sum(len(df) for sheets in dataframes.values() for df in sheets.values())
        total_sheets = sum(len(sheets) for sheets in dataframes.values())

        return {
            'success': True,
            'engine': engine,
            'dataframes': dataframes,
            'analysis': analysis,
            'relationships': relationships,
            'stats': {
                'total_files': len(file_paths),
                'total_sheets': total_sheets,
                'total_rows': total_rows,
                'total_documents': len(documents)
            }
        }

    except Exception as e:
        logger.error(f"Error processing files: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def format_result(result: dict) -> None:
    """Format and display query result."""
    query_type = result.get('query_type', 'unknown')

    # Show classification
    classification = result.get('classification', {})
    if classification:
        with st.expander("🔍 Query Analysis", expanded=False):
            st.write(f"**Type:** {classification.get('type', 'unknown').upper()}")
            st.write(f"**Reasoning:** {classification.get('reasoning', 'N/A')}")

    if not result.get('success', False):
        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        return

    # Display results based on type
    if query_type == 'structured':
        st.success("✅ Structured Query Result")

        # Show explanation
        explanation = result.get('explanation', '')
        if explanation:
            st.markdown(explanation)

        # Show data
        data = result.get('data')
        if data is not None:
            st.subheader("📊 Data")

            if isinstance(data, pd.DataFrame):
                if len(data) > 0:
                    st.dataframe(data, use_container_width=True)

                    # Download button
                    csv = data.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv,
                        file_name="query_result.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No matching rows found")

            elif isinstance(data, pd.Series):
                st.dataframe(data.to_frame(), use_container_width=True)

            else:
                st.code(str(data))

        # Show generated code
        code = result.get('query_code', '')
        if code:
            with st.expander("🔧 Generated Code", expanded=False):
                st.code(code, language='python')

    elif query_type == 'rag':
        st.success("✅ Semantic Analysis Result")

        answer = result.get('answer', '')
        if answer:
            st.markdown(answer)

        # Show context sources
        context = result.get('context', '')
        if context:
            with st.expander("📚 Source Context", expanded=False):
                st.text(context)

    elif query_type == 'hybrid':
        st.success("✅ Hybrid Query Result")

        # Show structured result
        structured = result.get('structured', {})
        if structured.get('success'):
            st.subheader("📊 Data Result")
            data = structured.get('data')
            if isinstance(data, pd.DataFrame):
                st.dataframe(data, use_container_width=True)

        # Show RAG analysis
        rag = result.get('rag', {})
        if rag.get('success'):
            st.subheader("💡 Analysis")
            st.markdown(rag.get('answer', ''))


def main():
    """Main Streamlit app."""

    # Header
    st.title("📊 Hybrid Excel Chatbot with File Upload")
    st.markdown("**Upload your Excel files and start querying with natural language**")

    # Sidebar
    with st.sidebar:
        st.header("📤 Upload Files")

        # File uploader
        uploaded_files = st.file_uploader(
            "Choose Excel files",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            help="Upload one or more Excel files (max 200MB each)"
        )

        # Process button
        if uploaded_files:
            st.write(f"**Files selected:** {len(uploaded_files)}")
            for file in uploaded_files:
                file_size_mb = file.size / (1024 * 1024)
                st.write(f"- {file.name} ({file_size_mb:.2f} MB)")

            if st.button("🚀 Process Files", use_container_width=True, type="primary"):
                # Create temporary directory
                temp_dir = tempfile.mkdtemp()

                try:
                    # Save uploaded files
                    file_paths = []
                    for uploaded_file in uploaded_files:
                        file_path = save_uploaded_file(uploaded_file, temp_dir)
                        file_paths.append(file_path)

                    # Process files with progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    result = process_files(file_paths, progress_bar, status_text)

                    if result['success']:
                        # Store in session state
                        st.session_state.engine = result['engine']
                        st.session_state.dataframes = result['dataframes']
                        st.session_state.analysis = result['analysis']
                        st.session_state.relationships = result['relationships']
                        st.session_state.stats = result['stats']
                        st.session_state.temp_dir = temp_dir
                        st.session_state.file_paths = file_paths
                        st.session_state.messages = []  # Clear chat history

                        status_text.empty()
                        progress_bar.empty()
                        st.success("✅ Files processed successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result['error']}")
                        shutil.rmtree(temp_dir, ignore_errors=True)

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    shutil.rmtree(temp_dir, ignore_errors=True)

        else:
            st.info("📁 Upload Excel files to get started")

            # Option to use default files
            st.divider()
            st.subheader("Or use default files")

            if st.button("📂 Load Default Files", use_container_width=True):
                # Check if default files exist
                default_files = [
                    "actuarial_life_data_file1.xlsx",
                    "actuarial_life_data_file2.xlsx"
                ]

                if all(Path(f).exists() for f in default_files):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    result = process_files(default_files, progress_bar, status_text)

                    if result['success']:
                        st.session_state.engine = result['engine']
                        st.session_state.dataframes = result['dataframes']
                        st.session_state.analysis = result['analysis']
                        st.session_state.relationships = result['relationships']
                        st.session_state.stats = result['stats']
                        st.session_state.messages = []

                        status_text.empty()
                        progress_bar.empty()
                        st.success("✅ Default files loaded!")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result['error']}")
                else:
                    st.error("Default files not found in current directory")

        # Show stats if files are loaded
        if 'stats' in st.session_state:
            st.divider()
            st.subheader("📊 Data Summary")
            stats = st.session_state.stats
            st.metric("Files", stats['total_files'])
            st.metric("Sheets", stats['total_sheets'])
            st.metric("Total Rows", f"{stats['total_rows']:,}")
            st.metric("Indexed Docs", stats['total_documents'])

            # Clear data button
            if st.button("🗑️ Clear Data", use_container_width=True):
                # Clean up temp directory if exists
                if 'temp_dir' in st.session_state:
                    shutil.rmtree(st.session_state.temp_dir, ignore_errors=True)

                # Clear session state
                for key in ['engine', 'dataframes', 'analysis', 'relationships', 'stats', 'temp_dir', 'file_paths', 'messages']:
                    if key in st.session_state:
                        del st.session_state[key]

                st.success("Data cleared!")
                st.rerun()

        st.divider()

        st.header("ℹ️ About")
        st.markdown("""
        **Features:**
        - 📤 Upload multiple Excel files
        - 🎯 Structured queries for exact data
        - 🧠 Semantic search for insights
        - 🤖 Automatic query routing
        - 📊 Handles files from KBs to MBs
        """)

        st.divider()

        st.header("💡 Example Queries")
        st.markdown("""
        **Structured:**
        - `Details of policy P00225`
        - `All policies in class Micro`
        - `Average premium by segment`

        **Semantic:**
        - `What data is available?`
        - `Explain persistency rates`
        - `Summarize the data`
        """)

        if 'messages' in st.session_state and len(st.session_state.messages) > 0:
            st.divider()
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    # Main content area
    if 'engine' not in st.session_state:
        # Welcome screen
        st.info("👆 Upload Excel files from the sidebar to get started")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🎯 Structured Queries")
            st.markdown("""
            Get exact, precise data:
            - Specific row lookups by ID
            - Filtered tables
            - Aggregations and calculations
            - Joins across sheets

            **Example:**
            > "Give me all details of policy P00225"

            Returns actual data in table format ✅
            """)

        with col2:
            st.subheader("🧠 Semantic Queries")
            st.markdown("""
            Get insights and understanding:
            - General overviews
            - Conceptual explanations
            - Pattern discovery
            - Qualitative analysis

            **Example:**
            > "What data is available?"

            Returns natural language explanation ✅
            """)

        st.markdown("---")

        st.subheader("📋 Supported File Formats")
        st.markdown("""
        - **.xlsx** - Excel 2007+ files
        - **.xls** - Legacy Excel files
        - **Size:** From a few KBs to several MBs
        - **Rows:** Optimized for 100k+ rows per file
        """)

    else:
        # Chat interface
        st.success("✅ Files loaded and ready!")

        # Initialize message history
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "assistant" and "result" in message:
                    format_result(message["result"])
                else:
                    st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask about your data..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Processing..."):
                    try:
                        result = st.session_state.engine.query(prompt)

                        # Display result
                        format_result(result)

                        # Add to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "result": result
                        })

                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.error(error_msg)
                        logger.error(f"Error processing query: {str(e)}", exc_info=True)

        # Footer
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Files", st.session_state.stats['total_files'])
        with col2:
            st.metric("Sheets", st.session_state.stats['total_sheets'])
        with col3:
            st.metric("Total Rows", f"{st.session_state.stats['total_rows']:,}")


if __name__ == "__main__":
    main()
