import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))

from file_handler import get_dataset_summary
from report_generator import generate_report, generate_pdf_report

def render():
    st.markdown('<div class="section-header">Download Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Export a complete summary of your analysis as a Word or PDF document.</div>', unsafe_allow_html=True)

    if "df" not in st.session_state or st.session_state.df is None:
        st.markdown("""
            <div class="empty-state-card">
                <div class="empty-state-icon">📄</div>
                <div class="empty-state-title">No dataset loaded</div>
                <div class="empty-state-desc">Go to the <b>Upload</b> tab in the sidebar to add or load a dataset first.</div>
            </div>
        """, unsafe_allow_html=True)
        return

    df = st.session_state.df
    summary = get_dataset_summary(df)

    if "insights" not in st.session_state or "charts" not in st.session_state:
        from auto_eda import generate_auto_charts, generate_text_insights
        from theme import get_chart_colors
        with st.spinner("Preparing report data..."):
            st.session_state.insights = generate_text_insights(df)
            chart_colors = get_chart_colors(st.session_state.theme_mode)
            st.session_state.charts = generate_auto_charts(df, chart_colors)

    report_format = st.radio("Choose report format:", ["Word (.docx)", "PDF (.pdf)"], horizontal=True)

    if st.button("Generate Report"):
        with st.spinner("Building your report..."):
            if report_format == "Word (.docx)":
                buffer = generate_report(
                    df=df,
                    summary=summary,
                    insights=st.session_state.insights,
                    charts=st.session_state.charts,
                    chat_history=st.session_state.get("chat_history", []),
                    filename=st.session_state.get("uploaded_filename", "dataset")
                )
                st.session_state.report_buffer = buffer
                st.session_state.report_mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                st.session_state.report_ext = "docx"
            else:
                buffer = generate_pdf_report(
                    df=df,
                    summary=summary,
                    insights=st.session_state.insights,
                    charts=st.session_state.charts,
                    chat_history=st.session_state.get("chat_history", []),
                    filename=st.session_state.get("uploaded_filename", "dataset")
                )
                st.session_state.report_buffer = buffer
                st.session_state.report_mime = "application/pdf"
                st.session_state.report_ext = "pdf"
        st.toast("Report ready to download", icon="📄")

    if "report_buffer" in st.session_state:
        filename_base = st.session_state.get("uploaded_filename", "dataset").split(".")[0]
        st.download_button(
            label=f"Download Report (.{st.session_state.report_ext})",
            data=st.session_state.report_buffer,
            file_name=f"AutoInsight_Report_{filename_base}.{st.session_state.report_ext}",
            mime=st.session_state.report_mime
        )