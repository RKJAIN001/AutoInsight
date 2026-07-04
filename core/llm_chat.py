from google import genai
from dotenv import load_dotenv
import os
import pandas as pd
import re

load_dotenv()

FORBIDDEN_KEYWORDS = ["import", "open(", "exec(", "eval(", "__", "os.", "sys.", "subprocess", "input("]

_client = None  # created lazily on first use, not at import time

def _get_api_key():
    """
    Tries Streamlit Cloud's secrets manager first (used in deployment),
    falls back to .env (used for local development).
    Broad exception handling since st.secrets can raise different
    exception types depending on environment/version.
    """
    try:
        import streamlit as st
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY")

def _get_client():
    """Creates the Gemini client on first use, not at import time -
    so a missing key fails gracefully inside a chat request instead of
    crashing the whole app on page load."""
    global _client
    if _client is None:
        api_key = _get_api_key()
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Set it in your .env file (local) "
                "or in Streamlit Cloud's Secrets settings (deployed)."
            )
        _client = genai.Client(api_key=api_key)
    return _client

def _build_schema_context(df):
    dtypes_str = ", ".join(f"{col} ({dtype})" for col, dtype in df.dtypes.items())
    sample_rows = df.head(3).to_string(index=False)
    return f"""
Dataset columns and types: {dtypes_str}
Total rows: {len(df)}
Sample data (first 3 rows):
{sample_rows}
"""

def _generate_pandas_expression(question, df):
    client = _get_client()
    schema = _build_schema_context(df)

    prompt = f"""You are a data analyst assistant. Given a pandas DataFrame called `df` with this structure:

{schema}

Write a SINGLE Python expression (not a statement, not multiple lines) that uses `df` to answer this question:
"{question}"

Rules:
- Return ONLY the raw expression, no explanation, no markdown code fences, no variable assignment.
- The expression must be valid to pass directly to Python's eval().
- Use only pandas/standard operations on `df`. No imports, no file access.
- If the question asks for a chart or visualization, still return a pandas expression that produces the underlying data (e.g. a grouped Series or DataFrame) rather than trying to draw the chart yourself.

Expression:"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    expression = response.text.strip()
    expression = re.sub(r"^```(python)?|```$", "", expression, flags=re.MULTILINE).strip()
    return expression

def _safe_eval(expression, df):
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in expression:
            raise ValueError(f"Generated expression contains a disallowed operation: '{keyword}'")

    safe_globals = {"__builtins__": {}}
    safe_locals = {"df": df, "pd": pd}

    result = eval(expression, safe_globals, safe_locals)
    return result

def _explain_result(question, expression, result):
    client = _get_client()
    prompt = f"""The user asked: "{question}"
We computed this using the expression: {expression}
The result was: {result}

Write a short, clear, one-to-two sentence natural-language answer to the user's question based on this result.
Don't mention the code or expression - just answer naturally, like a data analyst would."""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    return response.text.strip()

def ask_question(question, df):
    try:
        expression = _generate_pandas_expression(question, df)
        result = _safe_eval(expression, df)
        answer = _explain_result(question, expression, result)

        return {
            "success": True,
            "answer": answer,
            "expression": expression,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "answer": f"I couldn't process that question. Error: {str(e)}",
            "expression": None,
            "result": None
        }