import json
import os
import streamlit as st

USER_FILE = "users.json"


def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {"admin": "admin123"}


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


st.set_page_config(
    page_title="SafeSwipe",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ── Init session state ──
if "users" not in st.session_state:
    st.session_state.users = load_users()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "history" not in st.session_state:
    st.session_state.history = []

# ── Global CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #060812 !important;
    color: #e2e8f0;
    font-family: 'DM Mono', monospace;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: #0b0f1e !important; border-right: 1px solid #1e2a45; }

.block-container { padding: 0 1rem 4rem !important; max-width: 720px !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #060812; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 99px; }

div[data-baseweb="input"] input,
div[data-baseweb="select"] div,
div[data-baseweb="select"] span {
    background: #0d1529 !important;
    color: #c9d6ef !important;
    border-color: #1e2e50 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 14px !important;
}
div[data-baseweb="select"] {
    background: #0d1529 !important;
    border: 1px solid #1e2e50 !important;
    border-radius: 10px !important;
}
div[data-baseweb="input"] {
    border-radius: 10px !important;
    border: 1px solid #1e2e50 !important;
    background: #0d1529 !important;
}
div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"]:focus-within {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
}

label, .stSelectbox label, .stNumberInput label {
    color: #5b7fa6 !important;
    font-size: 11px !important;
    font-family: 'DM Mono', monospace !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #0099cc 0%, #0066ff 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 28px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 24px rgba(0,102,255,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(0,153,204,0.5) !important;
}

.stDownloadButton > button {
    background: transparent !important;
    color: #00d4ff !important;
    border: 1px solid #00d4ff !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    padding: 12px 20px !important;
}
.stDownloadButton > button:hover {
    background: rgba(0,212,255,0.08) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #0b0f1e !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid #1a2540 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #4a6080 !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 8px 24px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #0d2044 !important;
    color: #00d4ff !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #0b0f1e !important;
    border: 1px solid #1a2540 !important;
    border-top: none !important;
    border-radius: 0 0 16px 16px !important;
    padding: 28px 24px !important;
}

[data-testid="stSidebarNav"] {
    display: none !important;
}
            
/* Dataframe styling */
[data-testid="stDataFrame"] {
    border: 1px solid #1a2540 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# ── Login page ──
if not st.session_state.logged_in:
    st.markdown("""
<style>
[data-testid="collapsedControl"] {
    display: none !important;
}

[data-testid="stSidebar"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding:60px 0 40px;text-align:center;">
        <div style="display:inline-flex;align-items:center;justify-content:center;width:72px;height:72px;
            background:linear-gradient(135deg,#0099cc,#0044ff);border-radius:20px;font-size:34px;
            margin-bottom:20px;box-shadow:0 8px 32px rgba(0,100,255,0.4);">🛡️</div>
        <h1 style="font-family:'Syne',sans-serif;font-size:40px;font-weight:800;color:#ffffff;
            letter-spacing:-0.02em;margin-bottom:6px;">SafeSwipe</h1>
        <p style="color:#3d5a80;font-family:'DM Mono',monospace;font-size:12px;
            letter-spacing:0.2em;text-transform:uppercase;">AI Fraud Detection Platform</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Sign In", "Create Account"])

    with tab1:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        username = st.text_input("Username", key="login_user", placeholder="Enter username")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Sign In →", key="btn_login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Access granted.")
                st.rerun()
            else:
                st.error("Invalid credentials.")

    with tab2:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        new_user = st.text_input("Username", key="reg_user", placeholder="Choose a username")
        new_pass = st.text_input("Password", type="password", key="reg_pass", placeholder="Choose a password")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Create Account →", key="btn_register"):
            if new_user in st.session_state.users:
                st.warning("Username already taken.")
            elif new_user == "" or new_pass == "":
                st.warning("All fields are required.")
            else:
                st.session_state.users[new_user] = new_pass
                save_users(st.session_state.users)
                st.success("Account created. Sign in above.")
    st.stop()

# ── Sidebar ──
with st.sidebar:
    total = len(st.session_state.history)
    frauds = sum(1 for h in st.session_state.history if h["Result"] == "Fraud")

    st.markdown(f"""
    <div style="margin-bottom:28px;">
        <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:white;margin-bottom:4px;">🛡️ SafeSwipe</div>
        <div style="font-family:'DM Mono',monospace;font-size:11px;color:#3d5a80;letter-spacing:.12em;text-transform:uppercase;">Fraud Detection</div>
    </div>
    <div style="background:#0d1529;border:1px solid #1a2540;border-radius:12px;padding:14px 16px;margin-bottom:20px;">
        <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase;margin-bottom:4px;">Signed in as</div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;color:#00d4ff;font-size:16px;">{st.session_state.username}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Navigation ──

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Analyze"

    pages = [
        ("⚡", "Analyze",   "Run fraud checks"),
        ("📋", "History",   "Past transactions"),
        ("📊", "Analytics", "Stats & insights"),
        ("⚙️", "Settings",  "Account & config"),
    ]

    for icon, name, desc in pages:
        is_active = st.session_state.active_page == name
        bg = "#0d2044" if is_active else "transparent"
        border = "1px solid #1e3a6e" if is_active else "1px solid transparent"
        color = "#00d4ff" if is_active else "#5b7fa6"
        if st.button(f"{icon}  {name}", key=f"nav_{name}"):
            st.session_state.active_page = name
            st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:grid;gap:8px;margin-bottom:20px;">
        <div style="background:#0d1529;border:1px solid #1a2540;border-radius:10px;padding:12px;">
            <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase;margin-bottom:2px;">Model</div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;color:white;font-size:13px;">Random Forest</div>
        </div>
        <div style="background:#0d1529;border:1px solid #1a2540;border-radius:10px;padding:12px;">
            <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase;margin-bottom:2px;">Accuracy</div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;color:#22c55e;font-size:13px;">98.0%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if total > 0:
        st.markdown(f"""
        <div style="border-top:1px solid #1a2540;padding-top:16px;margin-bottom:16px;">
            <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase;margin-bottom:10px;">Session Stats</div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="color:#5b7fa6;font-size:12px;font-family:'DM Mono',monospace;">Checked</span>
                <span style="color:white;font-size:14px;font-family:'Syne',sans-serif;font-weight:700;">{total}</span>
            </div>
            <div style="display:flex;justify-content:space-between;">
                <span style="color:#5b7fa6;font-size:12px;font-family:'DM Mono',monospace;">Flagged</span>
                <span style="color:#ef4444;font-size:14px;font-family:'Syne',sans-serif;font-weight:700;">{frauds}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Sign Out", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# ── Page routing ──
page = st.session_state.active_page

if page == "Analyze":
    from pages.analyze import show
    show()
elif page == "History":
    from pages.history import show
    show()
elif page == "Analytics":
    from pages.analytics import show
    show()
elif page == "Settings":
    from pages.settings import show
    show()
