# Project Restructure Plan

## Current Issues
- 45+ files in root directory (very cluttered)
- Multiple Excel files (original + generated + temp)
- Multiple similar UI files (3 different versions)
- Documentation scattered (7 markdown files)
- Test files mixed with production code
- Temp/lock files (~$ prefix) present

## Proposed Structure

```
excel_chatbot/
├── README.md                      # Main project overview
├── requirements.txt               # Dependencies
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
│
├── src/                          # Source code
│   ├── __init__.py
│   ├── data_loader.py            # Data loading logic
│   ├── vector_store.py           # Vector DB operations
│   ├── chatbot.py                # Core chatbot logic
│   └── hybrid_engine.py          # Hybrid query engine
│
├── ui/                           # User interfaces
│   ├── __init__.py
│   ├── chatbot_cli.py            # CLI interface
│   ├── chatbot_ui.py             # Basic web UI
│   ├── chatbot_hybrid_ui.py      # Hybrid web UI
│   └── chatbot_upload_ui.py      # Upload web UI (recommended)
│
├── scripts/                      # Utility scripts
│   ├── setup.sh                  # Setup script
│   ├── start_web.sh              # Start basic web UI
│   ├── start_hybrid.sh           # Start hybrid UI
│   ├── start_upload.sh           # Start upload UI
│   └── analyze_excel.py          # Excel analysis tool
│
├── tests/                        # Test files
│   ├── __init__.py
│   ├── test_setup.py             # Setup verification
│   ├── test_hybrid.py            # Hybrid engine tests
│   ├── test_models.py            # Model tests
│   └── quick_test.py             # Quick sanity tests
│
├── data/                         # Data files
│   ├── sample/                   # Sample data
│   │   ├── actuarial_life_data_file1.xlsx
│   │   └── actuarial_life_data_file2.xlsx
│   └── generated/                # Generated dummy data
│       ├── DummyData_Book1_Generated.xlsx
│       ├── DummyData_Book2_Generated.xlsx
│       └── DummyData_Book3_Generated.xlsx
│
├── docs/                         # Documentation
│   ├── USER_GUIDE.md
│   ├── QUICK_START.md
│   ├── DATA_STRUCTURE.md
│   ├── HYBRID_GUIDE.md
│   ├── UPLOAD_GUIDE.md
│   ├── PROJECT_SUMMARY.md
│   ├── FINAL_SUMMARY.md
│   └── REGENERATED_FILES_SUMMARY.txt
│
├── chroma_db/                    # Vector database (gitignored)
├── venv/                         # Virtual environment (gitignored)
└── .env                          # Environment variables (gitignored)
```

## Benefits
1. ✅ Clear separation of concerns
2. ✅ Easy to find files by purpose
3. ✅ Cleaner root directory (only 4 files)
4. ✅ Better for version control
5. ✅ Professional structure
6. ✅ Easier onboarding for new developers
7. ✅ Follows Python best practices

## Migration Steps
1. Create directory structure
2. Move files to appropriate directories
3. Update import statements in Python files
4. Update script paths
5. Clean up temporary/lock files
6. Update .gitignore
7. Test everything works

