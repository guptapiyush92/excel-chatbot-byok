#!/bin/bash

# Excel Chatbot - Import Statement Update Script
# Updates import statements after restructuring

set -e

echo "=========================================="
echo "Updating Import Statements"
echo "=========================================="
echo ""

# Update imports in UI files
echo "Updating ui/ files..."

for file in ui/*.py; do
    if [ -f "$file" ]; then
        # Update imports from current directory to src
        sed -i '' 's/^from data_loader import/from src.data_loader import/g' "$file"
        sed -i '' 's/^from vector_store import/from src.vector_store import/g' "$file"
        sed -i '' 's/^from chatbot import/from src.chatbot import/g' "$file"
        sed -i '' 's/^from hybrid_engine import/from src.hybrid_engine import/g' "$file"

        # Also handle 'import' statements
        sed -i '' 's/^import data_loader$/import src.data_loader as data_loader/g' "$file"
        sed -i '' 's/^import vector_store$/import src.vector_store as vector_store/g' "$file"
        sed -i '' 's/^import chatbot$/import src.chatbot as chatbot/g' "$file"
        sed -i '' 's/^import hybrid_engine$/import src.hybrid_engine as hybrid_engine/g' "$file"

        echo "  ✓ Updated $file"
    fi
done

# Update imports in test files
echo ""
echo "Updating tests/ files..."

for file in tests/*.py; do
    if [ -f "$file" ] && [ "$file" != "tests/__init__.py" ]; then
        sed -i '' 's/^from data_loader import/from src.data_loader import/g' "$file"
        sed -i '' 's/^from vector_store import/from src.vector_store import/g' "$file"
        sed -i '' 's/^from chatbot import/from src.chatbot import/g' "$file"
        sed -i '' 's/^from hybrid_engine import/from src.hybrid_engine import/g' "$file"

        echo "  ✓ Updated $file"
    fi
done

# Update imports in scripts
echo ""
echo "Updating scripts/ files..."

for file in scripts/*.py; do
    if [ -f "$file" ]; then
        sed -i '' 's/^from data_loader import/from src.data_loader import/g' "$file"
        sed -i '' 's/^from vector_store import/from src.vector_store import/g' "$file"
        sed -i '' 's/^from chatbot import/from src.chatbot import/g' "$file"
        sed -i '' 's/^from hybrid_engine import/from src.hybrid_engine import/g' "$file"

        echo "  ✓ Updated $file"
    fi
done

# Update shell scripts to point to new locations
echo ""
echo "Updating shell scripts..."

# Update start scripts
if [ -f "scripts/start_upload.sh" ]; then
    sed -i '' 's/streamlit run chatbot_upload_ui.py/streamlit run ui\/chatbot_upload_ui.py/g' scripts/start_upload.sh
    echo "  ✓ Updated scripts/start_upload.sh"
fi

if [ -f "scripts/start_hybrid.sh" ]; then
    sed -i '' 's/streamlit run chatbot_hybrid_ui.py/streamlit run ui\/chatbot_hybrid_ui.py/g' scripts/start_hybrid.sh
    echo "  ✓ Updated scripts/start_hybrid.sh"
fi

if [ -f "scripts/start_web.sh" ]; then
    sed -i '' 's/streamlit run chatbot_ui.py/streamlit run ui\/chatbot_ui.py/g' scripts/start_web.sh
    echo "  ✓ Updated scripts/start_web.sh"
fi

echo ""
echo "=========================================="
echo "✅ Import Updates Complete!"
echo "=========================================="
echo ""
