# Project Restructure Guide

## 🎯 Quick Start

Run the automated restructure:

```bash
bash restructure_all.sh
```

This will reorganize everything automatically!

## 📋 What Will Change

### Before (Cluttered - 45+ files in root):
```
excel_chatbot/
├── data_loader.py
├── vector_store.py
├── chatbot.py
├── hybrid_engine.py
├── chatbot_cli.py
├── chatbot_ui.py
├── chatbot_hybrid_ui.py
├── chatbot_upload_ui.py
├── test_setup.py
├── test_hybrid.py
├── analyze_excel.py
├── actuarial_life_data_file1.xlsx
├── DummyData_Book1_Generated.xlsx
├── USER_GUIDE.md
├── PROJECT_SUMMARY.md
├── ... (30+ more files)
```

### After (Clean - 4 files + 6 folders):
```
excel_chatbot/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── src/                          ← Core logic
│   ├── data_loader.py
│   ├── vector_store.py
│   ├── chatbot.py
│   └── hybrid_engine.py
│
├── ui/                           ← All interfaces
│   ├── chatbot_cli.py
│   ├── chatbot_ui.py
│   ├── chatbot_hybrid_ui.py
│   └── chatbot_upload_ui.py
│
├── scripts/                      ← Utilities
│   ├── setup.sh
│   ├── start_upload.sh
│   └── analyze_excel.py
│
├── tests/                        ← All tests
│   ├── test_setup.py
│   └── test_hybrid.py
│
├── data/                         ← All data
│   ├── sample/
│   │   ├── actuarial_life_data_file1.xlsx
│   │   └── actuarial_life_data_file2.xlsx
│   └── generated/
│       ├── DummyData_Book1_Generated.xlsx
│       ├── DummyData_Book2_Generated.xlsx
│       └── DummyData_Book3_Generated.xlsx
│
└── docs/                         ← All documentation
    ├── USER_GUIDE.md
    ├── QUICK_START.md
    ├── PROJECT_SUMMARY.md
    └── ...
```

## ✅ Benefits

1. **Cleaner Root** - Only 4 essential files
2. **Logical Organization** - Files grouped by purpose
3. **Professional** - Follows Python best practices
4. **Scalable** - Easy to add new features
5. **Version Control** - Better for Git
6. **Developer Friendly** - Easy onboarding

## 🔧 Manual Steps (if needed)

If you prefer manual control:

### Step 1: Restructure
```bash
bash restructure_project.sh
```

### Step 2: Update Imports
```bash
bash update_imports.sh
```

### Step 3: Verify
```bash
python -m pytest tests/
streamlit run ui/chatbot_upload_ui.py
```

## 📝 Import Changes

All Python files will be updated automatically:

**Before:**
```python
from data_loader import ExcelDataLoader
from vector_store import VectorStore
```

**After:**
```python
from src.data_loader import ExcelDataLoader
from src.vector_store import VectorStore
```

## 🚀 Starting the App

**Before restructure:**
```bash
streamlit run chatbot_upload_ui.py
```

**After restructure:**
```bash
# Option 1: Use script
bash scripts/start_upload.sh

# Option 2: Direct command
streamlit run ui/chatbot_upload_ui.py
```

## ⚠️ Important Notes

1. **Backup First** - The script is safe, but always good to backup
2. **Virtual Environment** - `venv/` stays in root (not moved)
3. **ChromaDB** - `chroma_db/` stays in root (not moved)
4. **Environment** - `.env` stays in root (gitignored)
5. **Temp Files** - Excel lock files (~$*.xlsx) will be cleaned up

## 🧪 Testing After Restructure

Test that everything works:

```bash
# Activate virtual environment
source venv/bin/activate

# Test imports
python -c "from src.data_loader import ExcelDataLoader; print('✓ Imports work')"

# Run test suite
python -m pytest tests/

# Start the app
streamlit run ui/chatbot_upload_ui.py
```

## 📂 File Locations Reference

| Old Location | New Location |
|-------------|--------------|
| `data_loader.py` | `src/data_loader.py` |
| `chatbot_upload_ui.py` | `ui/chatbot_upload_ui.py` |
| `test_setup.py` | `tests/test_setup.py` |
| `analyze_excel.py` | `scripts/analyze_excel.py` |
| `actuarial_life_data_file1.xlsx` | `data/sample/actuarial_life_data_file1.xlsx` |
| `DummyData_Book1_Generated.xlsx` | `data/generated/DummyData_Book1_Generated.xlsx` |
| `USER_GUIDE.md` | `docs/USER_GUIDE.md` |
| `setup.sh` | `scripts/setup.sh` |

## 🔄 Rollback (if needed)

If something goes wrong, all files are just moved (not deleted).
You can manually move them back or restore from Git:

```bash
git checkout .
git clean -fd
```

## 📞 Support

If you encounter issues:
1. Check that virtual environment is activated
2. Verify Python path includes project root
3. Check import statements manually
4. Review the error messages

---

**Ready to restructure?** Run:
```bash
bash restructure_all.sh
```
