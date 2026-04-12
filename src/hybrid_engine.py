"""
Hybrid query engine that intelligently routes between structured queries and RAG.
Combines precise data retrieval with semantic understanding.
"""

import pandas as pd
from anthropic import Anthropic
from typing import Dict, Any, List, Optional, Tuple
import logging
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HybridQueryEngine:
    """
    Intelligent query engine that routes between:
    1. Structured queries (pandas/SQL) for precise data retrieval
    2. RAG for semantic understanding and insights
    """

    def __init__(self, dataframes: Dict[str, Dict[str, pd.DataFrame]], vector_store=None):
        """
        Initialize the hybrid query engine.

        Args:
            dataframes: Nested dict {file_name: {sheet_name: dataframe}}
            vector_store: Optional VectorStore for RAG queries
        """
        self.dataframes = dataframes
        self.vector_store = vector_store

        # Initialize Claude client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        base_url = os.getenv("ANTHROPIC_BASE_URL")

        if base_url:
            self.client = Anthropic(api_key=api_key, base_url=base_url)
        else:
            self.client = Anthropic(api_key=api_key)

        self.model = "claude-sonnet"

        # Build schema information
        self.schema_info = self._build_schema_info()

        logger.info("HybridQueryEngine initialized")

    def _build_schema_info(self) -> str:
        """Build a description of available data for Claude."""
        schema_parts = ["# Available Data Structure\n"]

        for file_name, sheets in self.dataframes.items():
            schema_parts.append(f"\n## File: {file_name}")
            for sheet_name, df in sheets.items():
                schema_parts.append(f"\n### Sheet: {sheet_name}")
                schema_parts.append(f"Rows: {len(df)}")
                schema_parts.append(f"Columns: {', '.join(df.columns.tolist())}")
                schema_parts.append(f"Sample data:\n{df.head(3).to_string()}\n")

        return "\n".join(schema_parts)

    def classify_query(self, query: str) -> Tuple[str, str]:
        """
        Classify query type and extract intent.

        Returns:
            Tuple of (query_type, reasoning)
            query_type: 'structured', 'rag', or 'hybrid'
        """
        classification_prompt = f"""Analyze this user query and classify it:

Query: "{query}"

Classification rules:
1. **STRUCTURED** - Use when query needs:
   - Specific row(s) by ID or exact filters (e.g., "policy ID 225", "all claims with status Approved")
   - Exact counts, sums, averages, aggregations
   - Filtering by specific values
   - Tabular output of multiple rows
   - Joins across sheets
   - Examples: "all policies in class Micro", "average premium by segment", "details of claim C00050"

2. **RAG** - Use when query needs:
   - General understanding ("what data is available?", "explain the structure")
   - Conceptual questions ("what does persistency mean?")
   - Pattern discovery without specific numbers
   - Qualitative insights

3. **HYBRID** - Use when query needs both:
   - Structured retrieval THEN analysis
   - Example: "Find high-value policies and analyze their characteristics"

Respond in JSON format:
{{
  "query_type": "structured|rag|hybrid",
  "reasoning": "brief explanation",
  "needs_exact_data": true/false,
  "needs_semantic_understanding": true/false
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": classification_prompt}]
            )

            result_text = response.content[0].text
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                query_type = result.get('query_type', 'structured')
                reasoning = result.get('reasoning', '')
                logger.info(f"Query classified as: {query_type} - {reasoning}")
                return query_type, reasoning
            else:
                logger.warning("Could not parse classification, defaulting to structured")
                return 'structured', 'Default classification'

        except Exception as e:
            logger.error(f"Classification error: {e}")
            # Default to structured for data-specific queries
            return 'structured', 'Error in classification'

    def execute_structured_query(self, query: str) -> Dict[str, Any]:
        """
        Execute a structured query using pandas operations.

        Returns:
            Dict with 'data', 'query_code', 'explanation'
        """
        logger.info(f"Executing structured query: {query}")

        # Generate pandas code using Claude
        code_prompt = f"""You are a pandas expert. Generate Python code to answer this query.

{self.schema_info}

User Query: "{query}"

Available DataFrames:
- df_policy_details: Policy_Details sheet from file 1
- df_claims: Claims_Experience sheet from file 1
- df_mortality: Mortality_Assumptions sheet from file 2
- df_premiums: Premiums_and_Reserves sheet from file 2

Requirements:
1. Write SAFE pandas code (no file I/O, no system calls)
2. Store final result in variable called 'result'
3. Result should be a DataFrame, Series, or simple value
4. Use .copy() when filtering to avoid warnings
5. Handle case-insensitive column access if needed

Example code patterns:
- Filtering: result = df_policy_details[df_policy_details['Policy_ID'] == 'P00225'].copy()
- Aggregation: result = df_claims.groupby('Claim_Type')['Claim_Amount'].mean()
- Join: result = pd.merge(df_policy_details, df_claims, on='Policy_ID')
- Tabular output: result = df_premiums[df_premiums['Class'] == 'Micro'][['Policy_ID', 'Class', 'Annual_Premium']].copy()

Respond with ONLY the Python code, no explanations:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": code_prompt}]
            )

            code = response.content[0].text.strip()

            # Extract code from markdown blocks if present
            if '```python' in code:
                code = re.search(r'```python\n(.*?)\n```', code, re.DOTALL).group(1)
            elif '```' in code:
                code = re.search(r'```\n(.*?)\n```', code, re.DOTALL).group(1)

            logger.info(f"Generated code:\n{code}")

            # Execute the code
            result = self._execute_pandas_code(code)

            # Generate explanation
            explanation = self._explain_result(query, result, code)

            return {
                'success': True,
                'data': result,
                'query_code': code,
                'explanation': explanation,
                'query_type': 'structured'
            }

        except Exception as e:
            logger.error(f"Structured query error: {e}")
            return {
                'success': False,
                'error': str(e),
                'query_type': 'structured'
            }

    def _execute_pandas_code(self, code: str) -> Any:
        """Safely execute pandas code and return result."""
        # Prepare namespace with dataframes
        namespace = {
            'pd': pd,
            'df_policy_details': None,
            'df_claims': None,
            'df_mortality': None,
            'df_premiums': None,
            'result': None
        }

        # Map dataframes to variables
        for file_name, sheets in self.dataframes.items():
            if 'file1' in file_name.lower():
                for sheet_name, df in sheets.items():
                    if 'policy' in sheet_name.lower():
                        namespace['df_policy_details'] = df
                    elif 'claims' in sheet_name.lower():
                        namespace['df_claims'] = df
            elif 'file2' in file_name.lower():
                for sheet_name, df in sheets.items():
                    if 'mortality' in sheet_name.lower():
                        namespace['df_mortality'] = df
                    elif 'premium' in sheet_name.lower():
                        namespace['df_premiums'] = df

        # Execute code
        exec(code, namespace)

        return namespace['result']

    def _explain_result(self, query: str, result: Any, code: str) -> str:
        """Generate human-readable explanation of the result."""
        result_summary = self._summarize_result(result)

        explanation_prompt = f"""Explain this query result to the user in a clear, concise way.

Original Query: "{query}"

Result Summary: {result_summary}

Provide a natural language explanation that:
1. Directly answers the user's question
2. Highlights key findings
3. Uses tables/formatting if appropriate
4. Is accurate and specific

Keep it concise but informative."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": explanation_prompt}]
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Explanation error: {e}")
            return f"Query executed successfully. Result: {result_summary}"

    def _summarize_result(self, result: Any) -> str:
        """Create a text summary of the query result."""
        if isinstance(result, pd.DataFrame):
            if len(result) == 0:
                return "Empty DataFrame (no matching rows)"
            elif len(result) == 1:
                return f"Single row:\n{result.to_string()}"
            else:
                return f"DataFrame with {len(result)} rows and {len(result.columns)} columns:\n{result.head(20).to_string()}"
        elif isinstance(result, pd.Series):
            return f"Series with {len(result)} values:\n{result.head(20).to_string()}"
        elif isinstance(result, (int, float, str)):
            return f"Single value: {result}"
        else:
            return str(result)

    def execute_rag_query(self, query: str) -> Dict[str, Any]:
        """Execute a RAG query using vector store."""
        logger.info(f"Executing RAG query: {query}")

        if not self.vector_store:
            return {
                'success': False,
                'error': 'Vector store not available',
                'query_type': 'rag'
            }

        try:
            # Search vector store
            results = self.vector_store.search(query, n_results=5)

            # Build context
            context_parts = ["# Relevant Data Context\n"]
            for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas']), 1):
                context_parts.append(f"\n## Context {i}")
                context_parts.append(f"Source: {metadata.get('file', 'unknown')} - {metadata.get('sheet', 'unknown')}")
                context_parts.append(f"Content:\n{doc}\n")

            context = "\n".join(context_parts)

            # Generate response
            rag_prompt = f"""Answer this question using the provided context from Excel files.

Context:
{context}

Question: {query}

Provide a comprehensive answer that:
1. Uses information from the context
2. Is accurate and specific
3. Uses proper formatting
4. Cites sources when relevant"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                system="You are an expert data analyst specializing in actuarial data.",
                messages=[{"role": "user", "content": rag_prompt}]
            )

            answer = response.content[0].text

            return {
                'success': True,
                'answer': answer,
                'context': context,
                'query_type': 'rag'
            }

        except Exception as e:
            logger.error(f"RAG query error: {e}")
            return {
                'success': False,
                'error': str(e),
                'query_type': 'rag'
            }

    def query(self, user_query: str) -> Dict[str, Any]:
        """
        Main query method that routes to appropriate handler.

        Returns:
            Dict with query results and metadata
        """
        logger.info(f"Processing query: {user_query}")

        # Classify query
        query_type, reasoning = self.classify_query(user_query)

        logger.info(f"Query type: {query_type}, Reasoning: {reasoning}")

        # Route to appropriate handler
        if query_type == 'structured':
            result = self.execute_structured_query(user_query)
        elif query_type == 'rag':
            result = self.execute_rag_query(user_query)
        else:  # hybrid
            # Execute structured first, then use RAG for analysis
            structured_result = self.execute_structured_query(user_query)
            if structured_result['success']:
                # Use structured data as context for RAG
                rag_result = self.execute_rag_query(
                    f"{user_query}\n\nStructured data result:\n{self._summarize_result(structured_result['data'])}"
                )
                result = {
                    'success': True,
                    'structured': structured_result,
                    'rag': rag_result,
                    'query_type': 'hybrid'
                }
            else:
                result = structured_result

        result['classification'] = {
            'type': query_type,
            'reasoning': reasoning
        }

        return result


if __name__ == "__main__":
    # Test the hybrid engine
    from data_loader import ExcelDataLoader

    print("Loading data...")
    loader = ExcelDataLoader([
        "actuarial_life_data_file1.xlsx",
        "actuarial_life_data_file2.xlsx"
    ])

    dataframes = loader.load_all_data()

    print("Initializing hybrid engine...")
    engine = HybridQueryEngine(dataframes)

    # Test queries
    test_queries = [
        "Give me all details of policy ID P00225",
        "What is the average premium for policies in class Micro?",
        "What data is available in these files?",
    ]

    for query in test_queries:
        print("\n" + "="*70)
        print(f"Query: {query}")
        print("="*70)

        result = engine.query(query)

        print(f"Type: {result.get('classification', {}).get('type', 'unknown')}")

        if result.get('success'):
            if result.get('query_type') == 'structured':
                print(f"\nExplanation:\n{result.get('explanation', 'N/A')}")
            elif result.get('query_type') == 'rag':
                print(f"\nAnswer:\n{result.get('answer', 'N/A')}")
        else:
            print(f"\nError: {result.get('error', 'Unknown error')}")
