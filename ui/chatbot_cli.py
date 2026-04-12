import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

#!/usr/bin/env python3
"""
Command-line interface for the Excel Chatbot.
"""

import sys
from src.chatbot import ChatbotManager, ExcelChatbot
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_header():
    """Print welcome header."""
    print("\n" + "="*70)
    print(" "*15 + "EXCEL CHATBOT - Actuarial Data Assistant")
    print("="*70)
    print("\nAsk questions about your Excel data in natural language!")
    print("\nCommands:")
    print("  - Type your question and press Enter")
    print("  - Type 'quit' or 'exit' to exit")
    print("  - Type 'clear' to clear conversation history")
    print("  - Type 'summary' to see available data summary")
    print("="*70 + "\n")


def main():
    """Main CLI loop."""
    try:
        print_header()

        # Check if Excel files exist
        file1 = Path("actuarial_life_data_file1.xlsx")
        file2 = Path("actuarial_life_data_file2.xlsx")

        if not file1.exists() or not file2.exists():
            print("❌ Error: Excel files not found!")
            print(f"Expected files:")
            print(f"  - {file1}")
            print(f"  - {file2}")
            sys.exit(1)

        # Initialize chatbot
        print("🔄 Initializing chatbot (this may take a moment)...\n")

        chatbot = ChatbotManager.initialize_from_excel_files(
            file_paths=[str(file1), str(file2)],
            reset_index=False  # Set to True to rebuild index
        )

        print("✅ Chatbot ready!\n")

        # Main loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break

                elif user_input.lower() == 'clear':
                    chatbot.clear_history()
                    print("✅ Conversation history cleared.\n")
                    continue

                elif user_input.lower() == 'summary':
                    print("\n" + chatbot.get_data_summary() + "\n")
                    continue

                # Process query
                print("\n🤔 Thinking...\n")

                result = chatbot.query(user_input)

                print("Bot:", result['answer'])
                print()

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break

            except Exception as e:
                print(f"\n❌ Error processing query: {str(e)}\n")
                logger.error(f"Error: {str(e)}", exc_info=True)

    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
