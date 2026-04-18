# Rich Message Formatting in Excel Chatbot

The FastAPI version now supports rich markdown formatting in chat responses!

## ✨ Supported Formatting

### 1. **Headers**
Use `#`, `##`, `###` for different heading levels

### 2. **Tables**

Perfect for displaying data:

| Name | Age | Department | Salary |
|------|-----|------------|--------|
| John | 30  | Engineering| $80,000|
| Jane | 28  | Marketing  | $75,000|
| Bob  | 35  | Sales      | $70,000|

### 3. **Code Blocks**

With syntax highlighting:

```python
def calculate_average(data):
    """Calculate average from Excel data."""
    return sum(data) / len(data)

# Example usage
values = [100, 200, 300, 400]
avg = calculate_average(values)
print(f"Average: {avg}")
```

```sql
SELECT
    Department,
    COUNT(*) as Employees,
    AVG(Salary) as AvgSalary
FROM Employees
GROUP BY Department
ORDER BY AvgSalary DESC;
```

### 4. **Inline Code**

Use `backticks` for inline code like `SUM(A1:A10)` or `pandas.DataFrame`.

### 5. **Lists**

**Bullet points:**
- First item with **bold text**
- Second item with *italic text*
- Third item with `inline code`
  - Nested item 1
  - Nested item 2

**Numbered lists:**
1. First step in the process
2. Second step with details
3. Third step with `formula`
4. Final step

### 6. **Emphasis**

- **Bold text** for important information
- *Italic text* for emphasis
- ***Bold and italic*** for extra emphasis
- ~~Strikethrough~~ for corrections

### 7. **Blockquotes**

> "Data is the new oil. It's valuable, but if unrefined it cannot really be used."
> — Clive Humby

### 8. **Horizontal Rules**

Use `---` for separators:

---

### 9. **Links**

Check out the [documentation](https://github.com/your-repo) for more details.

### 10. **Mixed Content**

You can combine everything:

## 📊 Sales Analysis Results

Here's what I found in your data:

**Total Revenue:** $1,234,567

### Top Performing Regions

| Region    | Revenue   | Growth |
|-----------|-----------|--------|
| North     | $456,789  | +15%   |
| South     | $345,678  | +12%   |
| East      | $234,567  | +8%    |
| West      | $197,533  | +5%    |

### Key Findings

1. **North region** leads with 37% of total revenue
2. Growth is consistent across all regions
3. Q4 showed the strongest performance with:
   - November: `$450,000`
   - December: `$520,000`
   - January: `$380,000`

### Recommended Actions

- ✅ Invest more in North region marketing
- ✅ Analyze factors contributing to East region growth
- ⚠️ West region needs attention - consider new strategies

### SQL Query Used

```sql
SELECT
    Region,
    SUM(Revenue) as TotalRevenue,
    ROUND(AVG(GrowthRate), 2) as AvgGrowth
FROM SalesData
WHERE Year = 2024
GROUP BY Region
ORDER BY TotalRevenue DESC;
```

---

**Note:** All calculations are based on the uploaded Excel data.

---

## 🎨 Styling Features

### Syntax Highlighting

Code blocks automatically get syntax highlighting for:
- Python
- SQL
- JavaScript
- JSON
- Excel formulas
- And many more!

### Responsive Tables

Tables automatically scroll horizontally on small screens while maintaining readability.

### Dark Code Blocks

Code blocks use a beautiful dark theme with proper syntax colors for better readability.

---

## 💡 How It Works

The AI is now instructed to:

1. **Use tables** when presenting structured data
2. **Use bullet points** for lists of items
3. **Use code blocks** for formulas and queries
4. **Use bold** for important numbers and findings
5. **Use headings** to organize long responses

This makes responses much more readable and professional!

---

## 🚀 Try These Sample Queries

Ask questions like:

- "Show me the top 5 customers by revenue in a table"
- "What's the average sales by region? Format as a table"
- "List the key findings from the data"
- "Show me the SQL query to calculate total revenue"
- "Summarize the data with headings and formatting"

The AI will automatically format the response with rich markdown!

---

## Technical Details

**Libraries Used:**
- [Marked.js](https://marked.js.org/) - Markdown parser
- [Highlight.js](https://highlightjs.org/) - Code syntax highlighting

**Supported Markdown:**
- GitHub Flavored Markdown (GFM)
- Tables
- Code blocks with syntax highlighting
- Lists (ordered and unordered)
- Headers (H1-H6)
- Bold, italic, strikethrough
- Blockquotes
- Horizontal rules
- Links

---

**Enjoy beautiful, formatted responses! 🎉**
