def get_theme_css(mode="dark"):
    if mode == "dark":
        colors = {
            "bg": "#050505",
            "surface": "#151210",
            "surface_2": "#1A1512",
            "text_primary": "#EDE6DD",
            "text_secondary": "#8A8078",
            "border": "#2A2320",
            "accent": "#D97A3F",
            "accent_light": "#E8935C",
            "accent_dark": "#B8632E",
            "shadow": "rgba(0,0,0,0.5)",
        }
    else:
        colors = {
            "bg": "#FAF6F1",
            "surface": "#FFFFFF",
            "surface_2": "#F3ECE3",
            "text_primary": "#2A2118",
            "text_secondary": "#7A6F63",
            "border": "#E6DCCF",
            "accent": "#B8632E",
            "accent_light": "#D97A3F",
            "accent_dark": "#8F4D22",
            "shadow": "rgba(42,33,24,0.08)",
        }

    css = f"""
    <style>
    .stApp {{
        background-color: {colors['bg']};
        color: {colors['text_primary']};
    }}
    .stApp p, .stApp span, .stApp div, .stApp label, .stApp h1,
    .stApp h2, .stApp h3, .stApp li {{
        color: {colors['text_primary']};
    }}
    [data-testid="stHeader"] {{ display: none; }}
    [data-testid="stToolbar"] {{ display: none; }}
    [data-testid="stDecoration"] {{ display: none; }}
    .stDeployButton {{ display: none; }}

    .block-container {{
        padding-top: 1.2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1400px;
        animation: fadeInPage 0.35s ease;
    }}
    @keyframes fadeInPage {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    [data-testid="stSidebar"] {{
        background-color: {colors['surface']};
        border-right: 1px solid {colors['border']};
        min-width: 280px !important;
        max-width: 280px !important;
        transform: none !important;
        visibility: visible !important;
        display: flex;
        flex-direction: column;
    }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] label {{
        color: {colors['text_primary']};
    }}
    [data-testid="collapsedControl"] {{ display: none; }}
    [data-testid="stSidebarCollapseButton"] {{ display: none; }}
    button[kind="header"] {{ display: none; }}
    [data-testid="stSidebar"] button[aria-label*="ollapse"] {{ display: none; }}

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        gap: 0.4rem;
    }}
    [data-testid="stSidebarUserContent"] {{
        padding-top: 0.8rem !important;
    }}
    section[data-testid="stSidebar"] > div {{
        padding-top: 0 !important;
    }}

    .sidebar-brand {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.4rem 0 0.2rem 0;
    }}
    .sidebar-brand-icon {{
        font-size: 1.5rem;
        filter: drop-shadow(0 0 8px {colors['accent']}66);
    }}
    .sidebar-brand-name {{
        font-size: 1.15rem;
        font-weight: 800;
        color: {colors['text_primary']};
        font-family: 'Courier New', monospace;
    }}
    .sidebar-user-box {{
        background-color: {colors['surface_2']};
        border: 1px solid {colors['border']};
        border-radius: 10px;
        padding: 0.7rem 0.9rem;
        margin: 0.6rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }}
    .sidebar-user-avatar {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, {colors['accent']}, {colors['accent_dark']});
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
        flex-shrink: 0;
    }}
    .sidebar-user-name {{
        font-size: 0.85rem;
        font-weight: 600;
        color: {colors['text_primary']};
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }}
    .sidebar-user-label {{
        font-size: 0.7rem;
        color: {colors['text_secondary']};
    }}

    .sidebar-nav-label {{
        font-size: 0.7rem;
        font-weight: 700;
        color: {colors['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0.6rem 0 0.3rem 0.2rem;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] {{
        gap: 0.15rem;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"] label {{
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 0.5rem 0.7rem;
        width: 100%;
        transition: all 0.15s ease;
        cursor: pointer;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background-color: {colors['surface_2']};
        border-color: {colors['border']};
    }}
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {{
        background-color: {colors['accent']}22 !important;
        border-color: {colors['accent']}66 !important;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] p {{
        color: {colors['accent']} !important;
        font-weight: 700;
    }}

    .theme-toggle-box {{
        background-color: {colors['surface_2']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        padding: 0.6rem 0.8rem;
    }}

    .kpi-card {{
        background-color: {colors['surface']};
        border: 1px solid {colors['border']};
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
    }}
    .kpi-label {{
        color: {colors['text_secondary']};
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
        font-family: 'Courier New', monospace;
    }}
    .kpi-value {{
        color: {colors['text_primary']};
        font-size: 1.6rem;
        font-weight: 700;
    }}
    .kpi-value-accent {{
        color: {colors['accent']};
        font-size: 1.6rem;
        font-weight: 700;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {colors['surface']};
        border-radius: 10px;
    }}

    .section-header {{
        color: {colors['text_primary']};
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 1.4rem;
        margin-bottom: 0.3rem;
        font-family: 'Courier New', monospace;
    }}
    .section-caption {{
        color: {colors['text_secondary']};
        font-size: 0.85rem;
        margin-bottom: 0.9rem;
    }}

    .stButton button {{
        background-color: {colors['accent']};
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }}
    .stButton button:hover {{
        background-color: {colors['accent_dark']};
        color: #FFFFFF;
        box-shadow: 0 0 18px {colors['accent']}88;
        transform: translateY(-1px);
    }}

    [data-testid="stChatMessage"] {{
        background-color: {colors['surface']};
        border: 1px solid {colors['border']};
        border-radius: 10px;
    }}

    .top-navbar-brand {{
        font-size: 1.3rem;
        font-weight: 800;
        font-family: 'Courier New', monospace;
        color: {colors['text_primary']};
    }}
    .top-navbar-brand span {{
        color: {colors['accent']};
    }}

    .hero-section {{
        text-align: center;
        padding: 4rem 1rem 2.5rem 1rem;
        position: relative;
        border-radius: 20px;
        background-image:
            linear-gradient({colors['bg']}, {colors['bg']}),
            repeating-linear-gradient(0deg, {colors['border']}33 0px, transparent 1px, transparent 40px, {colors['border']}33 41px),
            repeating-linear-gradient(90deg, {colors['border']}33 0px, transparent 1px, transparent 40px, {colors['border']}33 41px);
        animation: gridPulse 6s ease-in-out infinite;
        overflow: hidden;
    }}
    @keyframes gridPulse {{
        0%, 100% {{ background-position: 0 0, 0 0, 0 0; opacity: 1; }}
        50% {{ background-position: 0 0, 0 8px, 8px 0; opacity: 0.85; }}
    }}
    .hero-glow {{
        position: absolute;
        top: -100px;
        left: 50%;
        transform: translateX(-50%);
        width: 500px;
        height: 300px;
        background: radial-gradient(circle, {colors['accent']}33 0%, transparent 70%);
        filter: blur(30px);
        z-index: 0;
        pointer-events: none;
    }}
    .hero-title {{
        font-size: 3.2rem;
        font-weight: 800;
        color: {colors['text_primary']};
        font-family: 'Courier New', monospace;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }}
    .hero-title span {{
        background: linear-gradient(90deg, {colors['accent']}, {colors['accent_light']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .hero-subtitle {{
        font-size: 1.15rem;
        color: {colors['text_secondary']};
        max-width: 640px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }}
    .hero-badge {{
        display: inline-block;
        background-color: {colors['surface_2']};
        border: 1px solid {colors['accent']}55;
        color: {colors['accent']};
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.35rem 0.9rem;
        border-radius: 20px;
        margin-bottom: 1.2rem;
        letter-spacing: 0.03em;
        position: relative;
        z-index: 1;
    }}

    .feature-grid-card {{
        background-color: {colors['surface']};
        border: 1px solid {colors['border']};
        border-radius: 14px;
        padding: 1.6rem 1.4rem;
        height: 100%;
        transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
    }}
    .feature-grid-card:hover {{
        border-color: {colors['accent']};
        box-shadow: 0 0 24px {colors['accent']}33;
        transform: translateY(-3px);
    }}
    .feature-icon {{
        font-size: 1.8rem;
        margin-bottom: 0.7rem;
    }}
    .feature-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {colors['text_primary']};
        margin-bottom: 0.4rem;
    }}
    .feature-desc {{
        font-size: 0.88rem;
        color: {colors['text_secondary']};
        line-height: 1.5;
    }}
    .step-number {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, {colors['accent']}, {colors['accent_dark']});
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 0 14px {colors['accent']}55;
    }}
    .landing-divider {{
        border-top: 1px solid {colors['border']};
        margin: 2.5rem 0;
    }}

    /* ===== EMPTY STATE ===== */
    .empty-state-card {{
        background-color: {colors['surface']};
        border: 1px dashed {colors['border']};
        border-radius: 16px;
        padding: 3rem 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }}
    .empty-state-icon {{
        font-size: 2.8rem;
        margin-bottom: 1rem;
        opacity: 0.8;
    }}
    .empty-state-title {{
        font-size: 1.15rem;
        font-weight: 700;
        color: {colors['text_primary']};
        margin-bottom: 0.5rem;
    }}
    .empty-state-desc {{
        font-size: 0.9rem;
        color: {colors['text_secondary']};
        max-width: 420px;
        margin: 0 auto;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
    """
    return css

def get_chart_colors(mode="dark"):
    if mode == "dark":
        return {
            "paper": "#151210", "plot": "#151210",
            "font": "#EDE6DD", "grid": "#2A2320", "line": "#3A322C",
            "accent": ["#D97A3F", "#E8935C", "#B8632E", "#8F4D22"]
        }
    else:
        return {
            "paper": "#FFFFFF", "plot": "#FFFFFF",
            "font": "#2A2118", "grid": "#E6DCCF", "line": "#D4C7B5",
            "accent": ["#B8632E", "#D97A3F", "#8F4D22", "#E8935C"]
        }