import streamlit as st

def render():
    # ===== TOP NAVBAR =====
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([3, 1, 1, 1])
    with nav_col1:
        st.markdown("""
            <div class="top-navbar-brand">📊 Auto<span>Insight</span></div>
        """, unsafe_allow_html=True)
    with nav_col3:
        if st.button("Log In", key="nav_login", width='stretch'):
            st.session_state.view = "auth"
            st.session_state.auth_tab = "Login"
            st.rerun()
    with nav_col4:
        if st.button("Sign Up", key="nav_signup", width='stretch'):
            st.session_state.view = "auth"
            st.session_state.auth_tab = "Sign Up"
            st.rerun()

    st.markdown('<div style="border-bottom:1px solid rgba(128,128,128,0.2); margin-bottom:0.5rem;"></div>', unsafe_allow_html=True)

    # ===== HERO SECTION =====
    st.markdown("""
        <div class="hero-section">
            <div class="hero-glow"></div>
            <div class="hero-badge">⚡ AI-POWERED DATA ANALYSIS</div>
            <div class="hero-title">Turn Data Into <span>Insight</span>, Instantly</div>
            <div class="hero-subtitle">
                Upload any dataset and get automated charts, plain-English insights,
                a chatbot that answers real questions about your data, and a downloadable
                report — no code, no setup, no data science degree required.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.3, 1, 1.3])
    with col2:
        if st.button("Get Started →", key="hero_cta", width='stretch'):
            st.session_state.view = "auth"
            st.session_state.auth_tab = "Sign Up"
            st.rerun()

    st.markdown('<div class="landing-divider"></div>', unsafe_allow_html=True)

    # ===== STATS ROW =====
    stats = [
        ("< 30 sec", "From upload to first insight"),
        ("Any format", "CSV or Excel, any structure"),
        ("0", "Lines of code required"),
        ("100%", "Your data stays in your account"),
    ]
    cols = st.columns(4)
    for col, (number, label) in zip(cols, stats):
        with col:
            st.markdown(f"""
                <div style="text-align:center;">
                    <div style="font-size:1.8rem; font-weight:800; color:var(--accent, #D97A3F);" class="hero-title-mini">{number}</div>
                    <div class="feature-desc">{label}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="landing-divider"></div>', unsafe_allow_html=True)

    # ===== THE PROBLEM =====
    st.markdown('<div class="section-header" style="text-align:center;">Why AutoInsight</div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="max-width:720px; margin:0 auto; text-align:center;" class="feature-desc">
            Most people who need answers from data don't know SQL, Python, or how to build a pivot table
            three levels deep in Excel. They just have a spreadsheet and a question. AutoInsight closes that gap —
            upload your file, and get the analysis a data analyst would hand you, in seconds instead of days.
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ===== FEATURES (expanded descriptions) =====
    st.markdown('<div class="section-header" style="text-align:center;">Everything You Need, In One Place</div>', unsafe_allow_html=True)

    features = [
        ("📁", "Upload Anything",
         "Drop in a CSV or Excel file of any size or structure. AutoInsight automatically detects encoding issues, "
         "column types, and data quality problems — no manual configuration, no format requirements."),
        ("🧹", "Auto-Clean Messy Data",
         "Real-world data is never perfect. Missing numeric values are filled using mean or median (your choice), "
         "and missing categorical values are filled with the most frequent value — with a full transparency log of "
         "exactly what was changed."),
        ("📊", "Instant, Relevant Charts",
         "Rather than generic templates, AutoInsight inspects each column's type and cardinality to decide what "
         "actually makes sense to chart — distributions for numbers, breakdowns for categories, comparisons across both."),
        ("💬", "Chat With Your Data",
         "Ask questions the way you'd ask a colleague — 'what's the average charge for smokers?' The assistant "
         "translates your question into real pandas code, runs it, and explains the actual computed result. "
         "No hallucinated numbers."),
        ("📄", "Export Real Reports",
         "Generate a polished Word or PDF document — not a screenshot — containing your dataset overview, "
         "every insight, every chart, and your full Q&A history, ready to share or archive."),
        ("🔒", "Private, Per-Account Storage",
         "Every file you upload is saved securely under your own login. Log out, come back later, and every "
         "dataset you've worked on is exactly where you left it."),
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

    st.markdown('<div class="landing-divider"></div>', unsafe_allow_html=True)

    # ===== HOW IT WORKS =====
    st.markdown('<div class="section-header" style="text-align:center;">How It Works</div>', unsafe_allow_html=True)
    steps = [
        ("1", "Create an account", "Sign up in seconds — your data is tied to your account and nobody else's."),
        ("2", "Upload your file", "CSV or Excel. Clean missing values in a single click if needed."),
        ("3", "Explore and ask", "Browse auto-generated charts, ask questions in plain English, and export your findings."),
    ]
    cols = st.columns(3)
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
                <div style="text-align:center;">
                    <div class="step-number">{num}</div>
                    <div class="feature-title" style="text-align:center;">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="landing-divider"></div>', unsafe_allow_html=True)

    # ===== WHO IT'S FOR =====
    st.markdown('<div class="section-header" style="text-align:center;">Built For</div>', unsafe_allow_html=True)
    audiences = [
        ("🎓", "Students & Researchers", "Analyze survey or experiment data without learning a stats package first."),
        ("📈", "Small Business Owners", "Understand sales, inventory, or customer data without hiring an analyst."),
        ("🧑‍💼", "Analysts & PMs", "Get a fast first pass on a new dataset before diving into deeper tooling."),
    ]
    cols = st.columns(3)
    for col, (icon, title, desc) in zip(cols, audiences):
        with col:
            st.markdown(f"""
                <div class="feature-grid-card" style="text-align:center;">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ===== FINAL CTA =====
    st.markdown("""
        <div style="text-align:center;">
            <div class="section-header" style="text-align:center; margin-bottom:0.5rem;">Ready to understand your data?</div>
            <div class="feature-desc" style="margin-bottom:1.5rem;">No credit card, no installation. Just upload and ask.</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.3, 1, 1.3])
    with col2:
        if st.button("Get Started →", key="bottom_cta", width='stretch'):
            st.session_state.view = "auth"
            st.session_state.auth_tab = "Sign Up"
            st.rerun()