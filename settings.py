import streamlit as st
import json
import os

USER_FILE = "users.json"


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


def section_header(title):
    st.markdown(f"""
    <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#3d5a80;
        letter-spacing:.2em;text-transform:uppercase;margin:28px 0 16px;
        display:flex;align-items:center;gap:8px;">
        <span style="display:inline-block;width:20px;height:2px;background:#00d4ff;border-radius:99px;"></span>
        {title}
    </div>
    """, unsafe_allow_html=True)


def show():
    st.markdown("""
    <div style="padding:48px 0 32px;border-bottom:1px solid #0f1a2e;margin-bottom:36px;">
        <div style="display:flex;align-items:center;gap:16px;">
            <div style="width:48px;height:48px;background:linear-gradient(135deg,#1a3a5c,#0d2244);
                border-radius:14px;display:flex;align-items:center;justify-content:center;
                font-size:24px;box-shadow:0 4px 20px rgba(0,30,100,0.5);flex-shrink:0;">⚙️</div>
            <div>
                <h1 style="font-family:'Syne',sans-serif;font-size:32px;font-weight:800;color:white;
                    letter-spacing:-0.02em;line-height:1;margin-bottom:4px;">Settings</h1>
                <p style="color:#3d5a80;font-family:'DM Mono',monospace;font-size:11px;
                    letter-spacing:.15em;text-transform:uppercase;">Account & configuration</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    username = st.session_state.username

    # ── Account info ──
    section_header("Account")
    st.markdown(f"""
    <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:16px;padding:20px 24px;margin-bottom:16px;">
        <div style="display:flex;align-items:center;justify-content:space-between;">
            <div>
                <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;
                    letter-spacing:.12em;text-transform:uppercase;margin-bottom:6px;">Signed in as</div>
                <div style="font-family:'Syne',sans-serif;font-weight:800;color:#00d4ff;font-size:22px;">{username}</div>
            </div>
            <div style="width:48px;height:48px;background:linear-gradient(135deg,#0099cc,#0044ff);
                border-radius:50%;display:flex;align-items:center;justify-content:center;
                font-family:'Syne',sans-serif;font-weight:800;color:white;font-size:20px;">
                {username[0].upper()}
            </div>
        </div>
        <div style="border-top:1px solid #1a2540;margin-top:16px;padding-top:14px;
            display:flex;gap:24px;">
            <div>
                <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;
                    letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;">Transactions</div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:white;font-size:18px;">
                    {len(st.session_state.history)}</div>
            </div>
            <div>
                <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;
                    letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;">Fraud Flagged</div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:#f87171;font-size:18px;">
                    {sum(1 for h in st.session_state.history if h['Result'] == 'Fraud')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Change password ──
    section_header("Change Password")
    st.markdown("""
    <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:16px;padding:24px;margin-bottom:8px;">
    """, unsafe_allow_html=True)

    current_pass = st.text_input("Current Password", type="password", key="cur_pass", placeholder="••••••••")
    new_pass = st.text_input("New Password", type="password", key="new_pass", placeholder="At least 6 characters")
    confirm_pass = st.text_input("Confirm New Password", type="password", key="conf_pass", placeholder="Repeat new password")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("Update Password", key="update_pass_btn"):
        users = st.session_state.users
        if users.get(username) != current_pass:
            st.error("Current password is incorrect.")
        elif len(new_pass) < 6:
            st.warning("New password must be at least 6 characters.")
        elif new_pass != confirm_pass:
            st.warning("Passwords do not match.")
        else:
            users[username] = new_pass
            st.session_state.users = users
            save_users(users)
            st.success("Password updated successfully.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Detection preferences ──
    section_header("Detection Preferences")
    st.markdown("""
    <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:16px;padding:24px;margin-bottom:8px;">
    """, unsafe_allow_html=True)

    if "pref_threshold" not in st.session_state:
        st.session_state.pref_threshold = 50000
    if "pref_night_flag" not in st.session_state:
        st.session_state.pref_night_flag = True
    if "pref_prob_threshold" not in st.session_state:
        st.session_state.pref_prob_threshold = 10

    col1, col2 = st.columns(2)
    with col1:
        amount_threshold = st.number_input(
            "High-Amount Threshold (₹)",
            min_value=1000, max_value=500000,
            value=st.session_state.pref_threshold,
            step=5000,
            key="thresh_input"
        )
    with col2:
        prob_threshold = st.number_input(
            "Probability Threshold (%)",
            min_value=1, max_value=99,
            value=st.session_state.pref_prob_threshold,
            step=1,
            key="prob_input"
        )

    night_flag = st.checkbox(
        "Flag transactions between 00:00–04:00 as high-risk",
        value=st.session_state.pref_night_flag,
        key="night_flag_input"
    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#060d1f;border:1px solid #1a2540;border-radius:10px;
        padding:12px 16px;margin-bottom:16px;font-family:'DM Mono',monospace;font-size:11px;color:#5b7fa6;">
        Current rules: Flag if amount &gt; ₹{amount_threshold:,}
        {'or hour ≤ 03:00' if night_flag else ''}
        or model probability &gt; {prob_threshold}%
    </div>
    """, unsafe_allow_html=True)

    if st.button("Save Preferences", key="save_prefs_btn"):
        st.session_state.pref_threshold = amount_threshold
        st.session_state.pref_night_flag = night_flag
        st.session_state.pref_prob_threshold = prob_threshold
        st.success("Preferences saved.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Model info ──
    section_header("Model Information")
    st.markdown("""
    <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:16px;padding:20px 24px;margin-bottom:8px;">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div>
                <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;
                    letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;">Algorithm</div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:white;">Random Forest</div>
            </div>
            <div>
                <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;
                    letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;">Accuracy</div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:#22c55e;">98.0%</div>
            </div>
            <div>
                <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;
                    letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;">Features</div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:white;">13</div>
            </div>
            <div>
                <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;
                    letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;">Explainability</div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:#00d4ff;">SHAP</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Danger zone ──
    section_header("Danger Zone")
    st.markdown("""
    <div style="background:#0b0f1e;border:1px solid rgba(239,68,68,0.3);border-radius:16px;
        padding:20px 24px;margin-bottom:8px;">
        <div style="font-family:'DM Mono',monospace;font-size:12px;color:#5b7fa6;margin-bottom:16px;">
            Permanently clear all session data. This cannot be undone.
        </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑️  Clear History", key="danger_clear_hist"):
            st.session_state.history = []
            st.success("Transaction history cleared.")
    with col_b:
        if st.button("🚪  Sign Out", key="danger_signout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.history = []
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
