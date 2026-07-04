# 📊 AutoInsight

**Upload any dataset. Get instant insight.**

AutoInsight is a full-stack data analysis platform that lets anyone — no coding or data science background required — upload a CSV or Excel file and instantly receive automated visualizations, plain-English insights, an AI chatbot to query their data in natural language, and a downloadable analysis report.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [How the AI Chatbot Works](#how-the-ai-chatbot-works)
- [Security Notes](#security-notes)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Overview

Most people who need answers from data don't know SQL, Python, or how to build a multi-level pivot table in Excel — they just have a spreadsheet and a question. AutoInsight closes that gap: upload a file, and get the kind of first-pass analysis a data analyst would hand you, in seconds instead of days.

Every user has their own account, and every dataset they upload is saved privately to that account — so you can log out, come back later, and pick up exactly where you left off.

---

## Features

### 🔐 Authentication
- Secure signup/login with **bcrypt** password hashing (passwords are never stored in plain text)
- Per-user session management via Streamlit's session state

### 📁 Data Upload & Storage
- Supports both **CSV** and **Excel** (`.xlsx`, `.xls`) files
- Automatic encoding detection (UTF-8, Latin-1, CP1252, ISO-8859-1) — handles messy real-world files that aren't clean UTF-8
- Every upload is saved to disk under the user's own account, with metadata tracked in SQLite
- Users can **reload** or **delete** any previously uploaded file from their dashboard

### 🧹 Automatic Data Cleaning
- Detects missing values per column and reports type, count, and percentage missing
- One-click cleaning: numeric columns filled with **mean or median** (user's choice), categorical columns filled with the **most frequent value**
- Full transparency log of exactly what was changed and how

### 📊 Automated Insights & Charts
- Inspects each column's data type and cardinality at runtime to decide what's worth visualizing — no hardcoded assumptions about any particular dataset
- Generates distribution histograms, category breakdowns, and grouped comparisons automatically
- Produces plain-English textual insights (ranges, averages, most common values, missing data summary)

### 🎨 Custom Chart Builder
- Users can manually choose a chart type (Bar, Line, Scatter, Histogram, Box, Pie) and the exact columns to plot
- Input validation prevents invalid column/chart-type combinations with clear error messaging

### 💬 AI Chatbot (Google Gemini)
- Ask questions about your data in plain English
- Uses a **two-step LLM flow**: Gemini translates the question into a single pandas expression → the expression is executed safely against the real dataset → Gemini rephrases the actual computed result into natural language
- This means answers are always grounded in real computation, not hallucinated by the LLM
- Full expression transparency — every answer includes an expandable "How this was calculated" section showing the exact code that ran
- Users can switch between any of their saved datasets directly from the chat interface

### 📄 Report Export
- Generates a complete analysis report — not a screenshot — containing dataset overview, insights, embedded charts, and full chat history
- Available in both **Word (.docx)** and **PDF** formats

### 🎨 UI/UX
- Custom dark/light theme system (black-and-copper dark mode by default)
- Fully custom CSS styling — no default Streamlit look
- Toast notifications, empty states, loading spinners, and page-transition animations for a polished feel
- Persistent, non-collapsible sidebar navigation

---

## Tech Stack

| Layer | Technology |
|---|---|
| App framework | [Streamlit](https://streamlit.io/) |
| Language | Python 3.13 |
| Data processing | pandas, NumPy |
| Visualization | Plotly |
| Database | SQLite |
| Authentication | bcrypt |
| AI / LLM | Google Gemini API (`google-genai`) |
| Report generation | python-docx (Word), reportlab (PDF), kaleido (chart-to-image) |
| Config management | python-dotenv |

---

## Architecture

```
Upload (CSV/Excel)
        │
        ▼
File Handler (encoding-safe read) ──► Saved to disk + SQLite (per user)
        │
        ▼
Data Cleaner (missing value detection + fill)
        │
        ▼
Auto-EDA Engine (column classification → chart/insight generation)
        │
        ├──► Custom Plot Builder (user-selected columns/chart type)
        │
        ├──► LLM Chat (question → pandas expression → safe execution → natural-language answer)
        │
        └──► Report Generator (Word / PDF export)
```

### The Chatbot's Safety Model
The chatbot never lets the LLM execute arbitrary code or invent numbers:
1. Gemini receives the dataset's schema (column names/types + a small sample) and the user's question
2. Gemini returns **one pandas expression**, not a script
3. The expression is checked against a blocklist of dangerous keywords (`import`, `open(`, `exec(`, `__`, etc.)
4. It's evaluated using Python's `eval()` with `__builtins__` stripped out entirely — so even if a dangerous keyword slipped through, the underlying functions don't exist in that execution context
5. The **real, computed result** is sent back to Gemini, which only rephrases it into natural language

---

## Project Structure

```
AutoInsight/
├── main.py                    # Router: theme, auth gate, sidebar navigation
├── requirements.txt
├── .env                        # API keys (not committed)
├── .gitignore
│
├── core/
│   ├── database.py             # User auth + file metadata (SQLite)
│   ├── file_handler.py         # CSV/Excel loading with encoding fallback
│   ├── data_cleaner.py         # Missing value detection + cleaning
│   ├── auto_eda.py             # Automatic chart/insight generation
│   ├── custom_plot.py          # User-driven chart builder
│   ├── llm_chat.py             # Gemini integration + safe code execution
│   └── report_generator.py     # Word (.docx) and PDF report builders
│
├── dashboard/
│   ├── landing_page.py         # Public marketing/landing page
│   ├── auth_page.py            # Login / signup forms
│   ├── home_page.py            # Logged-in dashboard home
│   ├── upload_page.py          # File upload + saved files list
│   ├── dataset_page.py         # Column details, data quality, cleaning
│   ├── charts_page.py          # Auto charts + custom chart builder
│   ├── chat_page.py            # AI chatbot interface
│   └── report_page.py          # Report generation + download
│
├── assets/styles/
│   └── theme.py                 # CSS theme system (light/dark mode)
│
├── database/                    # SQLite .db file (not committed)
└── data/uploads/{user_id}/      # Per-user uploaded files (not committed)
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- A free [Google AI Studio](https://aistudio.google.com) account for a Gemini API key

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/AutoInsight.git
cd AutoInsight

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Configure your API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Run the app
```bash
streamlit run main.py
```
The app will open in your browser at `http://localhost:8501`.

---

## Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API key, used to power the AI chatbot feature |

---

## Security Notes
- Passwords are hashed with **bcrypt** before storage — never stored or logged in plain text
- The `.env` file (API keys) and `database/*.db` (user data) are excluded from version control via `.gitignore`
- File deletion is scoped to `user_id`, preventing any user from accessing or deleting another user's data
- Chatbot code execution is sandboxed (see [Architecture](#the-chatbots-safety-model) above) to prevent arbitrary code execution

---

## Known Limitations
- The chatbot's accuracy depends on Gemini generating valid pandas syntax; highly complex, multi-step questions may occasionally fail gracefully with an error message rather than a wrong answer
- Auto-chart selection is rule-based (by column dtype/cardinality), not itself machine-learned — a deliberate choice favoring reliability and explainability
- Designed as a single-instance local/demo app; not configured for multi-instance concurrent deployment out of the box
- No password reset flow (out of scope for this project's intended use)

## Future Improvements
- Password reset / email verification
- Support for additional file formats (JSON, Parquet)
- Chart export as standalone image files
- Scheduled/recurring report generation

---

## License
This project is available for personal and educational use.