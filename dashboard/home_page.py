import streamlit as st
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
from database import get_user_files

def render():
    user_files = get_user_files(st.session_state.user_id)
    file_count = len(user_files)
    has_active_dataset = "df" in st.session_state and st.session_state.df is not None

    st.markdown(f"""
        <div class="hero-section" style="padding: 2.5rem 1rem 2rem 1rem;">
            <div class="hero-glow"></div>
            <div class="hero-badge">👋 WELCOME BACK</div>
            <div class="hero-title" style="font-size:2.3rem;">{st.session_state.username}</div>
            <div class="hero-subtitle" style="font-size:1rem;">
                Your data workspace — upload a file, explore insights, and pick up right where you left off.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Files Uploaded</div>
                <div class="kpi-value">{file_count}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        active_name = st.session_state.get("uploaded_filename", "None") if has_active_dataset else "None"
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Active Dataset</div>
                <div class="kpi-value" style="font-size:1.1rem;">{active_name}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        chat_count = len(st.session_state.get("chat_history", []))
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Questions Asked</div>
                <div class="kpi-value-accent">{chat_count // 2 if chat_count else 0}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="landing-divider"></div>', unsafe_allow_html=True)

    if not has_active_dataset:
        st.markdown('<div class="section-header">Get Started</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="empty-state-card">
                <div class="empty-state-icon">📁</div>
                <div class="empty-state-title">No active dataset yet</div>
                <div class="empty-state-desc">Head to the <b>Upload</b> tab in the sidebar to add a new file, or reload one of your saved datasets.</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-header">Continue Working</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-caption">Jump back into your active dataset.</div>', unsafe_allow_html=True)
        continue_cards = [
            ("🔍", "Dataset View", "Inspect columns, preview rows, and clean missing values."),
            ("📊", "Charts", "See auto-generated visualizations for your current dataset."),
            ("💬", "Chatbot", "Ask a question in plain English about your data."),
        ]
        cols = st.columns(3)
        for col, (icon, title, desc) in zip(cols, continue_cards):
            with col:
                st.markdown(f"""
                    <div class="feature-grid-card">
                        <div class="feature-icon">{icon}</div>
                        <div class="feature-title">{title}</div>
                        <div class="feature-desc">{desc}</div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown('<div class="landing-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">What You Can Do Here</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">A quick reminder of everything AutoInsight offers.</div>', unsafe_allow_html=True)

    features = [
        ("📁", "Upload Anything", "CSV or Excel, any structure — read instantly, no configuration needed."),
        ("🧹", "Auto-Clean Data", "Missing values filled automatically — mean/median for numbers, most frequent for text."),
        ("📊", "Instant Charts", "Relevant charts generated automatically based on your data's actual structure."),
        ("💬", "Chat With Your Data", "Ask questions in plain English, get answers computed from real pandas operations."),
        ("📄", "Export Reports", "Download a complete Word or PDF report of your analysis and conversation."),
        ("🔒", "Private Storage", "Every file is saved securely to your account alone."),
    ]

    rows = [features[i:i+3] for i in range(0, len(features), 3)]
    for row in rows:
        cols = st.columns(len(row))
        for col, (icon, title, desc) in zip(cols, row):
            with col:
                st.markdown(f"""
                    <div class="feature-grid-card">
                        <div class="feature-icon">{icon}</div>
                        <div class="feature-title">{title}</div>
                        <div class="feature-desc">{desc}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.write("")