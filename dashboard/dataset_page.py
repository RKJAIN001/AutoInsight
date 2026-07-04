import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))

from file_handler import get_dataset_summary
from data_cleaner import get_missing_summary, clean_dataset
import pandas as pd

def render():
    st.markdown('<div class="section-header">Dataset View</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Inspect column types, check data quality, and clean missing values.</div>', unsafe_allow_html=True)

    if "df" not in st.session_state or st.session_state.df is None:
        st.markdown("""
            <div class="empty-state-card">
                <div class="empty-state-icon">📊</div>
                <div class="empty-state-title">No dataset loaded</div>
                <div class="empty-state-desc">Go to the <b>Upload</b> tab in the sidebar to add or load a dataset first.</div>
            </div>
        """, unsafe_allow_html=True)
        return

    df = st.session_state.df
    summary = get_dataset_summary(df)

    st.markdown('<div class="section-header">Column Details</div>', unsafe_allow_html=True)
    col_info = pd.DataFrame({
        "Column": summary["columns"],
        "Type": [summary["dtypes"][c] for c in summary["columns"]],
        "Missing": [summary["missing_values"][c] for c in summary["columns"]]
    })
    st.dataframe(col_info, width='stretch')

    st.markdown('<div class="section-header">Data Quality</div>', unsafe_allow_html=True)
    missing_report = get_missing_summary(df)

    if missing_report:
        st.markdown('<div class="section-caption">Missing values detected — choose how to fill them below.</div>', unsafe_allow_html=True)
        for item in missing_report:
            st.markdown(f"""
                <div class="kpi-card" style="padding: 0.7rem 1rem; margin-bottom: 0.5rem;">
                    <span style="color:#D97A3F;">⚠</span>
                    <b>{item['column']}</b> ({item['type']}) — {item['missing_count']} missing ({item['missing_pct']}%)
                </div>
            """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            numeric_strategy = st.selectbox("Fill numeric columns using:", ["mean", "median"])
        with col_b:
            st.write("")
            st.write("Text columns will be filled with their most frequent value.")

        if st.button("Clean Dataset"):
            with st.spinner("Cleaning dataset..."):
                cleaned_df, clean_log = clean_dataset(df, numeric_strategy=numeric_strategy)
                st.session_state.df = cleaned_df
            st.toast("Dataset cleaned successfully", icon="🧹")
            for entry in clean_log:
                st.write(f"✓ {entry}")
            st.rerun()
    else:
        st.markdown("""
            <div class="empty-state-card" style="padding: 2rem 1.5rem;">
                <div class="empty-state-icon">✅</div>
                <div class="empty-state-title">No missing values detected</div>
                <div class="empty-state-desc">This dataset is already clean.</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Preview</div>', unsafe_allow_html=True)
    show_full = st.toggle("Show full dataset")
    if show_full:
        st.dataframe(df, width='stretch')
    else:
        st.dataframe(df.head(10), width='stretch')