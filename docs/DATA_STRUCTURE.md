# Data Structure Analysis

## Overview
The project contains two Excel files with actuarial life insurance data:

### File 1: actuarial_life_data_file1.xlsx
Contains policy and claims information with **452 total rows** across 2 sheets.

#### Sheet 1: Policy_Details (301 rows, 13 columns)
**Purpose:** Core policy information and policyholder demographics

**Columns:**
- `Policy_ID`: Unique policy identifier (e.g., P00001)
- `Segment_ID`: Segment classification (S01-S10)
- `Class`: Policy class (Retail, Group, Micro)
- `Subclass`: Detailed classification (Endowment, Whole Life, Term, Employer Group, etc.)
- `Issue_Date`: Policy issue date
- `Age`: Policyholder age at issue
- `Gender`: M/F
- `Sum_Assured`: Coverage amount
- `Premium`: Premium amount
- `Term_Years`: Policy term in years
- `Policy_Status`: Current status
- `Distribution_Channel`: How policy was sold
- `Region`: Geographic region

#### Sheet 2: Claims_Experience (151 rows, 11 columns)
**Purpose:** Claims data and settlement information

**Columns:**
- `Claim_ID`: Unique claim identifier (e.g., C00001)
- `Policy_ID`: Foreign key to Policy_Details
- `Segment_ID`: Segment classification
- `Class`: Policy class
- `Subclass`: Policy subclass
- `Claim_Type`: Type of claim (Death, Surrender, Maturity, Rider)
- `Claim_Date`: Date claim was filed
- `Claim_Amount`: Claim amount
- `Settlement_Status`: Approved/Rejected/Pending
- `Days_To_Settle`: Settlement duration
- `Fraud_Flag`: Fraud indicator

### File 2: actuarial_life_data_file2.xlsx
Contains actuarial assumptions and financial metrics with **562 total rows** across 2 sheets.

#### Sheet 3: Mortality_Assumptions (261 rows, 7 columns)
**Purpose:** Mortality rates and actuarial assumptions by segment, age, and gender

**Columns:**
- `Segment_ID`: Segment classification (links to other tables)
- `Age`: Age group
- `Gender`: M/F
- `q_x`: Mortality rate (probability of death)
- `l_x`: Lives remaining (actuarial notation)
- `Exposure`: Exposure units
- `Mortality_Table`: Reference mortality table (Standard_Ultimate, IND_2012-14)

#### Sheet 4: Premiums_and_Reserves (301 rows, 11 columns)
**Purpose:** Financial metrics including premiums, reserves, and persistency

**Columns:**
- `Policy_ID`: Unique policy identifier (links to Policy_Details)
- `Segment_ID`: Segment classification
- `Class`: Policy class
- `Subclass`: Policy subclass
- `Annual_Premium`: Annual premium amount
- `Modal_Premium`: Premium per payment period
- `Reserve`: Policy reserve amount
- `Expense_Ratio`: Expense as % of premium
- `Discount_Rate`: Discount rate for valuation
- `Persistency_13M`: 13-month persistency rate
- `Persistency_25M`: 25-month persistency rate

## Relationships

### Primary Relationships:
1. **Policy_Details ↔ Claims_Experience**
   - Join key: `Policy_ID`
   - One-to-many: One policy can have multiple claims
   - Allows analysis of claims by policy characteristics

2. **Policy_Details ↔ Premiums_and_Reserves**
   - Join key: `Policy_ID`
   - One-to-one: Each policy has corresponding financial metrics
   - Links operational data with financial data

3. **All sheets ↔ Mortality_Assumptions**
   - Join keys: `Segment_ID`, `Age`, `Gender`
   - Provides actuarial assumptions for risk analysis
   - Enables mortality experience analysis

### Common Dimensions:
- **Segment_ID**: Appears in all 4 sheets - primary segmentation dimension
- **Class/Subclass**: Product classification system
- **Gender**: Demographic dimension in multiple sheets

## Data Scale and Performance Considerations

**Current Data:**
- Total rows: ~1,014 rows across all sheets
- This is sample data; the system is designed for 100k+ rows

**Scalability Features Implemented:**
1. Chunked reading (10,000 rows per chunk)
2. Batch embedding generation (32 documents per batch)
3. Vector indexing for fast similarity search
4. Efficient data structures using pandas

## Use Cases

The data structure supports queries like:
- **Policy Analysis**: "Show me all Term Life policies issued in 2021"
- **Claims Analysis**: "What's the average claim amount for Death claims?"
- **Mortality Analysis**: "Compare mortality rates between male and female policyholders"
- **Financial Analysis**: "What segments have the highest reserve ratios?"
- **Cross-file Analysis**: "Show claim patterns for policies with high persistency rates"
- **Risk Assessment**: "Identify policies with mortality rates exceeding assumptions"

## Technical Notes

- All data loaded successfully using openpyxl and pandas
- Vector embeddings created using sentence-transformers (all-MiniLM-L6-v2)
- Data indexed in ChromaDB for semantic search
- Claude API integration for natural language query processing
