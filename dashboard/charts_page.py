import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))

from auto_eda import generate_auto_charts, generate_text_insights
from custom_plot import build_custom_plot, PLOT_TYPES
from theme import get_chart_colors

def render():
    st.markdown('<div class="section-header">Charts & Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Automatically generated visualizations, plus a builder for your own custom charts.</div>', unsafe_allow_html=True)

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
    chart_colors = get_chart_colors(st.session_state.theme_mode)

    with st.spinner("Generating insights..."):
        insights = generate_text_insights(df)
        st.session_state.insights = insights

    st.markdown('<div class="section-header">Automatic Insights</div>', unsafe_allow_html=True)
    for insight in insights:
        st.markdown(f"""
            <div class="kpi-card" style="padding: 0.7rem 1rem; margin-bottom: 0.5rem;">
                <span style="color:#D97A3F;">▸</span>
                {insight}
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Auto-Generated Charts</div>', unsafe_allow_html=True)
    with st.spinner("Building charts..."):
        charts = generate_auto_charts(df, chart_colors)
        st.session_state.charts = charts

    for i in range(0, len(charts), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(charts):
                title, fig = charts[i + j]
                with col:
                    with st.container(border=True):
                        st.plotly_chart(fig, width='stretch')

    st.markdown('<div class="landing-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Build Your Own Chart</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Pick a chart type and the columns you want to visualize.</div>', unsafe_allow_html=True)

    all_columns = list(df.columns)

    col1, col2 = st.columns(2)
    with col1:
        plot_type = st.selectbox("Chart type", PLOT_TYPES)
    with col2:
        color_col = st.selectbox("Color by (optional)", ["None"] + all_columns)
        color_col = None if color_col == "None" else color_col

    col3, col4 = st.columns(2)
    x_col = None
    y_col = None

    with col3:
        if plot_type in ["Bar", "Line", "Scatter", "Histogram", "Pie"]:
            x_col = st.selectbox("X-axis / Category column", all_columns, key="x_col_select")
        elif plot_type == "Box":
            x_col = st.selectbox("X-axis / Group column (optional)", ["None"] + all_columns, key="x_col_select_box")
            x_col = None if x_col == "None" else x_col

    with col4:
        if plot_type in ["Bar", "Line", "Scatter", "Box"]:
            y_col = st.selectbox("Y-axis column (numeric)", all_columns, key="y_col_select")

    if st.button("Generate Custom Chart"):
        with st.spinner("Building your chart..."):
            fig, error = build_custom_plot(df, plot_type, x_col=x_col, y_col=y_col, color_col=color_col, chart_colors=chart_colors)

        if error:
            st.error(error)
        else:
            st.toast("Chart generated", icon="📊")
            with st.container(border=True):
                st.plotly_chart(fig, width='stretch')