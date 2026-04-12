import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

"""
Hybrid Streamlit interface that combines structured queries with RAG.
Automatically routes queries to the appropriate engine.
"""

import streamlit as st
from src.hybrid_engine import HybridQueryEngine
from src.data_loader import ExcelDataLoader
from src.vector_store import VectorStore, VectorStoreManager
from pathlib import Path
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Hybrid Excel Chatbot",
    page_icon="📊",
    layout="wide"
)


@st.cache_resource
def initialize_system():
    """Initialize both structured and RAG systems."""
    file1 = Path("actuarial_life_data_file1.xlsx")
    file2 = Path("actuarial_life_data_file2.xlsx")

    if not file1.exists() or not file2.exists():
        st.error("Excel files not found!")
        return None, None

    with st.spinner("Loading Excel data..."):
        # Load data for structured queries
        loader = ExcelDataLoader([str(file1), str(file2)])
        dataframes = loader.load_all_data()

        # Initialize vector store for RAG (if needed)
        try:
            vector_store = VectorStore()
            if vector_store.collection.count() == 0:
                with st.spinner("Building search index (first time only)..."):
                    documents = loader.prepare_documents_for_embedding(max_rows_per_chunk=50)
                    manager = VectorStoreManager(vector_store)
                    manager.index_excel_data(documents)
        except Exception as e:
            logger.warning(f"Vector store initialization failed: {e}")
            vector_store = None

        # Create hybrid engine
        engine = HybridQueryEngine(dataframes, vector_store)

    return engine, dataframes


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
    st.title("📊 Hybrid Excel Chatbot")
    st.markdown("**Intelligent system that combines precise queries with semantic understanding**")

    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This chatbot intelligently routes your queries:

        **🎯 Structured Queries:**
        - Specific row lookups by ID
        - Exact filters and aggregations
        - Tabular data output
        - Precise calculations

        **🧠 Semantic Queries:**
        - General understanding
        - Conceptual questions
        - Pattern discovery
        - Qualitative insights
        """)

        st.divider()

        st.header("💡 Example Queries")

        st.subheader("Structured:")
        st.markdown("""
        - `Give me all details of policy ID P00225`
        - `All policies in class Micro in table format`
        - `Average premium by segment`
        - `Claims with fraud flags`
        - `Policies with reserves > 1000000`
        """)

        st.subheader("Semantic:")
        st.markdown("""
        - `What data is available?`
        - `Explain persistency rates`
        - `What patterns exist in claims?`
        - `Summarize the mortality data`
        """)

        st.divider()

        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.messages = []
            st.success("History cleared!")
            st.rerun()

        if st.button("📊 Show Data Summary", use_container_width=True):
            if 'dataframes' in st.session_state and st.session_state.dataframes:
                with st.expander("Data Summary", expanded=True):
                    for file_name, sheets in st.session_state.dataframes.items():
                        st.write(f"**{file_name}**")
                        for sheet_name, df in sheets.items():
                            st.write(f"- {sheet_name}: {len(df)} rows, {len(df.columns)} columns")

    # Initialize system
    if 'engine' not in st.session_state:
        engine, dataframes = initialize_system()
        if engine is None:
            st.error("Failed to initialize chatbot. Please check that the Excel files exist.")
            return
        st.session_state.engine = engine
        st.session_state.dataframes = dataframes
        st.success("✅ Chatbot ready!")

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
        st.metric("Total Rows", "1,010")
    with col2:
        st.metric("Sheets", "4")
    with col3:
        st.metric("Files", "2")

    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.8em; margin-top: 20px;'>
        Powered by Claude AI | Hybrid Query Engine (Structured + RAG)
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
