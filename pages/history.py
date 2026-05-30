import streamlit as st
import pandas as pd
from io import StringIO


def show():
    st.markdown("""
    <div style="padding:48px 0 32px;border-bottom:1px solid #0f1a2e;margin-bottom:36px;">
        <div style="display:flex;align-items:center;gap:16px;">
            <div style="width:48px;height:48px;background:linear-gradient(135deg,#0055aa,#0033cc);
                border-radius:14px;display:flex;align-items:center;justify-content:center;
                font-size:24px;box-shadow:0 4px 20px rgba(0,50,200,0.4);flex-shrink:0;">📋</div>
            <div>
                <h1 style="font-family:'Syne',sans-serif;font-size:32px;font-weight:800;color:white;
                    letter-spacing:-0.02em;line-height:1;margin-bottom:4px;">Transaction History</h1>
                <p style="color:#3d5a80;font-family:'DM Mono',monospace;font-size:11px;
                    letter-spacing:.15em;text-transform:uppercase;">All checks from this session</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.history

    if not history:
        st.markdown("""
        <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:20px;
            padding:60px 32px;text-align:center;margin-top:20px;">
            <div style="font-size:40px;margin-bottom:16px;">📭</div>
            <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;
                color:#3d5a80;margin-bottom:8px;">No transactions yet</div>
            <div style="font-family:'DM Mono',monospace;font-size:12px;color:#1e3a5f;">
                Run your first analysis on the Analyze page
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    df = pd.DataFrame(history)
    total = len(df)
    fraud_count = (df["Result"] == "Fraud").sum()
    safe_count = total - fraud_count
    total_amount = df["Amount"].sum()

    # ── Summary cards ──
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:28px;">
        <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:14px;padding:16px;">
            <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;letter-spacing:.12em;
                text-transform:uppercase;margin-bottom:6px;">Total</div>
            <div style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:white;">{total}</div>
        </div>
        <div style="background:#0b0f1e;border:1px solid rgba(239,68,68,0.3);border-radius:14px;padding:16px;">
            <div style="font-size:10px;color:#7f1d1d;font-family:'DM Mono',monospace;letter-spacing:.12em;
                text-transform:uppercase;margin-bottom:6px;">Fraud</div>
            <div style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:#f87171;">{fraud_count}</div>
        </div>
        <div style="background:#0b0f1e;border:1px solid rgba(34,197,94,0.25);border-radius:14px;padding:16px;">
            <div style="font-size:10px;color:#166534;font-family:'DM Mono',monospace;letter-spacing:.12em;
                text-transform:uppercase;margin-bottom:6px;">Safe</div>
            <div style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:#4ade80;">{safe_count}</div>
        </div>
        <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:14px;padding:16px;">
            <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;letter-spacing:.12em;
                text-transform:uppercase;margin-bottom:6px;">Volume</div>
            <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#00d4ff;">₹{total_amount:,.0f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filters ──
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#3d5a80;
        letter-spacing:.2em;text-transform:uppercase;margin-bottom:14px;
        display:flex;align-items:center;gap:8px;">
        <span style="display:inline-block;width:20px;height:2px;background:#00d4ff;border-radius:99px;"></span>
        Filters
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        result_filter = st.selectbox("Result", ["All", "Fraud", "Safe"], key="hist_result")
    with col2:
        type_filter = st.selectbox("Type", ["All", "Purchase", "Refund"], key="hist_type")
    with col3:
        locations = ["All"] + sorted(df["Location"].unique().tolist())
        location_filter = st.selectbox("Location", locations, key="hist_loc")

    filtered = df.copy()
    if result_filter != "All":
        filtered = filtered[filtered["Result"] == result_filter]
    if type_filter != "All":
        filtered = filtered[filtered["Type"] == type_filter]
    if location_filter != "All":
        filtered = filtered[filtered["Location"] == location_filter]

    st.markdown(f"""
    <div style="font-size:11px;color:#3d5a80;font-family:'DM Mono',monospace;
        margin:16px 0 12px;">Showing {len(filtered)} of {total} transactions</div>
    """, unsafe_allow_html=True)

    # ── Transaction rows ──
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#3d5a80;
        letter-spacing:.2em;text-transform:uppercase;margin:20px 0 14px;
        display:flex;align-items:center;gap:8px;">
        <span style="display:inline-block;width:20px;height:2px;background:#00d4ff;border-radius:99px;"></span>
        Transactions
    </div>
    """, unsafe_allow_html=True)

    if filtered.empty:
        st.info("No transactions match the selected filters.")
    else:
        for _, tx in filtered.iloc[::-1].iterrows():
            is_fraud = tx["Result"] == "Fraud"
            bc = "rgba(239,68,68,0.3)" if is_fraud else "rgba(34,197,94,0.25)"
            fc = "#f87171" if is_fraud else "#4ade80"
            bg = "rgba(239,68,68,0.08)" if is_fraud else "rgba(34,197,94,0.06)"
            label = "⚠ FRAUD" if is_fraud else "✓ SAFE"
            day = tx.get("Day", "—")
            month = tx.get("Month", "—")

            st.markdown(f"""
            <div style="background:#0b0f1e;border:1px solid {bc};border-radius:14px;
                padding:16px 20px;margin-bottom:10px;display:flex;
                align-items:center;justify-content:space-between;gap:12px;">
                <div style="display:flex;align-items:center;gap:12px;flex:1;min-width:0;">
                    <div style="background:{bg};color:{fc};font-family:'DM Mono',monospace;
                        font-size:10px;letter-spacing:.1em;padding:4px 10px;
                        border-radius:6px;border:1px solid {bc};white-space:nowrap;flex-shrink:0;">{label}</div>
                    <div style="min-width:0;">
                        <div style="font-family:'Syne',sans-serif;font-weight:700;color:white;font-size:15px;">₹{tx['Amount']:,.2f}</div>
                        <div style="font-family:'DM Mono',monospace;font-size:11px;color:#3d5a80;
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                            {tx['Type']} · {tx['Location']} · {day} · {month}
                        </div>
                    </div>
                </div>
                <div style="text-align:right;font-family:'DM Mono',monospace;font-size:11px;
                    color:#3d5a80;flex-shrink:0;">
                    <div>{tx['Hour']:02d}:00</div>
                    <div style="color:{fc};font-weight:500;">{tx['Probability']}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Export ──
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#3d5a80;
        letter-spacing:.2em;text-transform:uppercase;margin-bottom:14px;
        display:flex;align-items:center;gap:8px;">
        <span style="display:inline-block;width:20px;height:2px;background:#00d4ff;border-radius:99px;"></span>
        Export
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        csv_data = filtered.to_csv(index=False)
        st.download_button(
            label="↓  Download CSV",
            data=csv_data,
            file_name="safeswipe_history.csv",
            mime="text/csv",
            key="dl_csv"
        )
    with col_b:
        if st.button("🗑️  Clear History", key="clear_hist"):
            st.session_state.history = []
            st.rerun()
