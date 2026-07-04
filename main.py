import streamlit as st
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "assets", "styles"))
sys.path.append(os.path.join(os.path.dirname(__file__), "dashboard"))

from theme import get_theme_css
from database import init_database

init_database()

st.set_page_config(
    page_title="AutoInsight",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "view" not in st.session_state:
    st.session_state.view = "landing"

st.markdown(get_theme_css(st.session_state.theme_mode), unsafe_allow_html=True)

# ===== NOT LOGGED IN: landing page or auth page =====
if not st.session_state.logged_in:
    if st.session_state.view == "landing":
        import landing_page
        landing_page.render()
    else:
        import auth_page
        auth_page.render()
    st.stop()

# ===== LOGGED IN: sidebar navigation + pages =====
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <span class="sidebar-brand-icon">📊</span>
            <span class="sidebar-brand-name">Auto<span style="color:inherit;">Insight</span></span>
        </div>
    """, unsafe_allow_html=True)

    user_initial = st.session_state.username[0].upper() if st.session_state.username else "?"
    st.markdown(f"""
        <div class="sidebar-user-box">
            <div class="sidebar-user-avatar">{user_initial}</div>
            <div>
                <div class="sidebar-user-name">{st.session_state.username}</div>
                <div class="sidebar-user-label">Logged in</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-nav-label">Navigate</div>', unsafe_allow_html=True)

    page_options = {
        "Home": "🏠  Home",
        "Upload": "📁  Upload",
        "Dataset View": "🔍  Dataset View",
        "Charts": "📊  Charts",
        "Chatbot": "💬  Chatbot",
        "Reports": "📄  Reports",
    }
    page_label = st.radio(
        "Navigate",
        list(page_options.values()),
        label_visibility="collapsed"
    )
    page = [k for k, v in page_options.items() if v == page_label][0]

    st.markdown('<div style="flex-grow:1; min-height:8vh;"></div>', unsafe_allow_html=True)

    st.divider()
    if st.button("Log Out", width='stretch'):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.df = None
        st.session_state.view = "landing"
        st.rerun()

    st.markdown('<div class="theme-toggle-box">', unsafe_allow_html=True)
    st.toggle(
        "Light mode",
        value=(st.session_state.theme_mode == "light"),
        key="theme_toggle_widget",
        on_change=lambda: st.session_state.update(
            theme_mode="light" if st.session_state.theme_toggle_widget else "dark"
        )
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ===== PAGE ROUTING =====
if page == "Home":
    import home_page
    home_page.render()
elif page == "Upload":
    import upload_page
    upload_page.render()
elif page == "Dataset View":
    import dataset_page
    dataset_page.render()
elif page == "Charts":
    import charts_page
    charts_page.render()
elif page == "Chatbot":
    import chat_page
    chat_page.render()
elif page == "Reports":
    import report_page
    report_page.render()