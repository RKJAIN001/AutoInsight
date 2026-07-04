from google import genai
from dotenv import load_dotenv
import os
import pandas as pd
import re

import streamlit as st

load_dotenv()

def _get_api_key():
    # Try Streamlit Cloud's secrets manager first (used in deployment),
    # fall back to .env (used for local development)
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return os.getenv("GEMINI_API_KEY")

_client = genai.Client(api_key=_get_api_key())

# Keywords that should never appear in generated code - defense in depth
# on top of the restricted execution namespace below.
FORBIDDEN_KEYWORDS = ["import", "open(", "exec(", "eval(", "__", "os.", "sys.", "subprocess", "input("]

def _build_schema_context(df):
    """Describes the dataset's structure to the LLM, without sending all the raw data."""
    dtypes_str = ", ".join(f"{col} ({dtype})" for col, dtype in df.dtypes.items())
    sample_rows = df.head(3).to_string(index=False)
    return f"""
Dataset columns and types: {dtypes_str}
Total rows: {len(df)}
Sample data (first 3 rows):
{sample_rows}
"""

def _generate_pandas_expression(question, df):
    """Asks Gemini to translate a natural-language question into ONE pandas expression."""
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

    response = _client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    expression = response.text.strip()
    # Strip markdown code fences if Gemini adds them despite instructions
    expression = re.sub(r"^```(python)?|```$", "", expression, flags=re.MULTILINE).strip()
    return expression

def _safe_eval(expression, df):
    """
    Executes the pandas expression in a locked-down namespace.
    Only `df` and `pd` are available - no builtins, no imports, no file/system access.
    """
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in expression:
            raise ValueError(f"Generated expression contains a disallowed operation: '{keyword}'")

    safe_globals = {"__builtins__": {}}
    safe_locals = {"df": df, "pd": pd}

    result = eval(expression, safe_globals, safe_locals)
    return result

def _explain_result(question, expression, result):
    """Asks Gemini to turn the raw computed result into a natural-language answer."""
    prompt = f"""The user asked: "{question}"
We computed this using the expression: {expression}
The result was: {result}

Write a short, clear, one-to-two sentence natural-language answer to the user's question based on this result.
Don't mention the code or expression - just answer naturally, like a data analyst would."""

    response = _client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )
    return response.text.strip()

def ask_question(question, df):
    """
    Main entry point: takes a natural-language question and the dataframe,
    returns a dict with the answer, the underlying result, and the expression used
    (for transparency - useful for the report/debugging).
    """
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