import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

"""
Streamlit web interface for the Excel Chatbot.
"""

import streamlit as st
from src.chatbot import ChatbotManager
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Excel Chatbot",
    page_icon="📊",
    layout="wide"
)


@st.cache_resource
def initialize_chatbot():
    """Initialize chatbot (cached to avoid reloading)."""
    file1 = Path("actuarial_life_data_file1.xlsx")
    file2 = Path("actuarial_life_data_file2.xlsx")

    if not file1.exists() or not file2.exists():
        st.error("Excel files not found!")
        return None

    with st.spinner("Initializing chatbot... This may take a moment."):
        chatbot = ChatbotManager.initialize_from_excel_files(
            file_paths=[str(file1), str(file2)],
            reset_index=False
        )

    return chatbot


def main():
    """Main Streamlit app."""

    # Header
    st.title("📊 Excel Chatbot - Actuarial Data Assistant")
    st.markdown("Ask questions about your actuarial life insurance data in natural language!")

    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This chatbot helps you query and analyze large Excel datasets using natural language.

        **Features:**
        - Semantic search across 100k+ rows
        - Natural language queries
        - Context-aware responses
        - Powered by Claude AI
        """)

        st.divider()

        st.header("🎯 Example Queries")
        st.markdown("""
        - What data is available?
        - What are the average premium amounts?
        - Show policies with high surrender values
        - Compare mortality rates by gender
        - What's the relationship between age and premium?
        """)

        st.divider()

        if st.button("🗑️ Clear History", use_container_width=True):
            if 'chatbot' in st.session_state and st.session_state.chatbot:
                st.session_state.chatbot.clear_history()
                st.session_state.messages = []
                st.success("History cleared!")
                st.rerun()

        if st.button("📋 Show Data Summary", use_container_width=True):
            if 'chatbot' in st.session_state and st.session_state.chatbot:
                summary = st.session_state.chatbot.get_data_summary()
                st.markdown(summary)

    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = initialize_chatbot()

    if st.session_state.chatbot is None:
        st.error("Failed to initialize chatbot. Please check that the Excel files exist.")
        return

    # Initialize message history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your data..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.chatbot.query(prompt)
                    response = result['answer']

                    st.markdown(response)

                    # Add assistant response to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })

                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    logger.error(f"Error processing query: {str(e)}", exc_info=True)

    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.8em;'>
        Powered by Claude AI and ChromaDB | Built for large-scale Excel data analysis
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
