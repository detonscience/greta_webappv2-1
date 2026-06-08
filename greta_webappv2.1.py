import streamlit as st
import pandas as pd
from datetime import date, time, timedelta, datetime
import calendar
from io import BytesIO
from urllib.parse import quote
from pathlib import Path

st.set_page_config(page_title="VALENTINA STUDIO", page_icon="✨", layout="wide")

GOOGLE_DRIVE_BACKUP_LINK = "https://drive.google.com/drive/folders/1Sh6y2iN0n5wM3sh-QpKel5PExf7dDNcP?usp=sharing"
GOOGLE_DRIVE_FOLDER_ID = "1Sh6y2iN0n5wM3sh-QpKel5PExf7dDNcP"
LOCAL_BACKUP_FOLDER = Path.home() / "Documents" / "Valentina_Studio_Backups"
AUTO_BACKUP_EVERY_MINUTES = 60
AUTO_BACKUP_KEEP_COPIES = 72
AUTO_BACKUP_FOLDER_NAME = "Valentina_Studio_Auto_Backups"

st.markdown("""
<style>
:root {
    --bg-main: #07070d;
    --panel-dark: #10111c;
    --panel-mid: #171827;
    --text-main: #f8f4ff;
    --text-muted: #b7aabd;
    --neon-pink: #ff4fb8;
    --neon-purple: #9b5cff;
    --neon-cyan: #36e9ff;
    --glass-border: rgba(255,255,255,0.14);
}
html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 15% 0%, rgba(255,79,184,0.20), transparent 30%),
        radial-gradient(circle at 85% 10%, rgba(54,233,255,0.16), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(155,92,255,0.16), transparent 35%),
        #07070d !important;
    color: var(--text-main) !important;
}
[data-testid="stHeader"] {
    background: rgba(7,7,13,0.35) !important;
    backdrop-filter: blur(18px);
}
[data-testid="stToolbar"] {
    right: 1rem;
}
.block-container {
    padding-top: 3.2rem !important;
    padding-bottom: 3rem !important;
    overflow: visible !important;
    color: var(--text-main) !important;
}
.app-title {
    font-size: 42px;
    font-weight: 950;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #ffffff;
    line-height: 1.15;
    margin-top: 8px;
    margin-bottom: 6px;
    overflow: visible;
    text-shadow: 0 0 18px rgba(255,79,184,0.45), 0 0 34px rgba(54,233,255,0.22);
}
.small-muted {
    color: var(--text-muted);
    font-size: 14px;
    letter-spacing: 0.02em;
}
.top-app-header {
    padding: 18px 20px 20px 20px;
    overflow: visible;
    border: 1px solid var(--glass-border);
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.035));
    box-shadow: 0 20px 60px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.16);
    backdrop-filter: blur(20px);
    position: relative;
}
.top-app-header::after {
    content: "";
    position: absolute;
    left: 22px;
    right: 22px;
    bottom: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--neon-pink), var(--neon-purple), var(--neon-cyan));
    border-radius: 999px;
}
.fresha-hero {
    background: linear-gradient(135deg, rgba(255,255,255,0.11), rgba(255,255,255,0.035));
    border: 1px solid var(--glass-border);
    border-radius: 26px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0px 18px 50px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.14);
    backdrop-filter: blur(18px);
}
.fresha-title {
    font-size: 31px;
    font-weight: 950;
    color: #ffffff;
    margin-bottom: 6px;
    letter-spacing: 0.02em;
}
.fresha-subtitle {
    color: var(--text-muted);
    font-size: 15px;
}
.fresha-stat-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.105), rgba(255,255,255,0.035));
    border-radius: 22px;
    padding: 17px;
    border: 1px solid var(--glass-border);
    box-shadow: 0px 14px 36px rgba(0,0,0,0.24), inset 0 1px 0 rgba(255,255,255,0.12);
    margin-bottom: 10px;
    backdrop-filter: blur(18px);
}
.fresha-stat-card:hover {
    border-color: rgba(255,79,184,0.55);
    box-shadow: 0px 18px 42px rgba(255,79,184,0.10), 0px 14px 36px rgba(0,0,0,0.28);
}
.fresha-stat-label {
    color: var(--text-muted);
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.fresha-stat-value {
    color: #ffffff;
    font-size: 27px;
    font-weight: 950;
    text-shadow: 0 0 18px rgba(54,233,255,0.18);
}
.appointment-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.10), rgba(255,255,255,0.035));
    border-radius: 20px;
    padding: 13px;
    margin-bottom: 10px;
    border: 1px solid var(--glass-border);
    box-shadow: 0px 10px 26px rgba(0,0,0,0.22), inset 0 1px 0 rgba(255,255,255,0.10);
    backdrop-filter: blur(16px);
}
.appointment-card:hover {
    border-color: rgba(54,233,255,0.45);
    transform: translateY(-1px);
}
.appointment-time { font-size: 18px; font-weight: 950; color: var(--neon-cyan); }
.appointment-client { font-size: 15px; font-weight: 850; color: #ffffff; }
.appointment-meta { color: var(--text-muted); font-size: 13px; line-height: 1.35; }
.fresha-pill { display: inline-block; padding: 5px 10px; border-radius: 999px; font-size: 12px; font-weight: 750; margin-top: 6px; }
.pill-confirmada { background: rgba(54,233,255,0.16); color: var(--neon-cyan); border: 1px solid rgba(54,233,255,0.35); }
.pill-pendiente { background: rgba(255,204,79,0.15); color: #ffd166; border: 1px solid rgba(255,209,102,0.35); }
.pill-cancelada { background: rgba(255,79,110,0.14); color: #ff6b8a; border: 1px solid rgba(255,107,138,0.35); }
.pill-completada { background: rgba(155,92,255,0.18); color: #c7a8ff; border: 1px solid rgba(155,92,255,0.40); }
.day-box {
    background: linear-gradient(145deg, rgba(255,255,255,0.09), rgba(255,255,255,0.03));
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 12px;
    min-height: 230px;
    box-shadow: 0px 12px 32px rgba(0,0,0,0.22);
    margin-bottom: 12px;
    backdrop-filter: blur(16px);
    color: var(--text-main);
}
.quick-action-box {
    background: linear-gradient(145deg, rgba(255,79,184,0.12), rgba(54,233,255,0.07));
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 20px;
    padding: 15px;
    margin-top: 10px;
    color: var(--text-main);
    box-shadow: 0px 14px 34px rgba(0,0,0,0.22);
}

.backup-warning-banner {
    background:
        radial-gradient(circle at 0% 0%, rgba(255, 218, 92, 0.42), transparent 30%),
        radial-gradient(circle at 100% 0%, rgba(255, 79, 184, 0.28), transparent 34%),
        linear-gradient(135deg, rgba(255, 184, 28, 0.28), rgba(255, 79, 184, 0.13)) !important;
    border: 1px solid rgba(255, 218, 92, 0.65) !important;
    border-left: 7px solid #ffd75e !important;
    border-radius: 22px;
    padding: 16px 18px;
    margin: 0 0 10px 0;
    box-shadow: 0px 18px 46px rgba(255, 184, 28, 0.18), 0px 14px 38px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.22);
    backdrop-filter: blur(18px);
}
.backup-warning-title {
    color: #ffffff !important;
    font-size: 16px;
    font-weight: 950;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    text-shadow: 0 0 18px rgba(255, 215, 94, 0.42);
    margin-bottom: 4px;
}
.backup-warning-text {
    color: #fff5c4 !important;
    font-size: 14px;
    font-weight: 750;
    line-height: 1.4;
}
.drive-note-banner {
    background: linear-gradient(135deg, rgba(54,233,255,0.11), rgba(255,255,255,0.045));
    border: 1px solid rgba(54,233,255,0.28);
    border-radius: 16px;
    padding: 10px 13px;
    margin: 8px 0 14px 0;
    color: #dbfbff !important;
    font-size: 13px;
    font-weight: 700;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(14,15,27,0.98) 0%, rgba(8,8,15,0.98) 100%);
    border-right: 1px solid rgba(255,255,255,0.11);
    box-shadow: 18px 0 55px rgba(0,0,0,0.32);
}
section[data-testid="stSidebar"] h3 {
    color: #ffffff;
    font-weight: 900;
    letter-spacing: 0.03em;
}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #8b6b7b;
    font-weight: 650;
}
section[data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 10px 12px;
    margin-bottom: 7px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.16);
    transition: all 0.15s ease-in-out;
    backdrop-filter: blur(12px);
}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    border-color: rgba(54,233,255,0.45);
    background: rgba(54,233,255,0.08);
    transform: translateX(3px);
}
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, rgba(255,79,184,0.95), rgba(155,92,255,0.95));
    border-color: rgba(255,255,255,0.22);
    box-shadow: 0px 10px 28px rgba(255,79,184,0.25);
}
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: #ffffff !important;
    font-weight: 850;
}
section[data-testid="stSidebar"] [role="radiogroup"] label p {
    font-size: 14px;
    font-weight: 780;
    color: #f3ecff;
    letter-spacing: 0.015em;
}
section[data-testid="stSidebar"] [role="radiogroup"] label p::first-letter {
    color: var(--neon-cyan);
}
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p::first-letter {
    color: #ffffff;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    border-radius: 16px;
    border-color: rgba(255,255,255,0.18) !important;
    background: rgba(255,255,255,0.10) !important;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.18);
    color: #ffffff !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #ffffff !important;
}
.sidebar-brand-card {
    background:
        radial-gradient(circle at 0% 0%, rgba(54,233,255,0.26), transparent 28%),
        radial-gradient(circle at 100% 0%, rgba(255,79,184,0.34), transparent 34%),
        linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0.045));
    color: white;
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 24px;
    padding: 18px;
    margin: 8px 0 16px 0;
    box-shadow: 0px 18px 48px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.18);
    backdrop-filter: blur(18px);
}
.sidebar-brand-title {
    font-size: 18px;
    font-weight: 950;
    margin-bottom: 2px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.sidebar-brand-subtitle {
    font-size: 12px;
    color: #d8c9e8;
    letter-spacing: 0.04em;
}
.stButton > button, .stDownloadButton > button, div[data-testid="stLinkButton"] a {
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    background: linear-gradient(135deg, rgba(255,79,184,0.92), rgba(155,92,255,0.90)) !important;
    color: #ffffff !important;
    font-weight: 850 !important;
    box-shadow: 0px 12px 26px rgba(255,79,184,0.18) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover, div[data-testid="stLinkButton"] a:hover {
    border-color: rgba(54,233,255,0.6) !important;
    box-shadow: 0px 14px 32px rgba(54,233,255,0.16) !important;
    transform: translateY(-1px);
}
div[data-testid="stDataFrame"], div[data-testid="stDataEditor"] {
    border-radius: 18px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
}
hr {
    border-color: rgba(255,255,255,0.12) !important;
}
/* Improve text contrast for Streamlit controls in dark neon mode */
.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div,
label, p, span, div[data-testid="stText"], div[data-testid="stCaptionContainer"] {
    color: var(--text-main) !important;
}

div[data-baseweb="tab-list"] button {
    color: #b7aabd !important;
    font-weight: 800 !important;
    border-radius: 999px !important;
    padding: 8px 14px !important;
}

div[data-baseweb="tab-list"] button[aria-selected="true"] {
    color: #ffffff !important;
    background: linear-gradient(135deg, rgba(255,79,184,0.28), rgba(54,233,255,0.14)) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    box-shadow: 0px 8px 22px rgba(255,79,184,0.14) !important;
}

div[data-baseweb="tab-border"] {
    background: rgba(255,255,255,0.12) !important;
}

div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stDateInput"] label,
div[data-testid="stTimeInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stFileUploader"] label,
div[data-testid="stCheckbox"] label,
div[data-testid="stRadio"] label {
    color: #f8f4ff !important;
    font-weight: 800 !important;
}

input, textarea, div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
    color: #111111 !important;
    background: #f8f4ff !important;
    border-radius: 14px !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    background: #f8f4ff !important;
    border-color: rgba(255,255,255,0.22) !important;
    border-radius: 14px !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: #111111 !important;
}

.stCodeBlock pre, code {
    color: #111111 !important;
    background: #f8f4ff !important;
    border-radius: 14px !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

.stAlert, div[data-testid="stAlert"] {
    color: #111111 !important;
}

div[data-testid="stAlert"] * {
    color: #111111 !important;
}

/* Keep disabled-looking text readable */
button:disabled, input:disabled, textarea:disabled {
    opacity: 0.85 !important;
}
/* iPad / tablet layout improvements */
@media screen and (min-width: 769px) and (max-width: 1180px) {
    .block-container {
        padding-top: 2rem !important;
        padding-left: 1.35rem !important;
        padding-right: 1.35rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 100% !important;
    }

    .top-app-header {
        padding: 16px 18px 18px 18px !important;
        border-radius: 24px !important;
        margin-bottom: 4px !important;
    }

    .app-title {
        font-size: 34px !important;
        letter-spacing: 0.06em !important;
        line-height: 1.12 !important;
    }

    .small-muted {
        font-size: 13px !important;
        line-height: 1.35 !important;
    }

    .fresha-hero {
        padding: 20px !important;
        border-radius: 22px !important;
        margin-bottom: 16px !important;
    }

    .fresha-title {
        font-size: 28px !important;
        line-height: 1.16 !important;
    }

    .fresha-subtitle {
        font-size: 14px !important;
        line-height: 1.35 !important;
    }

    .fresha-stat-card {
        padding: 15px !important;
        border-radius: 19px !important;
        min-height: 104px !important;
    }

    .fresha-stat-value {
        font-size: 24px !important;
        line-height: 1.15 !important;
    }

    .appointment-card {
        padding: 12px !important;
        border-radius: 18px !important;
        margin-bottom: 9px !important;
    }

    .appointment-time {
        font-size: 17px !important;
    }

    .appointment-client {
        font-size: 14px !important;
    }

    .appointment-meta {
        font-size: 12px !important;
        line-height: 1.35 !important;
    }

    .day-box {
        min-height: 190px !important;
        padding: 10px !important;
        border-radius: 17px !important;
    }

    section[data-testid="stSidebar"] {
        min-width: 240px !important;
        max-width: 260px !important;
    }

    .sidebar-brand-card {
        padding: 14px !important;
        border-radius: 20px !important;
        margin: 4px 0 14px 0 !important;
    }

    .sidebar-brand-title {
        font-size: 15px !important;
        letter-spacing: 0.06em !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label {
        padding: 10px 11px !important;
        border-radius: 14px !important;
        margin-bottom: 7px !important;
        min-height: 42px !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label p {
        font-size: 12px !important;
        line-height: 1.15 !important;
    }

    .stButton > button, .stDownloadButton > button, div[data-testid="stLinkButton"] a {
        min-height: 44px !important;
        padding: 0.55rem 1rem !important;
        border-radius: 15px !important;
        font-size: 13px !important;
    }

    input, textarea, div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
        min-height: 42px !important;
        font-size: 15px !important;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        min-height: 44px !important;
        border-radius: 14px !important;
    }

    div[data-baseweb="tab-list"] {
        gap: 6px !important;
        overflow-x: auto !important;
        padding-bottom: 4px !important;
    }

    div[data-baseweb="tab-list"] button {
        white-space: nowrap !important;
        min-height: 40px !important;
        font-size: 13px !important;
        padding: 8px 13px !important;
    }

    div[data-testid="stDataFrame"], div[data-testid="stDataEditor"] {
        max-width: 100% !important;
        overflow-x: auto !important;
    }
}
@media screen and (max-width: 768px) {
    section[data-testid="stSidebar"] {
        min-width: 100% !important;
    }
    .block-container {
        padding-top: 1.5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 2rem !important;
    }

    .top-app-header {
        padding-top: 4px !important;
        padding-bottom: 8px !important;
    }

    .app-title {
        font-size: 28px !important;
        line-height: 1.2 !important;
        margin-top: 4px !important;
        margin-bottom: 4px !important;
    }

    .small-muted {
        font-size: 12px !important;
        line-height: 1.35 !important;
    }

    .fresha-title {
        font-size: 24px !important;
        line-height: 1.18 !important;
    }

    .fresha-subtitle {
        font-size: 13px !important;
        line-height: 1.35 !important;
    }

    .fresha-hero {
        padding: 16px !important;
        border-radius: 18px !important;
        margin-bottom: 14px !important;
    }

    .fresha-stat-card {
        padding: 13px !important;
        border-radius: 16px !important;
    }

    .fresha-stat-value {
        font-size: 21px !important;
    }

    .appointment-card {
        padding: 11px !important;
        border-radius: 16px !important;
    }

    .appointment-time {
        font-size: 16px !important;
    }

    .appointment-client {
        font-size: 14px !important;
    }

    .appointment-meta {
        font-size: 12px !important;
    }

    .day-box {
        min-height: auto !important;
        padding: 10px !important;
        border-radius: 14px !important;
        margin-bottom: 8px !important;
    }

    .quick-action-box {
        padding: 12px !important;
        border-radius: 14px !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label {
        padding: 8px 10px !important;
        border-radius: 14px !important;
        margin-bottom: 6px !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label p {
        font-size: 13px !important;
    }

    .sidebar-brand-card {
        padding: 13px !important;
        border-radius: 18px !important;
        margin-bottom: 12px !important;
    }

    .sidebar-brand-title {
        font-size: 16px !important;
    }

    .sidebar-brand-subtitle {
        font-size: 11px !important;
    }
}
</style>
""", unsafe_allow_html=True)


def money(x):
    try:
        return f"${float(x):,.2f}"
    except Exception:
        return "$0.00"


def render_fresha_hero(title, subtitle):
    st.markdown(f"""
    <div class="fresha-hero">
        <div class="fresha-title">{title}</div>
        <div class="fresha-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def render_stat_card(label, value, note=""):
    st.markdown(f"""
    <div class="fresha-stat-card">
        <div class="fresha-stat-label">{label}</div>
        <div class="fresha-stat-value">{value}</div>
        <div class="small-muted">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def get_device_mode():
    try:
        width = st.context.browser.width
    except Exception:
        width = 1200

    if width <= 768:
        return "mobile"
    if width <= 1180:
        return "ipad"
    return "desktop"


def responsive_columns(desktop_count, ipad_count=2, mobile_count=1):
    device_mode = get_device_mode()
    if device_mode == "mobile":
        return st.columns(mobile_count)
    if device_mode == "ipad":
        return st.columns(ipad_count)
    return st.columns(desktop_count)


def status_class(status):
    status_clean = str(status).strip().lower()
    if status_clean == "confirmada":
        return "pill-confirmada"
    if status_clean == "cancelada":
        return "pill-cancelada"
    if status_clean == "completada":
        return "pill-completada"
    return "pill-pendiente"


def render_appointment_card(row, compact=False):
    pill_class = status_class(row.get("Estado", "Pendiente"))
    extra = "" if compact else f"<br>Diseño: {row.get('Diseno', '')}<br>Materiales: {row.get('Materiales', '')}"

    st.markdown(f"""
    <div class="appointment-card">
        <div class="appointment-time">{row.get('Hora', '')}</div>
        <div class="appointment-client">{row.get('Cliente', '')}</div>
        <div class="appointment-meta">
            {row.get('Servicio', '')} · {row.get('Empleado', '')}<br>
            Precio: <b>{money(row.get('Precio', 0))}</b>{extra}
        </div>
        <span class="fresha-pill {pill_class}">{row.get('Estado', 'Pendiente')}</span>
    </div>
    """, unsafe_allow_html=True)


def init_data():
    if "clientes" not in st.session_state:
        st.session_state.clientes = pd.DataFrame([
            {
                "Nombre": "Maria Lopez",
                "Telefono": "2105551111",
                "Email": "maria@example.com",
                "Cumpleanos": "1990-05-15",
                "Notas": "Prefiere tonos nude y citas por la mañana."
            },
            {
                "Nombre": "Ana Rivera",
                "Telefono": "2105552222",
                "Email": "ana@example.com",
                "Cumpleanos": "1988-10-02",
                "Notas": "Cliente frecuente, le gusta diseño minimalista."
            },
            {
                "Nombre": "Sofia Garcia",
                "Telefono": "2105553333",
                "Email": "sofia@example.com",
                "Cumpleanos": "1995-02-20",
                "Notas": "Prefiere pedicure los sábados."
            },
        ])

    if "empleados" not in st.session_state:
        st.session_state.empleados = pd.DataFrame([
            {
                "Nombre": "Greta",
                "Puesto": "Admin",
                "Activo": True,
                "Sueldo base": 900.0,
                "Comision %": 20.0
            },
            {
                "Nombre": "Eva",
                "Puesto": "Técnica",
                "Activo": True,
                "Sueldo base": 700.0,
                "Comision %": 25.0
            },
            {
                "Nombre": "Luna",
                "Puesto": "Técnica",
                "Activo": True,
                "Sueldo base": 650.0,
                "Comision %": 25.0
            },
        ])

    if "catalogo" not in st.session_state:
        st.session_state.catalogo = pd.DataFrame([
            {
                "Servicio": "Manicure gel",
                "Categoria": "Manos",
                "Duracion min": 60,
                "Precio": 55.0,
                "Activo": True,
                "Descripcion": "Aplicación de gel con limpieza básica."
            },
            {
                "Servicio": "Acrílico",
                "Categoria": "Manos",
                "Duracion min": 90,
                "Precio": 75.0,
                "Activo": True,
                "Descripcion": "Set acrílico completo."
            },
            {
                "Servicio": "Pedicure",
                "Categoria": "Pies",
                "Duracion min": 60,
                "Precio": 50.0,
                "Activo": True,
                "Descripcion": "Pedicure sencillo."
            },
            {
                "Servicio": "Retoque",
                "Categoria": "Manos",
                "Duracion min": 75,
                "Precio": 60.0,
                "Activo": True,
                "Descripcion": "Retoque de acrílico o gel."
            },
        ])

    if "citas" not in st.session_state:
        st.session_state.citas = pd.DataFrame([
            {
                "Fecha": str(date.today()),
                "Hora": "10:00",
                "Cliente": "Maria Lopez",
                "Empleado": "Greta",
                "Servicio": "Manicure gel",
                "Diseno": "French natural",
                "Materiales": "Gel nude, top coat",
                "Costo materiales": 8.0,
                "Precio": 55.0,
                "Estado": "Confirmada",
                "Notas": "Llega 10 min antes."
            },
            {
                "Fecha": str(date.today()),
                "Hora": "13:00",
                "Cliente": "Ana Rivera",
                "Empleado": "Eva",
                "Servicio": "Acrílico",
                "Diseno": "Coffin corto",
                "Materiales": "Acrílico clear, gel rosa",
                "Costo materiales": 12.0,
                "Precio": 75.0,
                "Estado": "Pendiente",
                "Notas": "Confirmar por WhatsApp."
            },
            {
                "Fecha": str(date.today() + timedelta(days=1)),
                "Hora": "11:30",
                "Cliente": "Sofia Garcia",
                "Empleado": "Luna",
                "Servicio": "Pedicure",
                "Diseno": "Rojo clásico",
                "Materiales": "Esmalte rojo",
                "Costo materiales": 6.0,
                "Precio": 50.0,
                "Estado": "Confirmada",
                "Notas": "Cliente regular."
            },
        ])

    if "ventas" not in st.session_state:
        st.session_state.ventas = pd.DataFrame([
            {
                "Fecha": str(date.today()),
                "Cliente": "Maria Lopez",
                "Servicio": "Manicure gel",
                "Empleado": "Greta",
                "Metodo pago": "Tarjeta",
                "Subtotal": 55.0,
                "Descuento": 0.0,
                "Total": 55.0,
                "Notas": "Venta demo"
            },
        ])

    if "inventario" not in st.session_state:
        st.session_state.inventario = pd.DataFrame([
            {
                "Producto": "Gel nude",
                "Categoria": "Gel",
                "Cantidad": 5,
                "Minimo": 2,
                "Costo unitario": 9.5
            },
            {
                "Producto": "Top coat",
                "Categoria": "Gel",
                "Cantidad": 2,
                "Minimo": 2,
                "Costo unitario": 8.0
            },
            {
                "Producto": "Acrílico clear",
                "Categoria": "Acrílico",
                "Cantidad": 1,
                "Minimo": 2,
                "Costo unitario": 15.0
            },
        ])

    if "gastos" not in st.session_state:
        st.session_state.gastos = pd.DataFrame([
            {
                "Fecha": str(date.today()),
                "Concepto": "Renta",
                "Categoria": "Fijo",
                "Monto": 1200.0,
                "Notas": "Demo"
            },
            {
                "Fecha": str(date.today()),
                "Concepto": "Materiales",
                "Categoria": "Inventario",
                "Monto": 180.0,
                "Notas": "Compra demo"
            },
        ])

    if "usuarios" not in st.session_state:
        st.session_state.usuarios = pd.DataFrame([
            {
                "Usuario": "admin",
                "Nombre": "Greta",
                "Rol": "Admin",
                "Activo": True
            },
            {
                "Usuario": "recepcion",
                "Nombre": "Recepción",
                "Rol": "Recepción",
                "Activo": True
            },
            {
                "Usuario": "eva",
                "Nombre": "Eva",
                "Rol": "Empleada",
                "Activo": True
            },
        ])

    if "app_settings" not in st.session_state:
        st.session_state.app_settings = {
            "nombre_negocio": "Greta Studio",
            "telefono_negocio": "",
            "direccion_negocio": "",
            "moneda": "USD",
            "online_booking_activo": True,
            "requiere_confirmacion_online": True,
        }

    if "social_integrations" not in st.session_state:
        st.session_state.social_integrations = {
            "booking_link": "https://greta-studio-booking.example.com",
            "google_reserve_enabled": False,
            "google_business_profile": "",
            "facebook_enabled": False,
            "facebook_page": "",
            "instagram_enabled": False,
            "instagram_profile": "",
            "meta_pixel_enabled": False,
            "meta_pixel_id": "",
            "google_analytics_enabled": False,
            "google_analytics_id": "",
            "tiktok_profile": "",
            "website_url": ""
        }


init_data()


def ensure_cita_ids():
    if "citas" not in st.session_state:
        return

    citas = st.session_state.citas.copy()

    if "Cita ID" not in citas.columns:
        citas.insert(0, "Cita ID", [f"CITA-{i + 1:03d}" for i in range(len(citas))])
    else:
        used_ids = set()
        next_number = 1
        fixed_ids = []

        for raw_id in citas["Cita ID"].astype(str).tolist():
            clean_id = raw_id.strip()

            if clean_id and clean_id.lower() != "nan" and clean_id not in used_ids:
                fixed_ids.append(clean_id)
                used_ids.add(clean_id)
                continue

            while f"CITA-{next_number:03d}" in used_ids:
                next_number += 1

            new_id = f"CITA-{next_number:03d}"
            fixed_ids.append(new_id)
            used_ids.add(new_id)
            next_number += 1

        citas["Cita ID"] = fixed_ids

    st.session_state.citas = citas


def next_cita_id():
    ensure_cita_ids()

    citas = st.session_state.citas.copy()
    max_number = 0

    if "Cita ID" in citas.columns:
        for raw_id in citas["Cita ID"].astype(str).tolist():
            clean_id = raw_id.strip().upper()
            if clean_id.startswith("CITA-"):
                try:
                    max_number = max(max_number, int(clean_id.replace("CITA-", "")))
                except Exception:
                    pass

    return f"CITA-{max_number + 1:03d}"


def delete_cita_by_id(cita_id):
    ensure_cita_ids()

    if not cita_id:
        return

    st.session_state.citas = st.session_state.citas[
        st.session_state.citas["Cita ID"].astype(str) != str(cita_id)
    ].reset_index(drop=True)


ensure_cita_ids()


ROLE_MENUS = {
    "Admin": [
        "Inicio",
        "Agenda Fresha",
        "Calendario",
        "Nueva cita",
        "Ventas",
        "Lista de clientes",
        "Catálogo",
        "Online booking",
        "Integraciones",
        "Reportes",
        "WhatsApp",
        "Empleados",
        "Nómina",
        "Inventario",
        "Finanzas",
        "Settings",
        "Ayuda / Guía",
        "Excel / Backup"
    ],
    "Recepción": [
        "Inicio",
        "Agenda Fresha",
        "Calendario",
        "Nueva cita",
        "Ventas",
        "Lista de clientes",
        "Catálogo",
        "Online booking",
        "Integraciones",
        "WhatsApp",
        "Ayuda / Guía"
    ],
    "Empleada": [
        "Inicio",
        "Agenda Fresha",
        "Calendario",
        "Lista de clientes",
        "WhatsApp",
        "Ayuda / Guía"
    ],
}


MENU_ICONS = {
    "Inicio": "⌂",
    "Agenda Fresha": "◷",
    "Calendario": "□",
    "Nueva cita": "+",
    "Ventas": "◈",
    "Lista de clientes": "◎",
    "Catálogo": "◇",
    "Online booking": "◌",
    "Integraciones": "⌁",
    "Reportes": "▰",
    "WhatsApp": "◍",
    "Empleados": "◉",
    "Nómina": "$",
    "Inventario": "▣",
    "Finanzas": "↗",
    "Settings": "⚙",
    "Ayuda / Guía": "?",
    "Excel / Backup": "▤"
}


def menu_label(name):
    return f"{MENU_ICONS.get(name, '•')}   {name}"


def clean_menu_label(label):
    for name in MENU_ICONS:
        if label.endswith(name):
            return name
    return label


def get_allowed_menus(role):
    return ROLE_MENUS.get(role, ROLE_MENUS["Empleada"])


def require_admin():
    if st.session_state.get("current_role", "Admin") != "Admin":
        st.warning("Esta sección es solo para Admin.")
        st.stop()


def get_client_info(nombre):
    clientes = st.session_state.clientes
    match = clientes[clientes["Nombre"] == nombre]
    if match.empty:
        return None
    return match.iloc[0]


def render_whatsapp_buttons(row):
    cliente = get_client_info(row.get("Cliente", ""))
    telefono = "" if cliente is None else str(cliente.get("Telefono", ""))
    telefono_limpio = "".join(ch for ch in telefono if ch.isdigit())

    if not telefono_limpio:
        st.caption("Cliente sin teléfono para WhatsApp.")
        return

    mensajes = {
        "Confirmar": f"Hola {row.get('Cliente', '')}, te confirmamos tu cita el {row.get('Fecha', '')} a las {row.get('Hora', '')} para {row.get('Servicio', '')}. Gracias.",
        "Recordatorio": f"Hola {row.get('Cliente', '')}, te recordamos tu cita el {row.get('Fecha', '')} a las {row.get('Hora', '')}. Te esperamos.",
        "Gracias": f"Hola {row.get('Cliente', '')}, muchas gracias por visitarnos en Valentina Studio. Esperamos verte pronto.",
        "Promo": f"Hola {row.get('Cliente', '')}, tenemos una promoción especial para ti en Valentina Studio. Escríbenos para más detalles.",
    }

    cols = st.columns(4)
    for i, (label, msg) in enumerate(mensajes.items()):
        cols[i].link_button(
            label,
            f"https://wa.me/{telefono_limpio}?text={quote(msg)}"
        )


def export_excel():
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        st.session_state.clientes.to_excel(writer, index=False, sheet_name="Clientes")
        st.session_state.empleados.to_excel(writer, index=False, sheet_name="Empleados")
        st.session_state.citas.to_excel(writer, index=False, sheet_name="Citas")
        st.session_state.inventario.to_excel(writer, index=False, sheet_name="Inventario")
        st.session_state.gastos.to_excel(writer, index=False, sheet_name="Gastos")
        st.session_state.catalogo.to_excel(writer, index=False, sheet_name="Catalogo")
        st.session_state.ventas.to_excel(writer, index=False, sheet_name="Ventas")
        st.session_state.usuarios.to_excel(writer, index=False, sheet_name="Usuarios")
        pd.DataFrame([st.session_state.social_integrations]).to_excel(writer, index=False, sheet_name="Integraciones")

    return output.getvalue()


def export_blank_excel_template():
    output = BytesIO()

    template_sheets = {
        "Clientes": list(st.session_state.clientes.columns),
        "Empleados": list(st.session_state.empleados.columns),
        "Citas": list(st.session_state.citas.columns),
        "Inventario": list(st.session_state.inventario.columns),
        "Gastos": list(st.session_state.gastos.columns),
        "Catalogo": list(st.session_state.catalogo.columns),
        "Ventas": list(st.session_state.ventas.columns),
        "Usuarios": list(st.session_state.usuarios.columns),
        "Integraciones": list(pd.DataFrame([st.session_state.social_integrations]).columns),
    }

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, columns in template_sheets.items():
            pd.DataFrame(columns=columns).to_excel(writer, index=False, sheet_name=sheet_name)

    return output.getvalue()


def save_backup_to_local_computer(destination_folder=None, prefix="valentina_studio_backup"):
    if destination_folder:
        backup_folder = Path(str(destination_folder)).expanduser()
    else:
        backup_folder = LOCAL_BACKUP_FOLDER

    backup_folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = backup_folder / f"{prefix}_{timestamp}.xlsx"

    counter = 2
    while backup_path.exists():
        backup_path = backup_folder / f"{prefix}_{timestamp}_{counter}.xlsx"
        counter += 1

    backup_path.write_bytes(export_excel())
    return backup_path


def find_google_drive_sync_folder():
    possible_roots = [
        Path.home() / "Library" / "CloudStorage",
        Path.home() / "Google Drive",
        Path.home() / "My Drive",
    ]

    for root in possible_roots:
        if not root.exists():
            continue

        if root.name in ["Google Drive", "My Drive"]:
            return root / AUTO_BACKUP_FOLDER_NAME

        for candidate in sorted(root.glob("GoogleDrive*")):
            my_drive = candidate / "My Drive"
            if my_drive.exists():
                return my_drive / AUTO_BACKUP_FOLDER_NAME

            if candidate.exists():
                return candidate / AUTO_BACKUP_FOLDER_NAME

    return None


def cleanup_old_auto_backups(backup_folder, keep_copies=AUTO_BACKUP_KEEP_COPIES):
    backup_folder = Path(backup_folder)
    backups = sorted(
        backup_folder.glob("valentina_studio_auto_backup_*.xlsx"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    for old_backup in backups[keep_copies:]:
        try:
            old_backup.unlink()
        except Exception:
            pass


def run_hidden_hourly_auto_backup():
    now = datetime.now()
    last_backup = st.session_state.get("hidden_last_auto_backup_at")

    if last_backup is not None:
        elapsed_minutes = (now - last_backup).total_seconds() / 60
        if elapsed_minutes < AUTO_BACKUP_EVERY_MINUTES:
            return

    google_drive_folder = find_google_drive_sync_folder()
    backup_folder = google_drive_folder if google_drive_folder else (LOCAL_BACKUP_FOLDER / AUTO_BACKUP_FOLDER_NAME)

    try:
        backup_path = save_backup_to_local_computer(
            backup_folder,
            prefix="valentina_studio_auto_backup"
        )
        cleanup_old_auto_backups(backup_folder)
        st.session_state.hidden_last_auto_backup_at = now
        st.session_state.hidden_last_auto_backup_path = str(backup_path)
    except Exception as exc:
        st.session_state.hidden_last_auto_backup_error = str(exc)


def render_backup_banner():
    st.markdown("""
    <div class="backup-warning-banner">
        <div class="backup-warning-title">⚠ Respaldo recomendado antes de borrar o hacer pruebas</div>
        <div class="backup-warning-text">
            Descarga un backup Excel, guarda una copia local y sube otra copia a Google Drive antes de eliminar información.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="drive-note-banner">
        Google Drive automático directo requiere Drive API. Por ahora el backup automático funciona con Google Drive Desktop; el botón abre tu carpeta privada de Drive.
    </div>
    """, unsafe_allow_html=True)

    backup_destination = st.text_input(
        "Carpeta para guardar backup local",
        value=str(LOCAL_BACKUP_FOLDER),
        help="Puedes pegar una ruta como ~/Desktop, ~/Documents/Backups o una carpeta sincronizada con Google Drive.",
        key="global_backup_destination_folder"
    )

    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button("Guardar backup en esta carpeta", key="global_save_local_backup"):
            try:
                path = save_backup_to_local_computer(backup_destination)
                st.success(f"Backup guardado en: {path}")
            except Exception as exc:
                st.error(f"No se pudo guardar el backup. Revisa la ruta de carpeta. Error: {exc}")

    with b2:
        st.download_button(
            "Descargar backup Excel",
            data=export_excel(),
            file_name=f"valentina_studio_backup_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="global_download_backup_excel"
        )

    with b3:
        st.link_button("Abrir Google Drive", GOOGLE_DRIVE_BACKUP_LINK)

    with st.expander("Excel de emergencia / subir datos", expanded=False):
        render_excel_emergency_import_export()


def delete_rows_by_indexes(session_key, indexes_to_delete):
    if not indexes_to_delete:
        return 0

    df = st.session_state[session_key].copy()
    valid_indexes = [int(i) for i in indexes_to_delete if int(i) in df.index]

    if not valid_indexes:
        return 0

    st.session_state[session_key] = df.drop(index=valid_indexes).reset_index(drop=True)

    if session_key == "citas":
        ensure_cita_ids()

    return len(valid_indexes)


def render_delete_rows_tool(title, session_key, label_column=None, key_prefix="delete_tool"):
    df = st.session_state.get(session_key, pd.DataFrame()).copy()

    st.markdown(f"### Borrar datos incorrectos: {title}")
    st.caption("Primero respalda. Marca con el puntito/checkbox las filas incorrectas y confirma antes de borrar.")

    if df.empty:
        st.info(f"No hay datos en {title}.")
        return

    delete_df = df.copy().reset_index().rename(columns={"index": "Fila original"})
    delete_df.insert(0, "Borrar", False)

    edited_delete_df = st.data_editor(
        delete_df,
        use_container_width=True,
        hide_index=True,
        disabled=[col for col in delete_df.columns if col != "Borrar"],
        column_config={
            "Borrar": st.column_config.CheckboxColumn(
                "● Borrar",
                help="Marca esta fila si quieres borrarla.",
                default=False,
            )
        },
        key=f"{key_prefix}_{session_key}_delete_grid"
    )

    selected_rows = edited_delete_df[edited_delete_df["Borrar"] == True]
    selected_indexes = selected_rows["Fila original"].astype(int).tolist()

    if selected_indexes:
        st.warning(f"Seleccionaste {len(selected_indexes)} registro(s) para borrar de {title}.")
        st.dataframe(
            selected_rows.drop(columns=["Borrar"]),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Marca uno o más registros en la columna ● Borrar.")

    confirm = st.checkbox(
        f"Confirmo que quiero borrar {len(selected_indexes)} registro(s) de {title}",
        key=f"{key_prefix}_{session_key}_confirm"
    )

    if st.button(
        f"Borrar registros marcados de {title}",
        key=f"{key_prefix}_{session_key}_button",
        disabled=not selected_indexes or not confirm
    ):
        deleted = delete_rows_by_indexes(session_key, selected_indexes)
        st.success(f"Se borraron {deleted} registro(s) de {title}.")
        st.rerun()


def import_excel(file):
    xls = pd.ExcelFile(file)

    sheet_map = {
        "Clientes": "clientes",
        "Empleados": "empleados",
        "Citas": "citas",
        "Inventario": "inventario",
        "Gastos": "gastos",
        "Catalogo": "catalogo",
        "Ventas": "ventas",
        "Usuarios": "usuarios",
    }

    imported_sheets = []

    for sheet, key in sheet_map.items():
        if sheet in xls.sheet_names:
            st.session_state[key] = pd.read_excel(file, sheet_name=sheet)
            imported_sheets.append(sheet)

    if "Integraciones" in xls.sheet_names:
        integraciones = pd.read_excel(file, sheet_name="Integraciones")
        if not integraciones.empty:
            st.session_state.social_integrations = integraciones.iloc[0].to_dict()
            imported_sheets.append("Integraciones")

    ensure_cita_ids()
    return imported_sheets


def render_excel_emergency_import_export():
    st.markdown("### Excel de emergencia")
    st.info("Descarga una hoja en blanco con todos los headers correctos. En una emergencia puedes llenar ese Excel y volverlo a subir aquí.")

    e1, e2 = st.columns(2)

    with e1:
        st.download_button(
            "Descargar Excel en blanco con headers",
            data=export_blank_excel_template(),
            file_name="valentina_studio_template_en_blanco.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_blank_excel_template"
        )

    with e2:
        st.download_button(
            "Descargar backup completo actual",
            data=export_excel(),
            file_name=f"valentina_studio_backup_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_full_excel_from_emergency"
        )

    st.divider()
    st.markdown("### Subir datos desde Excel")
    st.warning("Esto puede reemplazar tablas actuales con las hojas que vengan en el Excel. Primero descarga un backup completo antes de importar.")

    uploaded_excel = st.file_uploader(
        "Subir Excel de backup o plantilla llena",
        type=["xlsx"],
        key="emergency_excel_upload"
    )

    confirm_import = st.checkbox(
        "Confirmo que ya hice backup y quiero importar este Excel",
        key="emergency_excel_import_confirm"
    )

    if st.button(
        "Importar datos desde Excel",
        disabled=uploaded_excel is None or not confirm_import,
        key="emergency_excel_import_button"
    ):
        try:
            imported_sheets = import_excel(uploaded_excel)
            if imported_sheets:
                st.success("Datos importados: " + ", ".join(imported_sheets))
            else:
                st.warning("No se importó nada. Revisa que el Excel tenga hojas con nombres como Clientes, Citas, Ventas, Inventario, Gastos, Catalogo, Empleados o Usuarios.")
            st.rerun()
        except Exception as exc:
            st.error(f"No se pudo importar el Excel. Revisa el formato. Error: {exc}")


st.markdown(
    """
    <div class="top-app-header">
        <div class="app-title">VALENTINA STUDIO</div>
        <div class="small-muted">High-tech salon command center · agenda, clientes, ventas, booking, reportes y finanzas</div>
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()
run_hidden_hourly_auto_backup()
st.markdown(
    "<meta http-equiv='refresh' content='3600'>",
    unsafe_allow_html=True
)
render_backup_banner()
st.divider()


st.sidebar.markdown("""
<div class="sidebar-brand-card">
    <div class="sidebar-brand-title">Valentina Studio</div>
    <div class="sidebar-brand-subtitle">Salon OS · Neon Mode</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Usuario / Rol")

roles_disponibles = ["Admin", "Recepción", "Empleada"]

current_role = st.sidebar.selectbox(
    "Entrar como",
    roles_disponibles,
    index=0,
    key="current_role_selector"
)

st.session_state.current_role = current_role

st.sidebar.markdown("### Visual mode")
visual_mode = st.sidebar.selectbox(
    "Theme",
    ["Purple Mode", "Pink Mode"],
    index=0,
    key="visual_mode_selector"
)
st.session_state.visual_mode = visual_mode

if visual_mode == "Pink Mode":
    st.markdown("""
    <style>
    :root {
        --bg-main: #fff4f8;
        --panel-dark: #fff7fb;
        --panel-mid: #ffffff;
        --text-main: #331522;
        --text-muted: #7b5265;
        --neon-pink: #ff4fa3;
        --neon-purple: #c65cff;
        --neon-cyan: #ff8cc8;
        --glass-border: rgba(119, 28, 72, 0.16);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 15% 0%, rgba(255,79,163,0.22), transparent 32%),
            radial-gradient(circle at 85% 10%, rgba(255,140,200,0.22), transparent 30%),
            radial-gradient(circle at 50% 100%, rgba(198,92,255,0.12), transparent 36%),
            #fff4f8 !important;
        color: #331522 !important;
    }

    [data-testid="stHeader"] {
        background: rgba(255,244,248,0.50) !important;
        backdrop-filter: blur(18px);
    }

    .top-app-header,
    .fresha-hero,
    .fresha-stat-card,
    .appointment-card,
    .day-box {
        background: linear-gradient(135deg, rgba(255,255,255,0.82), rgba(255,232,243,0.58)) !important;
        border-color: rgba(119, 28, 72, 0.14) !important;
        box-shadow: 0px 18px 48px rgba(160, 50, 100, 0.13), inset 0 1px 0 rgba(255,255,255,0.72) !important;
    }

    .quick-action-box {
        background: linear-gradient(135deg, rgba(255,79,163,0.14), rgba(255,255,255,0.78)) !important;
        border-color: rgba(255,79,163,0.22) !important;
        color: #331522 !important;
    }

    .app-title,
    .fresha-title,
    .fresha-stat-value,
    .appointment-client,
    h1, h2, h3, h4, h5, h6 {
        color: #331522 !important;
        text-shadow: none !important;
    }

    .small-muted,
    .fresha-subtitle,
    .fresha-stat-label,
    .appointment-meta,
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div,
    label, p, span, div[data-testid="stText"], div[data-testid="stCaptionContainer"] {
        color: #6f4a5c !important;
    }

    .appointment-time {
        color: #d81b72 !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffeaf4 0%, #fff8fb 100%) !important;
        border-right: 1px solid rgba(119, 28, 72, 0.14) !important;
        box-shadow: 18px 0 55px rgba(160, 50, 100, 0.13) !important;
    }

    .sidebar-brand-card {
        background:
            radial-gradient(circle at 0% 0%, rgba(255,255,255,0.85), transparent 35%),
            radial-gradient(circle at 100% 0%, rgba(255,79,163,0.35), transparent 38%),
            linear-gradient(135deg, #ff4fa3, #ff8cc8) !important;
        border-color: rgba(255,255,255,0.75) !important;
        box-shadow: 0px 18px 48px rgba(255,79,163,0.26) !important;
    }

    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] [role="radiogroup"] label p,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #331522 !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(255,255,255,0.78) !important;
        border-color: rgba(119, 28, 72, 0.13) !important;
        box-shadow: 0px 6px 18px rgba(160, 50, 100, 0.10) !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
        border-color: rgba(255,79,163,0.50) !important;
        background: #fff2f8 !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, #ff4fa3, #c65cff) !important;
        border-color: rgba(255,255,255,0.55) !important;
        box-shadow: 0px 10px 28px rgba(255,79,163,0.28) !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border-color: rgba(119, 28, 72, 0.16) !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] *,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    input, textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        color: #331522 !important;
    }

    .stButton > button, .stDownloadButton > button, div[data-testid="stLinkButton"] a {
        background: linear-gradient(135deg, #ff4fa3, #c65cff) !important;
        color: #ffffff !important;
        box-shadow: 0px 12px 26px rgba(255,79,163,0.22) !important;
    }

    .pill-confirmada { background: rgba(255,79,163,0.12) !important; color: #c2185b !important; border: 1px solid rgba(255,79,163,0.32) !important; }
    .pill-pendiente { background: rgba(255,193,7,0.16) !important; color: #9a6900 !important; border: 1px solid rgba(255,193,7,0.35) !important; }
    .pill-cancelada { background: rgba(229,57,53,0.12) !important; color: #b3261e !important; border: 1px solid rgba(229,57,53,0.30) !important; }
    .pill-completada { background: rgba(198,92,255,0.14) !important; color: #7b2cbf !important; border: 1px solid rgba(198,92,255,0.30) !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .theme-mode-note::after { content: "Purple Mode active"; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.caption(f"Rol activo: {current_role} · {visual_mode}")

allowed_menus = get_allowed_menus(current_role)
menu_display = st.sidebar.radio(
    "Menú principal",
    [menu_label(item) for item in allowed_menus],
    label_visibility="collapsed"
)
menu = clean_menu_label(menu_display)


if st.session_state.get("current_role", "Admin") == "Admin":
    with st.expander("🧹 Borrar datos incorrectos de pruebas", expanded=False):
        st.warning("Primero respalda. Después selecciona solamente los registros incorrectos. Nada se borra hasta marcar la confirmación.")

        cleanup_tabs = st.tabs([
            "Citas",
            "Clientes",
            "Ventas",
            "Servicios",
            "Empleados",
            "Inventario",
            "Gastos",
            "Usuarios"
        ])

        with cleanup_tabs[0]:
            render_delete_rows_tool("Citas", "citas", label_column="Cliente", key_prefix="global_cleanup")
        with cleanup_tabs[1]:
            render_delete_rows_tool("Clientes", "clientes", label_column="Nombre", key_prefix="global_cleanup")
        with cleanup_tabs[2]:
            render_delete_rows_tool("Ventas", "ventas", label_column="Cliente", key_prefix="global_cleanup")
        with cleanup_tabs[3]:
            render_delete_rows_tool("Servicios", "catalogo", label_column="Servicio", key_prefix="global_cleanup")
        with cleanup_tabs[4]:
            render_delete_rows_tool("Empleados", "empleados", label_column="Nombre", key_prefix="global_cleanup")
        with cleanup_tabs[5]:
            render_delete_rows_tool("Inventario", "inventario", label_column="Producto", key_prefix="global_cleanup")
        with cleanup_tabs[6]:
            render_delete_rows_tool("Gastos", "gastos", label_column="Concepto", key_prefix="global_cleanup")
        with cleanup_tabs[7]:
            render_delete_rows_tool("Usuarios", "usuarios", label_column="Usuario", key_prefix="global_cleanup")

    st.divider()


if menu == "Inicio":
    render_fresha_hero(
        "Inicio del estudio",
        "Vista rápida tipo Fresha: ventas, próximas citas, clientes y accesos rápidos."
    )

    citas = st.session_state.citas.copy()
    ventas = st.session_state.ventas.copy()
    gastos = st.session_state.gastos.copy()
    inventario = st.session_state.inventario.copy()

    ventas["Total"] = pd.to_numeric(ventas["Total"], errors="coerce").fillna(0)
    gastos["Monto"] = pd.to_numeric(gastos["Monto"], errors="coerce").fillna(0)
    citas["Costo materiales"] = pd.to_numeric(
        citas["Costo materiales"],
        errors="coerce"
    ).fillna(0)
    inventario["Cantidad"] = pd.to_numeric(
        inventario["Cantidad"],
        errors="coerce"
    ).fillna(0)
    inventario["Minimo"] = pd.to_numeric(
        inventario["Minimo"],
        errors="coerce"
    ).fillna(0)

    citas_hoy = citas[citas["Fecha"].astype(str) == str(date.today())]

    ingresos = ventas["Total"].sum()
    gastos_total = gastos["Monto"].sum()
    materiales = citas["Costo materiales"].sum()
    ganancia = ingresos - gastos_total - materiales

    bajos = inventario[inventario["Cantidad"] <= inventario["Minimo"]]

    s1, s2, s3, s4 = responsive_columns(4, ipad_count=4, mobile_count=4)

    with s1:
        render_stat_card("Ventas", money(ingresos), "Total registrado")
    with s2:
        render_stat_card("Citas de hoy", len(citas_hoy), "Servicios agendados")
    with s3:
        render_stat_card("Clientes", len(st.session_state.clientes), "Base de datos")
    with s4:
        render_stat_card("Ganancia estimada", money(ganancia), "Ventas - gastos - materiales")

    if get_device_mode() == "desktop":
        left, right = st.columns([1.4, 1])
    else:
        left, right = st.columns(2)

    with left:
        st.markdown("### Agenda de hoy")

        if citas_hoy.empty:
            st.info("No hay citas para hoy.")
        else:
            for _, row in citas_hoy.sort_values("Hora").iterrows():
                render_appointment_card(row)
                render_whatsapp_buttons(row)

    with right:
        st.markdown("### Acciones rápidas")

        st.markdown("""
        <div class="quick-action-box">
        <b>Flujo recomendado</b><br>
        1. Agrega cliente<br>
        2. Agenda cita<br>
        3. Confirma por WhatsApp<br>
        4. Cobra en Ventas<br>
        5. Revisa Reportes
        </div>
        """, unsafe_allow_html=True)

        if not bajos.empty:
            st.warning("Productos bajos en inventario")
            st.dataframe(bajos, use_container_width=True)
        else:
            st.success("Inventario sin alertas críticas.")


elif menu == "Agenda Fresha":
    render_fresha_hero(
        "Agenda Fresha",
        "Vista diaria con filtros, detalles del cliente y acciones rápidas."
    )

    citas = st.session_state.citas.copy()

    empleados_activos = st.session_state.empleados[
        st.session_state.empleados["Activo"] == True
    ]["Nombre"].tolist()

    top1, top2, top3 = responsive_columns(3, ipad_count=3, mobile_count=1)

    with top1:
        fecha_agenda = st.date_input(
            "Fecha de agenda",
            value=date.today(),
            key="agenda_fecha"
        )
    with top2:
        filtro_empleado = st.selectbox(
            "Profesional",
            ["Todas"] + empleados_activos,
            key="agenda_empleado"
        )
    with top3:
        filtro_estado = st.selectbox(
            "Estado",
            ["Todos", "Confirmada", "Pendiente", "Cancelada", "Completada"],
            key="agenda_estado"
        )

    busqueda = st.text_input("Buscar cliente, servicio o notas", key="agenda_busqueda")

    citas_dia = citas[citas["Fecha"].astype(str) == str(fecha_agenda)]

    if filtro_empleado != "Todas":
        citas_dia = citas_dia[citas_dia["Empleado"] == filtro_empleado]

    if filtro_estado != "Todos":
        citas_dia = citas_dia[citas_dia["Estado"] == filtro_estado]

    if busqueda:
        citas_dia = citas_dia[
            citas_dia.apply(
                lambda r: busqueda.lower() in " ".join([str(v) for v in r.values]).lower(),
                axis=1
            )
        ]

    k1, k2, k3 = responsive_columns(3, ipad_count=3, mobile_count=1)

    with k1:
        render_stat_card("Citas", len(citas_dia), "Resultado actual")
    with k2:
        total_est = pd.to_numeric(
            citas_dia.get("Precio", 0),
            errors="coerce"
        ).fillna(0).sum()
        render_stat_card("Ventas estimadas", money(total_est), "Según filtros")
    with k3:
        clientes_unicos = citas_dia["Cliente"].nunique() if not citas_dia.empty else 0
        render_stat_card("Clientes únicos", clientes_unicos, "En vista")

    if get_device_mode() == "desktop":
        agenda_col, detalle_col = st.columns([1.4, 1])
    else:
        agenda_col, detalle_col = st.columns(2)

    with agenda_col:
        st.markdown("### Timeline del día")

        if citas_dia.empty:
            st.info("No hay citas con esos filtros.")
        else:
            for _, row in citas_dia.sort_values("Hora").iterrows():
                render_appointment_card(row)
                with st.expander(f"Opciones: {row['Cliente']} · {row['Hora']} · {row.get('Cita ID', '')}"):
                    cliente_info = get_client_info(row["Cliente"])

                    if cliente_info is not None:
                        st.write(f"**Teléfono:** {cliente_info.get('Telefono', '')}")
                        st.write(f"**Email:** {cliente_info.get('Email', '')}")
                        st.write(f"**Perfil:** {cliente_info.get('Notas', '')}")

                    st.write(f"**Servicio:** {row['Servicio']}")
                    st.write(f"**Diseño:** {row['Diseno']}")
                    st.write(f"**Materiales:** {row['Materiales']}")
                    st.write(f"**Precio:** {money(row['Precio'])}")
                    st.write(f"**Estado:** {row['Estado']}")
                    st.write(f"**Notas:** {row['Notas']}")
                    render_whatsapp_buttons(row)

                    st.divider()
                    st.caption(f"ID de cita: {row.get('Cita ID', '')}")
                    if st.button(
                        "Borrar esta cita",
                        key=f"delete_calendar_day_{row.get('Cita ID', row.name)}"
                    ):
                        delete_cita_by_id(row.get("Cita ID", ""))
                        st.success("Cita borrada correctamente.")
                        st.rerun()

                with st.expander(f"Abrir cita: {row['Cliente']} · {row['Hora']}"):
                    cliente_info = get_client_info(row["Cliente"])

                    if cliente_info is not None:
                        st.write(f"**Teléfono:** {cliente_info.get('Telefono', '')}")
                        st.write(f"**Email:** {cliente_info.get('Email', '')}")
                        st.write(f"**Perfil:** {cliente_info.get('Notas', '')}")

                    st.write(f"**Servicio:** {row['Servicio']}")
                    st.write(f"**Diseño:** {row['Diseno']}")
                    st.write(f"**Materiales:** {row['Materiales']}")
                    st.write(f"**Precio:** {money(row['Precio'])}")
                    st.write(f"**Estado:** {row['Estado']}")
                    st.write(f"**Notas:** {row['Notas']}")
                    render_whatsapp_buttons(row)

                    st.divider()
                    st.caption(f"ID de cita: {row.get('Cita ID', '')}")
                    if st.button(
                        "Borrar esta cita",
                        key=f"delete_agenda_{row.get('Cita ID', row.name)}"
                    ):
                        delete_cita_by_id(row.get("Cita ID", ""))
                        st.success("Cita borrada correctamente.")
                        st.rerun()

    with detalle_col:
        st.markdown("### Vista por profesional")

        for emp in empleados_activos:
            emp_citas = citas_dia[citas_dia["Empleado"] == emp]

            with st.expander(f"{emp} · {len(emp_citas)} citas", expanded=True):
                if emp_citas.empty:
                    st.caption("Sin citas")
                else:
                    for _, row in emp_citas.sort_values("Hora").iterrows():
                        render_appointment_card(row, compact=True)


elif menu == "Calendario":
    render_fresha_hero(
        "Calendario",
        "Vista flexible de citas por año, mes, semana o día."
    )

    citas = st.session_state.citas.copy()
    citas["Fecha_dt"] = pd.to_datetime(citas["Fecha"], errors="coerce")
    citas = citas.dropna(subset=["Fecha_dt"])

    empleados_activos = st.session_state.empleados[
        st.session_state.empleados["Activo"] == True
    ]["Nombre"].tolist()

    vista = st.radio(
        "Vista del calendario",
        ["Día", "Semana", "Mes", "Año"],
        horizontal=True,
        key="calendario_tipo_vista"
    )

    filtro_empleado = st.selectbox(
        "Filtrar por empleada",
        ["Todas"] + empleados_activos,
        key="calendario_filtro_empleado"
    )

    if filtro_empleado != "Todas":
        citas = citas[citas["Empleado"] == filtro_empleado]

    if vista == "Día":
        fecha_dia = st.date_input(
            "Selecciona día",
            value=date.today(),
            key="cal_dia"
        )

        citas_dia = citas[citas["Fecha_dt"].dt.date == fecha_dia]

        render_stat_card(
            "Citas del día",
            len(citas_dia),
            fecha_dia.strftime("%d/%m/%Y")
        )

        if citas_dia.empty:
            st.info("No hay citas para este día.")
        else:
            for _, row in citas_dia.sort_values("Hora").iterrows():
                render_appointment_card(row)

    elif vista == "Semana":
        fecha_base = st.date_input(
            "Semana de",
            value=date.today(),
            key="cal_semana"
        )

        inicio_semana = fecha_base - timedelta(days=fecha_base.weekday())
        dias = [inicio_semana + timedelta(days=i) for i in range(7)]
        dias_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        cols = st.columns(7)

        for i, dia in enumerate(dias):
            with cols[i]:
                st.markdown(
                    f'<div class="day-box"><b>{dias_es[i]}</b><br>{dia.strftime("%d/%m/%Y")}<hr>',
                    unsafe_allow_html=True
                )

                citas_dia = citas[citas["Fecha_dt"].dt.date == dia]

                if citas_dia.empty:
                    st.caption("Sin citas")
                else:
                    for _, row in citas_dia.sort_values("Hora").iterrows():
                        render_appointment_card(row, compact=True)

                st.markdown("</div>", unsafe_allow_html=True)

    elif vista == "Mes":
        hoy = date.today()

        meses_nombre = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        col_mes, col_anio = st.columns(2)

        with col_mes:
            mes = st.selectbox(
                "Mes",
                list(range(1, 13)),
                index=hoy.month - 1,
                format_func=lambda x: meses_nombre[x - 1],
                key="cal_mes"
            )

        with col_anio:
            anio = st.number_input(
                "Año",
                min_value=2020,
                max_value=2035,
                value=hoy.year,
                step=1,
                key="cal_anio_mes"
            )

        citas_mes = citas[
            (citas["Fecha_dt"].dt.month == mes) &
            (citas["Fecha_dt"].dt.year == int(anio))
        ]

        render_stat_card("Citas del mes", len(citas_mes), "Total mensual")

        cal = calendar.Calendar(firstweekday=0)
        semanas = cal.monthdatescalendar(int(anio), int(mes))

        for semana in semanas:
            cols = st.columns(7)

            for _, dia in enumerate(semana):
                with cols[_]:
                    opacity = "0.35" if dia.month != mes else "1"
                    citas_dia = citas_mes[citas_mes["Fecha_dt"].dt.date == dia]

                    st.markdown(
                        f'<div class="day-box" style="opacity:{opacity};"><b>{dia.day}</b><br><span class="small-muted">{len(citas_dia)} citas</span><hr>',
                        unsafe_allow_html=True
                    )

                    for _, row in citas_dia.sort_values("Hora").head(3).iterrows():
                        render_appointment_card(row, compact=True)

                    st.markdown("</div>", unsafe_allow_html=True)

    else:
        anio = st.number_input(
            "Selecciona año",
            min_value=2020,
            max_value=2035,
            value=date.today().year,
            step=1,
            key="cal_anio"
        )

        citas_anio = citas[citas["Fecha_dt"].dt.year == int(anio)]

        meses_nombre = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        rows = []

        for m in range(1, 13):
            citas_m = citas_anio[citas_anio["Fecha_dt"].dt.month == m]

            rows.append({
                "Mes": meses_nombre[m - 1],
                "Citas": len(citas_m),
                "Clientes únicos": citas_m["Cliente"].nunique() if not citas_m.empty else 0,
                "Ventas estimadas": pd.to_numeric(
                    citas_m.get("Precio", 0),
                    errors="coerce"
                ).fillna(0).sum()
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=True)


elif menu == "Nueva cita":
    render_fresha_hero(
        "Nueva cita",
        "Agenda una cita nueva y déjala lista para confirmar por WhatsApp."
    )

    clientes_lista = st.session_state.clientes["Nombre"].tolist()

    empleados_lista = st.session_state.empleados[
        st.session_state.empleados["Activo"] == True
    ]["Nombre"].tolist()

    catalogo = st.session_state.catalogo.copy()
    servicios_lista = catalogo[catalogo["Activo"] == True]["Servicio"].tolist()

    with st.form("form_nueva_cita"):
        c1, c2, c3 = responsive_columns(3, ipad_count=3, mobile_count=1)

        with c1:
            fecha_cita = st.date_input("Fecha", value=date.today())
            hora_cita = st.time_input("Hora", value=time(10, 0))
            cliente_cita = st.selectbox("Cliente", clientes_lista)

        with c2:
            empleado_cita = st.selectbox("Empleado", empleados_lista)
            servicio_cita = st.selectbox("Servicio", servicios_lista)
            estado_cita = st.selectbox(
                "Estado",
                ["Pendiente", "Confirmada", "Completada", "Cancelada"]
            )

        with c3:
            match = catalogo[catalogo["Servicio"] == servicio_cita]
            precio_sugerido = float(match.iloc[0]["Precio"]) if not match.empty else 0.0
            precio = st.number_input("Precio", min_value=0.0, value=precio_sugerido)
            costo_materiales = st.number_input("Costo materiales", min_value=0.0, value=0.0)

        diseno = st.text_input("Diseño / tipo de trabajo")
        materiales = st.text_input("Materiales a usar")
        notas = st.text_area("Notas")

        guardar = st.form_submit_button("Guardar cita")

    if guardar:
        nueva = pd.DataFrame([{
            "Cita ID": next_cita_id(),
            "Fecha": str(fecha_cita),
            "Hora": hora_cita.strftime("%H:%M"),
            "Cliente": cliente_cita,
            "Empleado": empleado_cita,
            "Servicio": servicio_cita,
            "Diseno": diseno,
            "Materiales": materiales,
            "Costo materiales": costo_materiales,
            "Precio": precio,
            "Estado": estado_cita,
            "Notas": notas
        }])

        st.session_state.citas = pd.concat(
            [st.session_state.citas, nueva],
            ignore_index=True
        )

        st.success("Cita guardada correctamente.")


elif menu == "Ventas":
    render_fresha_hero(
        "Ventas",
        "Registra pagos, revisa ventas del día y conecta cada venta con una cita o servicio."
    )

    ventas = st.session_state.ventas.copy()
    ventas["Total"] = pd.to_numeric(ventas["Total"], errors="coerce").fillna(0)
    ventas["Fecha_dt"] = pd.to_datetime(ventas["Fecha"], errors="coerce")

    ventas_hoy = ventas[ventas["Fecha_dt"].dt.date == date.today()]

    c1, c2, c3, c4 = responsive_columns(4, ipad_count=4, mobile_count=4)

    with c1:
        render_stat_card("Ventas hoy", money(ventas_hoy["Total"].sum()), "Total cobrado hoy")
    with c2:
        render_stat_card("Tickets hoy", len(ventas_hoy), "Ventas registradas")
    with c3:
        promedio = ventas_hoy["Total"].mean() if not ventas_hoy.empty else 0
        render_stat_card("Venta promedio", money(promedio), "Promedio por ticket")
    with c4:
        render_stat_card("Ventas totales", money(ventas["Total"].sum()), "Histórico")

    tab1, tab2 = st.tabs(["Nueva venta", "Historial de ventas"])

    with tab1:
        catalogo = st.session_state.catalogo.copy()
        clientes_lista = st.session_state.clientes["Nombre"].tolist()

        empleados_lista = st.session_state.empleados[
            st.session_state.empleados["Activo"] == True
        ]["Nombre"].tolist()

        servicios_lista = catalogo[catalogo["Activo"] == True]["Servicio"].tolist()

        with st.form("form_venta"):
            v1, v2, v3 = responsive_columns(3, ipad_count=3, mobile_count=1)

            with v1:
                fecha_venta = st.date_input("Fecha", value=date.today(), key="venta_fecha")
                cliente_venta = st.selectbox("Cliente", clientes_lista, key="venta_cliente")
                empleado_venta = st.selectbox("Empleado", empleados_lista, key="venta_empleado")

            with v2:
                servicio_venta = st.selectbox("Servicio", servicios_lista, key="venta_servicio")
                metodo_pago = st.selectbox(
                    "Método de pago",
                    ["Efectivo", "Tarjeta", "Zelle", "Cash App", "Otro"]
                )
                descuento = st.number_input("Descuento", min_value=0.0, value=0.0)

            with v3:
                match = catalogo[catalogo["Servicio"] == servicio_venta]
                precio_sugerido = float(match.iloc[0]["Precio"]) if not match.empty else 0.0
                subtotal = st.number_input("Subtotal", min_value=0.0, value=precio_sugerido)
                total = max(subtotal - descuento, 0)
                st.metric("Total", money(total))

            notas_venta = st.text_area("Notas de venta")
            guardar_venta = st.form_submit_button("Guardar venta")

        if guardar_venta:
            nueva_venta = pd.DataFrame([{
                "Fecha": str(fecha_venta),
                "Cliente": cliente_venta,
                "Servicio": servicio_venta,
                "Empleado": empleado_venta,
                "Metodo pago": metodo_pago,
                "Subtotal": subtotal,
                "Descuento": descuento,
                "Total": total,
                "Notas": notas_venta
            }])

            st.session_state.ventas = pd.concat(
                [st.session_state.ventas, nueva_venta],
                ignore_index=True
            )

            st.success("Venta registrada correctamente.")

    with tab2:
        st.dataframe(st.session_state.ventas, use_container_width=True)


elif menu == "Lista de clientes":
    render_fresha_hero(
        "Lista de clientes",
        "Base de datos de clientes, cumpleaños, notas y contacto."
    )

    tab1, tab2 = st.tabs(["Clientes", "Agregar cliente"])

    with tab1:
        editado = st.data_editor(
            st.session_state.clientes,
            use_container_width=True,
            num_rows="dynamic"
        )

        if st.button("Guardar cambios de clientes"):
            st.session_state.clientes = editado
            st.success("Clientes actualizados.")

    with tab2:
        with st.form("form_cliente"):
            nombre = st.text_input("Nombre")
            telefono = st.text_input("Teléfono")
            email = st.text_input("Email")
            cumple = st.text_input("Cumpleaños", placeholder="YYYY-MM-DD")
            notas = st.text_area("Notas / perfil del cliente")
            guardar_cliente = st.form_submit_button("Guardar cliente")

        if guardar_cliente and nombre:
            nuevo = pd.DataFrame([{
                "Nombre": nombre,
                "Telefono": telefono,
                "Email": email,
                "Cumpleanos": cumple,
                "Notas": notas
            }])

            st.session_state.clientes = pd.concat(
                [st.session_state.clientes, nuevo],
                ignore_index=True
            )

            st.success("Cliente agregado.")


elif menu == "Catálogo":
    render_fresha_hero(
        "Catálogo",
        "Servicios, precios, duración y disponibilidad para citas y online booking."
    )

    tab1, tab2 = st.tabs(["Servicios", "Agregar servicio"])

    with tab1:
        catalogo_editado = st.data_editor(
            st.session_state.catalogo,
            use_container_width=True,
            num_rows="dynamic"
        )

        if st.button("Guardar cambios del catálogo"):
            st.session_state.catalogo = catalogo_editado
            st.success("Catálogo actualizado.")

    with tab2:
        with st.form("form_servicio_catalogo"):
            c1, c2, c3 = responsive_columns(3, ipad_count=3, mobile_count=1)

            with c1:
                servicio = st.text_input("Nombre del servicio")
                categoria = st.text_input("Categoría", "Manos")

            with c2:
                duracion = st.number_input("Duración min", min_value=5, value=60, step=5)
                precio = st.number_input("Precio", min_value=0.0, value=50.0)

            with c3:
                activo = st.checkbox("Activo", value=True)

            descripcion = st.text_area("Descripción")

            guardar_servicio = st.form_submit_button("Guardar servicio")

        if guardar_servicio and servicio:
            nuevo_servicio = pd.DataFrame([{
                "Servicio": servicio,
                "Categoria": categoria,
                "Duracion min": duracion,
                "Precio": precio,
                "Activo": activo,
                "Descripcion": descripcion
            }])

            st.session_state.catalogo = pd.concat(
                [st.session_state.catalogo, nuevo_servicio],
                ignore_index=True
            )

            st.success("Servicio agregado al catálogo.")


elif menu == "Online booking":
    render_fresha_hero(
        "Online booking",
        "Simulación de reservas online para clientes. Las solicitudes entran como citas pendientes."
    )

    settings = st.session_state.app_settings

    if not settings.get("online_booking_activo", True):
        st.warning("Online booking está desactivado en Settings.")

    catalogo = st.session_state.catalogo.copy()
    servicios_activos = catalogo[catalogo["Activo"] == True]

    empleados_activos = st.session_state.empleados[
        st.session_state.empleados["Activo"] == True
    ]["Nombre"].tolist()

    with st.form("form_online_booking"):
        b1, b2, b3 = responsive_columns(3, ipad_count=3, mobile_count=1)

        with b1:
            cliente_nombre = st.text_input("Nombre del cliente")
            cliente_telefono = st.text_input("Teléfono")
            cliente_email = st.text_input("Email")

        with b2:
            servicio_online = st.selectbox("Servicio", servicios_activos["Servicio"].tolist())
            empleado_online = st.selectbox(
                "Profesional preferido",
                ["Sin preferencia"] + empleados_activos
            )

        with b3:
            fecha_online = st.date_input("Fecha deseada", value=date.today())
            hora_online = st.time_input("Hora deseada", value=time(10, 0))

        notas_online = st.text_area("Notas / diseño que desea")
        enviar_solicitud = st.form_submit_button("Solicitar cita")

    if enviar_solicitud and cliente_nombre:
        if cliente_nombre not in st.session_state.clientes["Nombre"].tolist():
            nuevo_cliente = pd.DataFrame([{
                "Nombre": cliente_nombre,
                "Telefono": cliente_telefono,
                "Email": cliente_email,
                "Cumpleanos": "",
                "Notas": "Cliente agregado desde online booking"
            }])

            st.session_state.clientes = pd.concat(
                [st.session_state.clientes, nuevo_cliente],
                ignore_index=True
            )

        empleado_final = (
            empleados_activos[0]
            if empleado_online == "Sin preferencia" and empleados_activos
            else empleado_online
        )

        match = servicios_activos[servicios_activos["Servicio"] == servicio_online]
        precio_servicio = float(match.iloc[0]["Precio"]) if not match.empty else 0.0

        nueva_cita = pd.DataFrame([{
            "Cita ID": next_cita_id(),
            "Fecha": str(fecha_online),
            "Hora": hora_online.strftime("%H:%M"),
            "Cliente": cliente_nombre,
            "Empleado": empleado_final,
            "Servicio": servicio_online,
            "Diseno": notas_online,
            "Materiales": "",
            "Costo materiales": 0.0,
            "Precio": precio_servicio,
            "Estado": "Pendiente",
            "Notas": "Solicitud creada desde online booking"
        }])

        st.session_state.citas = pd.concat(
            [st.session_state.citas, nueva_cita],
            ignore_index=True
        )

        st.success("Solicitud recibida. La cita quedó como Pendiente.")


elif menu == "Integraciones":
    render_fresha_hero(
        "Integraciones",
        "Conecta el online booking con redes sociales, Google, Meta y analítica."
    )

    social = st.session_state.social_integrations.copy()

    tab1, tab2, tab3 = st.tabs(["Booking links", "Redes sociales", "Tracking / Ads"])

    with tab1:
        st.subheader("Link público de reservas")
        st.caption("Este link se puede poner en Instagram bio, Facebook, Google Business Profile, TikTok o sitio web.")

        booking_link = st.text_input(
            "Booking link",
            value=social.get("booking_link", ""),
            key="integration_booking_link"
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Instagram bio**")
            st.code(booking_link or "Agrega tu link de booking", language="text")
        with c2:
            st.markdown("**Facebook button**")
            st.code(booking_link or "Agrega tu link de booking", language="text")
        with c3:
            st.markdown("**Google Business Profile**")
            st.code(booking_link or "Agrega tu link de booking", language="text")

        if booking_link:
            st.link_button("Abrir booking link", booking_link)

        st.divider()
        st.subheader("Google Reserve")

        google_reserve_enabled = st.checkbox(
            "Activar Google Reserve / Reserve with Google",
            value=social.get("google_reserve_enabled", False)
        )

        google_business_profile = st.text_input(
            "Google Business Profile URL",
            value=social.get("google_business_profile", "")
        )

        st.info("Por ahora esto guarda la configuración. La integración real con Reserve with Google requiere aprobación/API del proveedor o partner.")

    with tab2:
        st.subheader("Facebook e Instagram bookings")

        c1, c2 = st.columns(2)

        with c1:
            facebook_enabled = st.checkbox(
                "Activar Facebook booking",
                value=social.get("facebook_enabled", False)
            )

            facebook_page = st.text_input(
                "Facebook Page URL",
                value=social.get("facebook_page", "")
            )

        with c2:
            instagram_enabled = st.checkbox(
                "Activar Instagram booking",
                value=social.get("instagram_enabled", False)
            )

            instagram_profile = st.text_input(
                "Instagram Profile URL",
                value=social.get("instagram_profile", "")
            )

        c3, c4 = st.columns(2)

        with c3:
            tiktok_profile = st.text_input(
                "TikTok Profile URL",
                value=social.get("tiktok_profile", "")
            )

        with c4:
            website_url = st.text_input(
                "Website URL",
                value=social.get("website_url", "")
            )

        st.markdown("### Checklist para enlazar redes")

        st.markdown("""
        <div class="quick-action-box">
        <b>Pasos recomendados</b><br>
        1. Copia el booking link de Valentina Studio.<br>
        2. Pégalo en Instagram bio o botón de contacto.<br>
        3. Agrégalo como botón de reservar en Facebook Page.<br>
        4. Agrégalo en Google Business Profile como appointment link.<br>
        5. Usa Meta Pixel y Google Analytics para medir conversiones.
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.subheader("Meta Pixel Ads")

        meta_pixel_enabled = st.checkbox(
            "Activar Meta Pixel",
            value=social.get("meta_pixel_enabled", False)
        )

        meta_pixel_id = st.text_input(
            "Meta Pixel ID",
            value=social.get("meta_pixel_id", "")
        )

        st.subheader("Google Analytics")

        google_analytics_enabled = st.checkbox(
            "Activar Google Analytics",
            value=social.get("google_analytics_enabled", False)
        )

        google_analytics_id = st.text_input(
            "Google Analytics Measurement ID",
            value=social.get("google_analytics_id", ""),
            placeholder="G-XXXXXXXXXX"
        )

        st.caption("Esto deja guardados los IDs. Después se puede conectar a una página pública real de booking para disparar eventos de tracking y medición.")
