# How to Run the Restructured Excel Chatbot

## ✅ Fixed! The import errors are resolved.

## 🚀 Quick Start

### Option 1: Use the run script (Easiest)
```bash
./run.sh
```

### Option 2: Direct command
```bash
source venv/bin/activate
streamlit run ui/chatbot_upload_ui.py
```

### Option 3: Use the scripts folder
```bash
bash scripts/start_upload.sh
```

---

## 📂 Project Structure

```
excel_chatbot/
├── run.sh                    ← Quick start script
├── src/                      ← Core modules
│   ├── data_loader.py
│   ├── vector_store.py
│   ├── chatbot.py
│   └── hybrid_engine.py
├── ui/                       ← User interfaces
│   └── chatbot_upload_ui.py  ← Main app
├── data/
│   └── generated/            ← Your Excel files are here!
│       ├── DummyData_Book1_Generated.xlsx
│       ├── DummyData_Book2_Generated.xlsx
│       └── DummyData_Book3_Generated.xlsx
└── scripts/
    └── start_upload.sh       ← Alternative start script
```

---

## 🌐 Access the App

Once started, open your browser:
- **Local:** http://localhost:8501
- **Network:** http://10.40.69.106:8501

---

## 📤 Upload Your Files

Your Excel files are in: `data/generated/`
- DummyData_Book1_Generated.xlsx
- DummyData_Book2_Generated.xlsx  
- DummyData_Book3_Generated.xlsx

---

## 🛑 Stop the App

Press `Ctrl+C` in the terminal

Or kill all Streamlit processes:
```bash
pkill -f streamlit
```

---

## 🔧 What Was Fixed

The import error was caused by Python not finding the `src` module.

**Solution:** Added this to all UI and test files:
```python
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```

Now Python can find `src/` from any location!

---

## ✨ Quick Commands

| Command | Purpose |
|---------|---------|
| `./run.sh` | Start the app |
| `bash scripts/start_upload.sh` | Start via scripts |
| `pkill -f streamlit` | Stop the app |
| `source venv/bin/activate` | Activate virtual environment |

---

## 🆘 Troubleshooting

### Import errors?
```bash
source venv/bin/activate
python -c "from src.data_loader import ExcelDataLoader; print('✓ Works')"
```

### Port already in use?
```bash
pkill -f streamlit
sleep 2
./run.sh
```

### Missing dependencies?
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

**Your app is ready!** Run: `./run.sh` 🎉
