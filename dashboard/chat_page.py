import streamlit as st
import sys, os
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))

from llm_chat import ask_question
from database import get_user_files

def render():
    st.markdown('<div class="section-header">Ask About Your Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Ask a question in plain English — answers are computed from real pandas operations, never guessed.</div>', unsafe_allow_html=True)

    user_files = get_user_files(st.session_state.user_id)

    if not user_files:
        st.markdown("""
            <div class="empty-state-card">
                <div class="empty-state-icon">💬</div>
                <div class="empty-state-title">No datasets to chat with</div>
                <div class="empty-state-desc">Go to the <b>Upload</b> tab in the sidebar to add a dataset first.</div>
            </div>
        """, unsafe_allow_html=True)
        return

    file_options = {filename: (file_id, filepath) for file_id, filename, filepath, _ in user_files}
    filenames = list(file_options.keys())

    current_active = st.session_state.get("uploaded_filename")
    default_index = filenames.index(current_active) if current_active in filenames else 0

    selected_filename = st.selectbox("Choose a dataset to chat with:", filenames, index=default_index)

    if selected_filename != st.session_state.get("chat_active_filename"):
        file_id, filepath = file_options[selected_filename]
        if os.path.exists(filepath):
            with st.spinner("Loading dataset..."):
                st.session_state.chat_df = pd.read_csv(filepath)
                st.session_state.chat_active_filename = selected_filename
                st.session_state.chat_history = []
        else:
            st.error(f"'{selected_filename}' could not be found on disk.")
            return

    df = st.session_state.chat_df
    st.caption(f"Currently chatting with: **{selected_filename}** ({len(df):,} rows, {len(df.columns)} columns)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if not st.session_state.chat_history:
        st.markdown("""
            <div class="empty-state-card" style="padding: 2rem 1.5rem;">
                <div class="empty-state-icon">✨</div>
                <div class="empty-state-title">Ask your first question</div>
                <div class="empty-state-desc">Try something like "what's the average value in [column]?" or "which category appears most often?"</div>
            </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_question = st.chat_input("Ask a question about your data...")

    if user_question:
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = ask_question(user_question, df)

            st.write(result["answer"])

            if result["success"] and result["result"] is not None:
                if isinstance(result["result"], (pd.Series, pd.DataFrame)):
                    st.dataframe(result["result"], width='stretch')
                with st.expander("How this was calculated"):
                    st.code(result["expression"], language="python")

        st.session_state.chat_history.append({"role": "assistant", "content": result["answer"]})