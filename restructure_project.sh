#!/bin/bash

# Excel Chatbot - Project Restructuring Script
# This script reorganizes the project into a cleaner structure

set -e  # Exit on error

echo "=========================================="
echo "Excel Chatbot - Project Restructure"
echo "=========================================="
echo ""

# Confirm with user
read -p "This will reorganize your project structure. Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "Step 1: Creating directory structure..."

# Create directories
mkdir -p src
mkdir -p ui
mkdir -p scripts
mkdir -p tests
mkdir -p data/sample
mkdir -p data/generated
mkdir -p docs

echo "✓ Directories created"

echo ""
echo "Step 2: Moving source code..."

# Move core source files to src/
mv data_loader.py src/ 2>/dev/null || true
mv vector_store.py src/ 2>/dev/null || true
mv chatbot.py src/ 2>/dev/null || true
mv hybrid_engine.py src/ 2>/dev/null || true

# Create __init__.py
touch src/__init__.py

echo "✓ Source code moved to src/"

echo ""
echo "Step 3: Moving UI files..."

# Move UI files
mv chatbot_cli.py ui/ 2>/dev/null || true
mv chatbot_ui.py ui/ 2>/dev/null || true
mv chatbot_hybrid_ui.py ui/ 2>/dev/null || true
mv chatbot_upload_ui.py ui/ 2>/dev/null || true

touch ui/__init__.py

echo "✓ UI files moved to ui/"

echo ""
echo "Step 4: Moving scripts..."

# Move scripts
mv setup.sh scripts/ 2>/dev/null || true
mv start_web.sh scripts/ 2>/dev/null || true
mv start_hybrid.sh scripts/ 2>/dev/null || true
mv start_upload.sh scripts/ 2>/dev/null || true
mv analyze_excel.py scripts/ 2>/dev/null || true

# Make scripts executable
chmod +x scripts/*.sh 2>/dev/null || true

echo "✓ Scripts moved to scripts/"

echo ""
echo "Step 5: Moving test files..."

# Move test files
mv test_setup.py tests/ 2>/dev/null || true
mv test_hybrid.py tests/ 2>/dev/null || true
mv test_models.py tests/ 2>/dev/null || true
mv quick_test.py tests/ 2>/dev/null || true

touch tests/__init__.py

echo "✓ Test files moved to tests/"

echo ""
echo "Step 6: Moving data files..."

# Move sample data
mv actuarial_life_data_file1.xlsx data/sample/ 2>/dev/null || true
mv actuarial_life_data_file2.xlsx data/sample/ 2>/dev/null || true

# Move generated data
mv DummyData_Book1_Generated.xlsx data/generated/ 2>/dev/null || true
mv DummyData_Book2_Generated.xlsx data/generated/ 2>/dev/null || true
mv DummyData_Book3_Generated.xlsx data/generated/ 2>/dev/null || true

# Move old versions to generated (for backup)
mv DummyData_Book*.xlsx data/generated/ 2>/dev/null || true

echo "✓ Data files moved to data/"

echo ""
echo "Step 7: Moving documentation..."

# Move docs
mv USER_GUIDE.md docs/ 2>/dev/null || true
mv QUICK_START.md docs/ 2>/dev/null || true
mv DATA_STRUCTURE.md docs/ 2>/dev/null || true
mv HYBRID_GUIDE.md docs/ 2>/dev/null || true
mv UPLOAD_GUIDE.md docs/ 2>/dev/null || true
mv PROJECT_SUMMARY.md docs/ 2>/dev/null || true
mv FINAL_SUMMARY.md docs/ 2>/dev/null || true
mv REGENERATED_FILES_SUMMARY.txt docs/ 2>/dev/null || true
mv RESTRUCTURE_PLAN.md docs/ 2>/dev/null || true

echo "✓ Documentation moved to docs/"

echo ""
echo "Step 8: Cleaning up temporary files..."

# Remove Excel temp/lock files
rm -f ~\$*.xlsx 2>/dev/null || true

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo "✓ Temporary files removed"

echo ""
echo "Step 9: Creating updated .gitignore..."

cat > .gitignore << 'GITIGNORE'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project specific
.env
chroma_db/
*.log

# Excel temp files
~$*.xlsx
~$*.xls

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
GITIGNORE

echo "✓ .gitignore updated"

echo ""
echo "=========================================="
echo "✅ Restructure Complete!"
echo "=========================================="
echo ""
echo "New structure:"
echo "  src/        - Core source code"
echo "  ui/         - User interfaces"
echo "  scripts/    - Utility scripts"
echo "  tests/      - Test files"
echo "  data/       - Data files (sample & generated)"
echo "  docs/       - Documentation"
echo ""
echo "⚠️  IMPORTANT: You need to update import statements!"
echo ""
echo "Run the update script next:"
echo "  bash update_imports.sh"
echo ""
