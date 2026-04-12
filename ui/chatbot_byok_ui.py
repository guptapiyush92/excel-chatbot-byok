"""
Multi-Provider BYOK (Bring Your Own Key) Excel Chatbot
Supports Anthropic Claude, Google Gemini, and OpenAI GPT
Users provide their own API keys
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from src.data_loader import ExcelDataLoader
from src.vector_store import VectorStore, VectorStoreManager
from src.llm_provider import MultiProviderLLM, create_llm_client
import logging
import pandas as pd
import os
import tempfile
import shutil
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Excel Chatbot - Multi-Provider BYOK",
    page_icon="🤖",
    layout="wide"
)


def save_uploaded_file(uploaded_file, temp_dir):
    """Save uploaded file to temporary directory."""
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def process_files_with_llm(file_paths, llm_client, progress_bar=None, status_text=None):
    """Process uploaded Excel files and create chatbot with specified LLM."""
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

        # Initialize vector store
        collection_name = f"excel_data_{int(time.time())}"
        vector_store = VectorStore(collection_name=collection_name)

        if status_text:
            status_text.text("📥 Indexing documents...")
        if progress_bar:
            progress_bar.progress(0.7)

        # Index documents
        manager = VectorStoreManager(vector_store)
        manager.index_excel_data(documents)

        if progress_bar:
            progress_bar.progress(1.0)

        # Calculate statistics
        total_rows = sum(len(df) for sheets in dataframes.values() for df in sheets.values())
        total_sheets = sum(len(sheets) for sheets in dataframes.values())

        return {
            'success': True,
            'llm_client': llm_client,
            'vector_store': vector_store,
            'dataframes': dataframes,
            'analysis': analysis,
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


def query_with_llm(llm_client, vector_store, dataframes, query):
    """Query using the configured LLM."""
    try:
        # Search vector store for relevant context
        results = vector_store.search(query, n_results=5)

        # Build context from results
        context_parts = []
        for doc, metadata in zip(results['documents'], results['metadatas']):
            context_parts.append(f"From {metadata['file']} - {metadata['sheet']}:\n{doc}\n")

        context = "\n".join(context_parts)

        # Build schema info
        schema_info = []
        for file_name, sheets in dataframes.items():
            schema_info.append(f"File: {file_name}")
            for sheet_name, df in sheets.items():
                schema_info.append(f"  Sheet: {sheet_name} ({len(df)} rows)")
                schema_info.append(f"  Columns: {', '.join(df.columns.tolist())}")

        schema_text = "\n".join(schema_info)

        # Create messages for LLM
        messages = [
            {
                "role": "system",
                "content": f"""You are an expert data analyst helping users understand their Excel data.

Available Data:
{schema_text}

Use the provided context to answer questions accurately. If you're not sure, say so."""
            },
            {
                "role": "user",
                "content": f"""Context from data:
{context}

Question: {query}

Please provide a clear, helpful answer based on the data."""
            }
        ]

        # Generate response
        response = llm_client.generate(messages, max_tokens=2048, temperature=0.7)

        return {
            'success': True,
            'answer': response,
            'context': context
        }

    except Exception as e:
        logger.error(f"Error querying LLM: {e}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }


def main():
    """Main Streamlit app."""

    # Header
    st.title("🤖 Excel Chatbot - Multi-Provider BYOK")
    st.markdown("**Bring Your Own API Key** - Use Anthropic Claude, Google Gemini, or OpenAI GPT")

    # Sidebar - API Configuration
    with st.sidebar:
        st.header("🔑 API Configuration")

        # Provider selection
        providers = MultiProviderLLM.get_available_providers()
        provider_names = {
            "anthropic": "🔷 Anthropic Claude",
            "gemini": "🟢 Google Gemini",
            "openai": "🟦 OpenAI GPT"
        }

        selected_provider = st.selectbox(
            "Select AI Provider",
            options=list(providers.keys()),
            format_func=lambda x: provider_names[x]
        )

        provider_info = providers[selected_provider]

        # API Key input
        st.markdown(f"**Get API Key:** [{provider_info['name']}]({provider_info['api_key_url']})")
        api_key = st.text_input(
            "API Key",
            type="password",
            help=f"Your {provider_info['name']} API key"
        )

        # Model selection
        selected_model = st.selectbox(
            "Model",
            options=provider_info['models'],
            index=0,
            help="Choose the model to use"
        )

        # Base URL (optional, for corporate proxies)
        if provider_info['supports_base_url']:
            use_custom_url = st.checkbox("Use Custom Base URL", value=False)
            if use_custom_url:
                base_url = st.text_input(
                    "Base URL",
                    placeholder="https://your-proxy.com/v1",
                    help="For corporate proxies or custom endpoints"
                )
            else:
                base_url = None
        else:
            base_url = None

        # Initialize LLM button
        if api_key:
            if st.button("🚀 Initialize AI", use_container_width=True, type="primary"):
                try:
                    with st.spinner("Initializing AI..."):
                        llm_client = create_llm_client(
                            provider=selected_provider,
                            api_key=api_key,
                            model=selected_model,
                            base_url=base_url
                        )
                        st.session_state.llm_client = llm_client
                        st.session_state.provider = selected_provider
                        st.session_state.model = selected_model
                        st.success(f"✅ {provider_info['name']} initialized!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.info("👆 Enter your API key above")

        st.divider()

        # File Upload Section
        st.header("📤 Upload Files")

        uploaded_files = st.file_uploader(
            "Choose Excel files",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            help="Upload one or more Excel files"
        )

        if uploaded_files and 'llm_client' in st.session_state:
            st.write(f"**Files selected:** {len(uploaded_files)}")
            for file in uploaded_files:
                file_size_mb = file.size / (1024 * 1024)
                st.write(f"- {file.name} ({file_size_mb:.2f} MB)")

            if st.button("🚀 Process Files", use_container_width=True, type="primary"):
                temp_dir = tempfile.mkdtemp()

                try:
                    # Save uploaded files
                    file_paths = []
                    for uploaded_file in uploaded_files:
                        file_path = save_uploaded_file(uploaded_file, temp_dir)
                        file_paths.append(file_path)

                    # Process files
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    result = process_files_with_llm(
                        file_paths,
                        st.session_state.llm_client,
                        progress_bar,
                        status_text
                    )

                    if result['success']:
                        st.session_state.vector_store = result['vector_store']
                        st.session_state.dataframes = result['dataframes']
                        st.session_state.stats = result['stats']
                        st.session_state.temp_dir = temp_dir
                        st.session_state.messages = []

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

        elif uploaded_files and 'llm_client' not in st.session_state:
            st.warning("⚠️ Initialize AI first")

        # Show stats if data loaded
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
                if 'temp_dir' in st.session_state:
                    shutil.rmtree(st.session_state.temp_dir, ignore_errors=True)

                for key in ['llm_client', 'vector_store', 'dataframes', 'stats', 'temp_dir', 'messages', 'provider', 'model']:
                    if key in st.session_state:
                        del st.session_state[key]

                st.success("Data cleared!")
                st.rerun()

        st.divider()
        st.header("ℹ️ About")
        st.markdown("""
        **Multi-Provider Support:**
        - 🔷 Anthropic Claude
        - 🟢 Google Gemini
        - 🟦 OpenAI GPT

        **Features:**
        - Bring your own API key
        - Upload multiple Excel files
        - Natural language queries
        - Semantic search
        """)

    # Main content area
    if 'llm_client' not in st.session_state:
        # Welcome screen
        st.info("👈 Configure your AI provider in the sidebar to get started")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🔷 Anthropic Claude")
            st.markdown("""
            - Claude Sonnet 4
            - Claude Opus 4
            - Fast and accurate
            - Great for analysis
            """)

        with col2:
            st.subheader("🟢 Google Gemini")
            st.markdown("""
            - Gemini 2.0 Flash
            - Gemini 1.5 Pro
            - Multimodal capable
            - Cost-effective
            """)

        with col3:
            st.subheader("🟦 OpenAI GPT")
            st.markdown("""
            - GPT-4o
            - GPT-4 Turbo
            - Industry standard
            - Reliable
            """)

    elif 'vector_store' not in st.session_state:
        # Data upload prompt
        provider_name = MultiProviderLLM.get_available_providers()[st.session_state.provider]['name']
        st.success(f"✅ {provider_name} ({st.session_state.model}) is ready!")
        st.info("👈 Upload Excel files from the sidebar to begin")

    else:
        # Chat interface
        provider_name = MultiProviderLLM.get_available_providers()[st.session_state.provider]['name']
        st.success(f"✅ Using {provider_name} ({st.session_state.model})")

        # Initialize message history
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
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
                with st.spinner("Thinking..."):
                    result = query_with_llm(
                        st.session_state.llm_client,
                        st.session_state.vector_store,
                        st.session_state.dataframes,
                        prompt
                    )

                    if result['success']:
                        st.markdown(result['answer'])
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": result['answer']
                        })
                    else:
                        error_msg = f"Error: {result['error']}"
                        st.error(error_msg)

        # Footer
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Files", st.session_state.stats['total_files'])
        with col2:
            st.metric("Sheets", st.session_state.stats['total_sheets'])
        with col3:
            st.metric("Rows", f"{st.session_state.stats['total_rows']:,}")


if __name__ == "__main__":
    main()
