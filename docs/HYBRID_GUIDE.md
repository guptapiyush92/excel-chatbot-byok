# Hybrid Query System - User Guide

## 🎯 What's New?

Your chatbot now has **TWO intelligent engines** working together:

### 1. **Structured Query Engine** (NEW!)
- For **precise, exact data** retrieval
- Generates pandas code automatically
- Returns data in tables
- Perfect for: filters, aggregations, specific IDs, counts, sums

### 2. **RAG Engine** (Original)
- For **semantic understanding** and insights
- Uses vector search
- Returns natural language explanations
- Perfect for: general questions, patterns, concepts

### 3. **Automatic Router**
- **Intelligently decides** which engine to use
- You don't need to specify - it figures it out!
- Can even use **both** for complex queries

---

## 🚀 How to Use

### Start the Hybrid Chatbot

```bash
# Option 1: Quick script
./start_hybrid.sh

# Option 2: Direct command
source venv/bin/activate
streamlit run chatbot_hybrid_ui.py
```

Opens at: **http://localhost:8501**

---

## 💡 Query Examples

### ✅ Structured Queries (Get Exact Data)

These will use the **structured engine** and return precise, tabular results:

**Specific Row Lookups:**
```
Give me all details of policy ID P00225
Show me claim ID C00050
Get information for policy P00100
```

**Filtering:**
```
All policies in class Micro in table format
Show policies with premiums > 50000
Claims with fraud flags
Policies in segment S05
```

**Aggregations:**
```
Average premium by policy class
Total claim amount by claim type
Count of policies per segment
Sum of reserves by class
```

**Joins:**
```
Show policies with their claim history
Compare premiums and reserves for policy P00225
All approved death claims with policy details
```

### 🧠 Semantic Queries (Get Insights)

These will use the **RAG engine** for understanding:

**General Understanding:**
```
What data is available in these files?
Explain the structure of the data
What sheets exist?
```

**Conceptual Questions:**
```
What does persistency rate mean?
Explain mortality assumptions
What is expense ratio?
How do reserves work?
```

**Pattern Discovery:**
```
What patterns exist in the claims data?
Summarize the mortality data
What insights can you find about fraud?
```

---

## 📊 What You Get

### Structured Query Results

When you ask for specific data, you get:

1. **📋 Classification** - Shows it was routed to structured engine
2. **💬 Explanation** - Human-readable answer
3. **📊 Data Table** - Actual data in tabular format
4. **📥 Download Button** - Export to CSV
5. **🔧 Generated Code** - See the pandas code (optional)

**Example Output:**
```
Query: "All policies in class Micro"

✅ Structured Query Result

Found 89 policies in the Micro class across segments S01-S10.

📊 Data (89 rows):
Policy_ID | Class | Subclass      | Premium  | Sum_Assured
P00001    | Micro | Rural Micro   | 33535.01 | 4674866
P00005    | Micro | Urban Micro   | 20874.91 | 1464441
...

[Download as CSV button]
```

### Semantic Query Results

When you ask conceptual questions:

1. **📋 Classification** - Shows it was routed to RAG
2. **💬 Natural Language Answer** - Comprehensive explanation
3. **📚 Source Context** - Which data was used (optional)

**Example Output:**
```
Query: "What data is available?"

✅ Semantic Analysis Result

The Excel files contain 4 sheets with actuarial life insurance data:

1. **Policy_Details** - 301 policies with demographics...
2. **Claims_Experience** - 151 claims with settlements...
...
```

---

## 🎓 Tips for Best Results

### For Exact Data (Structured):
- ✅ Use specific IDs: "policy P00225", "claim C00050"
- ✅ Request tables: "in table format", "show all columns"
- ✅ Be specific with filters: "class = Micro", "premium > 50000"
- ✅ Ask for calculations: "average", "sum", "count"

### For Understanding (Semantic):
- ✅ Ask open questions: "what", "explain", "describe"
- ✅ Request insights: "patterns", "trends", "summarize"
- ✅ Ask about concepts: "what does X mean?"

### What Works Best:
- **Good:** "Give me all details of policy P00225"
- **Good:** "All policies in class Micro"
- **Good:** "Average premium by segment"
- **Good:** "What data is available?"

### What to Avoid:
- **Avoid vague:** "Show me some policies" (which ones?)
- **Better:** "Show me first 10 policies" or "policies with premium > 50000"

---

## 🔍 How the Router Works

The system analyzes your query and automatically decides:

| Your Query Contains... | Router Chooses | Why |
|------------------------|----------------|-----|
| Specific ID (P00225) | **Structured** | Needs exact row lookup |
| "in table format" | **Structured** | Wants tabular output |
| "average", "sum", "count" | **Structured** | Needs calculation |
| Exact filters ("class Micro") | **Structured** | Needs precise filtering |
| "what", "explain", "describe" | **RAG** | Needs understanding |
| "pattern", "insight", "summarize" | **RAG** | Needs analysis |
| "what data is available" | **RAG** | Needs overview |

---

## 🆚 Comparison: Old vs New

### OLD System (RAG Only):
```
Query: "Give me details of policy P00225"

❌ Result: Vague description, approximate data
"Based on the context, policy P00225 appears to be
a Micro class policy with some premium information..."
```

### NEW System (Hybrid):
```
Query: "Give me details of policy P00225"

✅ Result: Exact, complete data in table

Policy_ID: P00225
Class: Micro
Subclass: Rural Micro
Age: 42
Gender: M
Sum_Assured: 959,221
Premium: 7,270.93
Term_Years: 15
Status: Matured
[...all 20+ fields with exact values]
```

---

## 🎯 Use Cases

### Business Analysis
```
Average claim amount by claim type
Policies with reserves > 1 million
Claims approval rate by segment
Persistency trends by class
```

### Specific Lookups
```
All details for policy P00150
Claims for policy P00225
Mortality rates for age 30 males
Premiums for segment S05
```

### Understanding
```
What does the data tell us about fraud?
Explain the relationship between files
Summarize persistency patterns
What insights exist in claims?
```

---

## 📁 Files

**New Files:**
- `hybrid_engine.py` - Core hybrid query engine
- `chatbot_hybrid_ui.py` - Streamlit interface
- `test_hybrid.py` - Test script
- `start_hybrid.sh` - Quick launcher

**Original Files (Still Available):**
- `chatbot_ui.py` - Original RAG-only UI
- `chatbot_cli.py` - Command-line interface

---

## 🚀 Quick Start

```bash
# 1. Launch hybrid chatbot
./start_hybrid.sh

# 2. Try structured query
"Give me all details of policy P00225"

# 3. Try semantic query
"What data is available?"

# 4. Try filtered query
"All policies in class Micro in table format"
```

---

## 🎊 Result

You now have the **best of both worlds**:
- ✅ **Precise data** when you need it
- ✅ **Semantic understanding** when you want it
- ✅ **Automatic routing** - no need to choose
- ✅ **Same friendly interface**

**No more vague answers for specific queries!** 🎯
