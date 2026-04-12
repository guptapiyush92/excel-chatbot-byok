#!/bin/bash

# Excel Chatbot - Complete Restructure (Automated)
# Runs restructure + import updates + verification

echo "=========================================="
echo "Excel Chatbot - Complete Restructure"
echo "=========================================="
echo ""
echo "This will:"
echo "  1. Reorganize project structure"
echo "  2. Update all import statements"
echo "  3. Verify the setup"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Make scripts executable
chmod +x restructure_project.sh
chmod +x update_imports.sh

# Run restructure
echo ""
echo "==== Step 1: Restructuring ===="
bash restructure_project.sh

# Run import updates
echo ""
echo "==== Step 2: Updating Imports ===="
bash update_imports.sh

# Verification
echo ""
echo "==== Step 3: Verification ===="
echo ""

if [ -d "src" ] && [ -d "ui" ] && [ -d "tests" ] && [ -d "data" ] && [ -d "docs" ]; then
    echo "✓ Directory structure created"
else
    echo "✗ Some directories missing"
    exit 1
fi

if [ -f "src/data_loader.py" ] && [ -f "src/vector_store.py" ]; then
    echo "✓ Source files in place"
else
    echo "✗ Source files missing"
    exit 1
fi

if [ -f "ui/chatbot_upload_ui.py" ]; then
    echo "✓ UI files in place"
else
    echo "✗ UI files missing"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Restructure Complete & Verified!"
echo "=========================================="
echo ""
echo "New Project Structure:"
echo ""
echo "excel_chatbot/"
echo "├── src/              - Core code"
echo "├── ui/               - User interfaces"
echo "├── scripts/          - Utilities"
echo "├── tests/            - Tests"
echo "├── data/             - Data files"
echo "└── docs/             - Documentation"
echo ""
echo "To start the app:"
echo "  bash scripts/start_upload.sh"
echo ""
echo "Or directly:"
echo "  streamlit run ui/chatbot_upload_ui.py"
echo ""
