import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))

from file_handler import load_dataset, get_dataset_summary
from database import save_user_file_record, get_user_files, delete_user_file
import pandas as pd

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "uploads")

def render():
    st.markdown('<div class="section-header">Upload Your Dataset</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Add a new CSV or Excel file, or reload one you\'ve already saved.</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        if st.session_state.get("uploaded_filename") != uploaded_file.name:
            with st.spinner("Reading and saving your file..."):
                df = load_dataset(uploaded_file)
                st.session_state.df = df
                st.session_state.uploaded_filename = uploaded_file.name
                st.session_state.chat_history = []
                st.session_state.pop("insights", None)
                st.session_state.pop("charts", None)
                st.session_state.pop("report_buffer", None)

                user_folder = os.path.join(UPLOAD_DIR, str(st.session_state.user_id))
                os.makedirs(user_folder, exist_ok=True)
                filepath = os.path.join(user_folder, uploaded_file.name)
                df.to_csv(filepath, index=False)

                save_user_file_record(st.session_state.user_id, uploaded_file.name, filepath)

            st.toast(f"'{uploaded_file.name}' uploaded successfully", icon="✅")

    if "df" in st.session_state and st.session_state.df is not None:
        df = st.session_state.df
        summary = get_dataset_summary(df)

        st.markdown(f'<div class="section-header">Active Dataset: {st.session_state.get("uploaded_filename", "")}</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Rows</div><div class="kpi-value">{summary['num_rows']:,}</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Columns</div><div class="kpi-value">{summary['num_columns']}</div></div>""", unsafe_allow_html=True)
        with col3:
            missing_total = sum(summary['missing_values'].values())
            st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Missing Values</div><div class="kpi-value-accent">{missing_total}</div></div>""", unsafe_allow_html=True)

        st.info("Go to **Dataset View** in the sidebar to explore columns, preview data, and clean it.")

    st.markdown('<div class="section-header">Your Files</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Every dataset you\'ve uploaded is saved to your account.</div>', unsafe_allow_html=True)

    user_files = get_user_files(st.session_state.user_id)

    if not user_files:
        st.markdown("""
            <div class="empty-state-card">
                <div class="empty-state-icon">📭</div>
                <div class="empty-state-title">No files yet</div>
                <div class="empty-state-desc">Upload a CSV or Excel file above to get started — it'll show up here every time you log in.</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for file_id, filename, filepath, uploaded_at in user_files:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                with col1:
                    st.write(f"**{filename}**")
                with col2:
                    st.write(f"Uploaded: {uploaded_at[:16].replace('T', ' ')}")
                with col3:
                    if st.button("Load", key=f"load_{file_id}"):
                        if os.path.exists(filepath):
                            with st.spinner("Loading dataset..."):
                                df = pd.read_csv(filepath)
                                st.session_state.df = df
                                st.session_state.uploaded_filename = filename
                                st.session_state.chat_history = []
                                st.session_state.pop("insights", None)
                                st.session_state.pop("charts", None)
                                st.session_state.pop("report_buffer", None)
                            st.toast(f"Loaded '{filename}'", icon="📂")
                            st.rerun()
                        else:
                            st.error("File not found on disk. It may have been moved or deleted.")
                with col4:
                    delete_key = f"confirm_delete_{file_id}"
                    if st.session_state.get(delete_key):
                        if st.button("Confirm", key=f"confirm_btn_{file_id}", type="primary"):
                            success, msg = delete_user_file(file_id, st.session_state.user_id)
                            if success:
                                if st.session_state.get("uploaded_filename") == filename:
                                    st.session_state.df = None
                                    st.session_state.uploaded_filename = None
                                    st.session_state.chat_history = []
                                    st.session_state.pop("insights", None)
                                    st.session_state.pop("charts", None)
                                st.toast(msg, icon="🗑️")
                                st.session_state.pop(delete_key, None)
                                st.rerun()
                            else:
                                st.error(msg)
                    else:
                        if st.button("Delete", key=f"delete_{file_id}"):
                            st.session_state[delete_key] = True
                            st.rerun()