# File Upload Feature - User Guide

## 🎉 What's New?

You can now **upload your own Excel files** directly in the web interface! No need to place files in the project directory anymore.

---

## 🚀 How to Use

### 1. Launch the Upload Interface

```bash
# Quick start
./start_upload.sh

# Or manually
source venv/bin/activate
streamlit run chatbot_upload_ui.py
```

Opens at: **http://localhost:8501**

---

### 2. Upload Your Files

**In the sidebar:**

1. Click **"Choose Excel files"**
2. Select one or more `.xlsx` or `.xls` files
3. Review the files and their sizes
4. Click **"🚀 Process Files"**

**Processing steps (automatic):**
- 📂 Loads Excel files
- 🔍 Analyzes structure
- 📊 Loads data into memory
- 🧮 Prepares documents
- 🔤 Creates vector embeddings
- 📥 Indexes for search
- 🤖 Initializes hybrid engine

**Time:** 10-30 seconds depending on file size

---

### 3. Start Querying

Once files are processed, you can:
- Ask structured queries (exact data)
- Ask semantic queries (insights)
- View data statistics
- Download results as CSV

---

## 📋 Supported Files

### File Formats
- ✅ `.xlsx` (Excel 2007+)
- ✅ `.xls` (Legacy Excel)

### File Sizes
- ✅ **Small:** Few KBs - instant processing
- ✅ **Medium:** 1-10 MB - 10-20 seconds
- ✅ **Large:** 10-50 MB - 30-60 seconds
- ⚠️ **Very Large:** 50-200 MB - may take 2-3 minutes

### Data Volume
- ✅ **Optimized for:** 100k+ rows per file
- ✅ **Tested with:** Multiple files, multiple sheets
- ✅ **Memory efficient:** Chunked processing

---

## 📊 What Gets Processed?

### Automatic Analysis:
1. **All sheets** in each file
2. **All columns** and their data types
3. **Relationships** between sheets (common columns)
4. **Sample data** for schema understanding
5. **Vector embeddings** for semantic search

### Data Structure Detected:
- Column names and types
- Number of rows per sheet
- Relationships via foreign keys
- Sample values for context

---

## 💡 Features

### 📤 Upload Multiple Files
```
Upload as many Excel files as you need:
- file1.xlsx (Sales data)
- file2.xlsx (Customer data)
- file3.xlsx (Product catalog)

System will process all files together!
```

### 🔄 Re-upload Anytime
```
1. Click "🗑️ Clear Data" in sidebar
2. Upload new files
3. Click "🚀 Process Files"

Old data is completely replaced.
```

### 📊 View Statistics
```
Sidebar shows:
- Number of files loaded
- Total sheets across all files
- Total rows of data
- Number of indexed documents
```

### 💾 Download Results
```
For structured queries:
- View results in table
- Click "📥 Download as CSV"
- Save to your computer
```

---

## 🎯 Example Workflows

### Workflow 1: Analyze Sales Data

**Upload:**
- `sales_2023.xlsx`
- `sales_2024.xlsx`

**Query:**
```
"What's the total revenue by quarter?"
"Show top 10 customers by sales"
"Compare 2023 vs 2024 performance"
```

### Workflow 2: HR Analytics

**Upload:**
- `employees.xlsx`
- `performance_reviews.xlsx`
- `salary_data.xlsx`

**Query:**
```
"Details for employee ID E12345"
"Average salary by department"
"All employees with performance rating > 4"
```

### Workflow 3: Financial Analysis

**Upload:**
- `transactions.xlsx`
- `accounts.xlsx`

**Query:**
```
"Total transactions by account type"
"Show all transactions > 10000"
"Explain the account structure"
```

---

## ⚡ Performance Tips

### For Fast Processing:
1. **Smaller files first** - Test with small files initially
2. **Fewer sheets** - Remove unnecessary sheets before upload
3. **Clean data** - Remove empty rows/columns
4. **Reasonable size** - Keep files under 50MB when possible

### For Large Files:
1. **Be patient** - Large files need time to vectorize
2. **Check progress** - Watch the progress bar
3. **Split if needed** - Consider splitting 100MB+ files
4. **Close other apps** - Free up system memory

---

## 🔍 What Happens Behind the Scenes?

### 1. File Upload (Instant)
- Files saved to temporary directory
- Original files remain untouched

### 2. Data Loading (5-10s)
- Excel sheets parsed
- Data loaded into pandas DataFrames
- Schema analyzed

### 3. Document Preparation (5-10s)
- Rows converted to text documents
- Metadata attached (file, sheet, row range)
- Documents chunked for efficient search

### 4. Vectorization (10-30s)
- Text converted to vector embeddings
- Uses sentence-transformers model
- Optimized for semantic similarity

### 5. Indexing (5-10s)
- Vectors stored in ChromaDB
- Fast similarity search enabled
- Persistent storage created

### 6. Ready! (Instant)
- Hybrid engine initialized
- Both structured and semantic queries enabled
- Chat interface activated

---

## 🆚 Upload vs Default Files

### With Upload:
✅ Use your own data
✅ Change files anytime
✅ Multiple file types
✅ Flexible workflows
✅ No manual file copying

### With Default Files:
✅ Quick testing
✅ Demo purposes
✅ Example queries
✅ Pre-loaded data

**You can use both!** Upload for your data, default for testing.

---

## 🛡️ Data Security

### Where Files Are Stored:
- **Temporary directory** during session
- **Automatically deleted** when you clear data
- **In-memory processing** for queries
- **Vector DB local** (not cloud)

### What Gets Saved:
- ✅ Vector embeddings (local ChromaDB)
- ✅ DataFrames (in-memory only)
- ❌ Original files (deleted after processing)
- ❌ No cloud uploads
- ❌ No external storage

### Privacy:
- All processing happens **locally**
- Only Claude API calls go external (for query understanding)
- Your data never leaves your machine (except API queries)

---

## 🔧 Troubleshooting

### "File too large" Error
**Solution:**
- Split file into smaller parts
- Remove unnecessary sheets/columns
- Use filtered exports

### "Processing failed" Error
**Solution:**
- Check file isn't corrupted
- Ensure it's a valid Excel file
- Try re-uploading
- Check file has data (not empty)

### Slow Processing
**Normal for:**
- Files > 20MB
- 100k+ rows
- Many sheets
- First-time model loading

**Speed up:**
- Close other apps
- Use faster computer
- Split large files

### "Out of memory" Error
**Solution:**
- Process one file at a time
- Restart Streamlit
- Close other applications
- Consider smaller chunk sizes

---

## 📝 Quick Reference

### Commands:
```bash
# Launch upload interface
./start_upload.sh

# Or manual launch
source venv/bin/activate
streamlit run chatbot_upload_ui.py
```

### Sidebar Actions:
- **Upload Files** - Choose Excel files
- **Process Files** - Start processing
- **Load Default** - Use example files
- **Clear Data** - Remove all data
- **Clear Chat** - Clear conversation

### File Limits:
- Max size per file: **200MB** (configurable)
- Max files: **No limit** (memory dependent)
- Supported formats: `.xlsx`, `.xls`

---

## 🎊 Benefits

### Flexibility:
✅ No manual file copying
✅ Quick iteration on different datasets
✅ Easy to share (just send the Excel files)
✅ Works with any Excel structure

### Convenience:
✅ All-in-one interface
✅ Visual feedback during processing
✅ Progress tracking
✅ Error messages if issues

### Power:
✅ Handles large files efficiently
✅ Automatic vectorization
✅ Intelligent query routing
✅ Both structured and semantic queries

---

## 🚀 Get Started Now!

```bash
./start_upload.sh
```

1. Upload your Excel files
2. Wait for processing
3. Start asking questions!

**That's it!** The system handles everything else automatically. 🎉
