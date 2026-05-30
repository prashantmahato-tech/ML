# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
# import numpy as np


# CHART_STYLE = {
#     "figure.facecolor": "#0b0f1e",
#     "axes.facecolor": "#0b0f1e",
#     "axes.edgecolor": "#1a2540",
#     "axes.labelcolor": "#5b7fa6",
#     "text.color": "#94a3b8",
#     "xtick.color": "#4a6080",
#     "ytick.color": "#4a6080",
#     "grid.color": "#0f1a2e",
#     "font.family": "monospace",
#     "font.size": 8,          # reduced global font size
# }


# def section_header(title):
#     st.markdown(f"""
#     <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#3d5a80;
#         letter-spacing:.2em;text-transform:uppercase;margin:20px 0 12px;
#         display:flex;align-items:center;gap:8px;">
#         <span style="display:inline-block;width:20px;height:2px;background:#00d4ff;border-radius:99px;"></span>
#         {title}
#     </div>
#     """, unsafe_allow_html=True)


# def show():
#     st.markdown("""
#     <div style="padding:48px 0 32px;border-bottom:1px solid #0f1a2e;margin-bottom:36px;">
#         <div style="display:flex;align-items:center;gap:16px;">
#             <div style="width:48px;height:48px;background:linear-gradient(135deg,#006688,#004499);
#                 border-radius:14px;display:flex;align-items:center;justify-content:center;
#                 font-size:24px;box-shadow:0 4px 20px rgba(0,70,150,0.4);flex-shrink:0;">📊</div>
#             <div>
#                 <h1 style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:white;
#                     letter-spacing:-0.02em;line-height:1;margin-bottom:4px;">Analytics</h1>
#                 <p style="color:#3d5a80;font-family:'DM Mono',monospace;font-size:11px;
#                     letter-spacing:.15em;text-transform:uppercase;">Session insights & patterns</p>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     history = st.session_state.history

#     if not history:
#         st.markdown("""
#         <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:20px;
#             padding:60px 32px;text-align:center;margin-top:20px;">
#             <div style="font-size:40px;margin-bottom:16px;">📈</div>
#             <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;
#                 color:#3d5a80;margin-bottom:8px;">No data yet</div>
#             <div style="font-family:'DM Mono',monospace;font-size:12px;color:#1e3a5f;">
#                 Run some analyses to see your fraud patterns
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
#         return

#     df = pd.DataFrame(history)
#     total = len(df)
#     fraud_count = int((df["Result"] == "Fraud").sum())
#     safe_count = total - fraud_count
#     fraud_rate = fraud_count / total * 100 if total > 0 else 0
#     avg_amount = df["Amount"].mean()
#     avg_fraud_amount = df[df["Result"] == "Fraud"]["Amount"].mean() if fraud_count > 0 else 0
#     max_amount = df["Amount"].max()

#     # ── KPI cards ──
#     section_header("Key Metrics")
#     st.markdown(f"""
#     <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:8px;">
#         <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:16px;padding:20px;">
#             <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;
#                 letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px;">Fraud Rate</div>
#             <div style="font-family:'Syne',sans-serif;font-size:36px;font-weight:800;
#                 color:{'#f87171' if fraud_rate > 20 else '#f59e0b' if fraud_rate > 5 else '#4ade80'};">
#                 {fraud_rate:.1f}%</div>
#             <div style="font-family:'DM Mono',monospace;font-size:11px;color:#3d5a80;margin-top:4px;">
#                 {fraud_count} of {total} flagged</div>
#         </div>
#         <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:16px;padding:20px;">
#             <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;
#                 letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px;">Avg Transaction</div>
#             <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:#00d4ff;">
#                 ₹{avg_amount:,.0f}</div>
#             <div style="font-family:'DM Mono',monospace;font-size:11px;color:#3d5a80;margin-top:4px;">
#                 Max: ₹{max_amount:,.0f}</div>
#         </div>
#     </div>
#     <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:28px;">
#         <div style="background:#0b0f1e;border:1px solid rgba(239,68,68,0.25);border-radius:16px;padding:20px;">
#             <div style="font-size:10px;color:#7f1d1d;font-family:'DM Mono',monospace;
#                 letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px;">Avg Fraud Amount</div>
#             <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:#f87171;">
#                 ₹{avg_fraud_amount:,.0f}</div>
#             <div style="font-family:'DM Mono',monospace;font-size:11px;color:#7f1d1d;margin-top:4px;">
#                 {'Higher than avg ⚠' if avg_fraud_amount > avg_amount else 'Within normal range'}</div>
#         </div>
#         <div style="background:#0b0f1e;border:1px solid rgba(34,197,94,0.2);border-radius:16px;padding:20px;">
#             <div style="font-size:10px;color:#166534;font-family:'DM Mono',monospace;
#                 letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px;">Safe Transactions</div>
#             <div style="font-family:'Syne',sans-serif;font-size:36px;font-weight:800;color:#4ade80;">
#                 {safe_count}</div>
#             <div style="font-family:'DM Mono',monospace;font-size:11px;color:#166534;margin-top:4px;">
#                 {100-fraud_rate:.1f}% clean</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     plt.rcParams.update(CHART_STYLE)

#     # ── Results pie chart ──
#     section_header("Fraud vs Safe Breakdown")

#     # Constrain pie chart to a narrow column so it doesn't stretch full width
#     col_pie, col_spacer = st.columns([1, 2])
#     with col_pie:
#         fig1, ax1 = plt.subplots(figsize=(3, 2.2))
#         fig1.patch.set_facecolor("#0b0f1e")
#         sizes = [fraud_count, safe_count] if fraud_count > 0 else [0.001, safe_count]
#         colors = ["#ef4444", "#22c55e"]
#         explode = (0.05, 0)
#         wedges, texts, autotexts = ax1.pie(
#             sizes, explode=explode, colors=colors,
#             autopct="%1.1f%%", startangle=140,
#             wedgeprops=dict(edgecolor="#0b0f1e", linewidth=1.5),
#             textprops=dict(fontsize=7),
#         )
#         for t in texts:
#             t.set_fontsize(0)
#         for at in autotexts:
#             at.set_fontsize(7)
#             at.set_color("#94a3b8")
#         ax1.legend(
#             [mpatches.Patch(color="#ef4444"), mpatches.Patch(color="#22c55e")],
#             ["Fraud", "Safe"], loc="lower right",
#             fontsize=7, framealpha=0,
#             labelcolor="#94a3b8",
#         )
#         ax1.set_facecolor("#0b0f1e")
#         # Shrink the pie circle itself by shrinking the axes within the figure
#         ax1.set_position([0.1, 0.1, 0.5, 0.5])   # [left, bottom, width, height] — reduce to shrink pie
#         st.pyplot(fig1)
#         plt.close(fig1)

#     # ── Fraud by location ──
#     if len(df["Location"].unique()) > 1:
#         section_header("Fraud by Location")
#         loc_fraud = df[df["Result"] == "Fraud"]["Location"].value_counts()
#         loc_total = df["Location"].value_counts()
#         loc_rate = (loc_fraud / loc_total * 100).fillna(0).sort_values(ascending=True)

#         fig2, ax2 = plt.subplots(figsize=(6, max(2.5, len(loc_rate) * 0.4)))
#         fig2.patch.set_facecolor("#0b0f1e")
#         ax2.set_facecolor("#0b0f1e")
#         bar_colors = ["#ef4444" if v > 50 else "#f59e0b" if v > 20 else "#22c55e" for v in loc_rate.values]
#         bars = ax2.barh(loc_rate.index, loc_rate.values, color=bar_colors,
#                         height=0.5, edgecolor="#0b0f1e")
#         ax2.set_xlabel("Fraud Rate (%)", color="#5b7fa6", fontsize=8)
#         ax2.tick_params(labelsize=8)
#         ax2.spines[:].set_visible(False)
#         ax2.tick_params(colors="#4a6080")
#         for bar, val in zip(bars, loc_rate.values):
#             ax2.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
#                      f"{val:.0f}%", va="center", color="#94a3b8", fontsize=7)
#         fig2.tight_layout()
#         st.pyplot(fig2)
#         plt.close(fig2)

#     # ── Transactions by hour ──
#     section_header("Transactions by Hour")
#     hour_counts = df.groupby(["Hour", "Result"]).size().unstack(fill_value=0)
#     hours = list(range(24))

#     fraud_by_hour = [hour_counts.loc[h, "Fraud"] if h in hour_counts.index and "Fraud" in hour_counts.columns else 0 for h in hours]
#     safe_by_hour  = [hour_counts.loc[h, "Safe"]  if h in hour_counts.index and "Safe"  in hour_counts.columns else 0 for h in hours]

#     fig3, ax3 = plt.subplots(figsize=(7, 2.6))
#     fig3.patch.set_facecolor("#0b0f1e")
#     ax3.set_facecolor("#0b0f1e")
#     x = np.arange(24)
#     ax3.bar(x, safe_by_hour, color="#22c55e", alpha=0.7, label="Safe", width=0.7)
#     ax3.bar(x, fraud_by_hour, bottom=safe_by_hour, color="#ef4444", alpha=0.85, label="Fraud", width=0.7)
#     ax3.set_xticks(x)
#     ax3.set_xticklabels([f"{h:02d}" for h in hours], fontsize=6, rotation=45)
#     ax3.set_ylabel("Count", color="#5b7fa6", fontsize=8)
#     ax3.set_xlabel("Hour of Day", color="#5b7fa6", fontsize=8)
#     ax3.tick_params(labelsize=7)
#     ax3.spines[:].set_visible(False)
#     ax3.tick_params(colors="#4a6080")
#     ax3.legend(fontsize=8, framealpha=0, labelcolor="#94a3b8")
#     ax3.axvspan(0, 4, alpha=0.05, color="#ef4444")
#     ax3.text(2, ax3.get_ylim()[1] * 0.9, "Risk Zone", color="#ef4444",
#              fontsize=7, ha="center", alpha=0.7)
#     fig3.tight_layout()
#     st.pyplot(fig3)
#     plt.close(fig3)

#     # ── Amount distribution ──
#     section_header("Amount Distribution")
#     fig4, ax4 = plt.subplots(figsize=(6, 2.4))
#     fig4.patch.set_facecolor("#0b0f1e")
#     ax4.set_facecolor("#0b0f1e")

#     fraud_amounts = df[df["Result"] == "Fraud"]["Amount"]
#     safe_amounts  = df[df["Result"] == "Safe"]["Amount"]

#     if len(safe_amounts) > 0:
#         ax4.hist(safe_amounts, bins=15, color="#22c55e", alpha=0.6, label="Safe", edgecolor="#0b0f1e")
#     if len(fraud_amounts) > 0:
#         ax4.hist(fraud_amounts, bins=15, color="#ef4444", alpha=0.7, label="Fraud", edgecolor="#0b0f1e")

#     ax4.axvline(50000, color="#f59e0b", linestyle="--", linewidth=1.2, alpha=0.8, label="₹50k threshold")
#     ax4.set_xlabel("Amount (₹)", color="#5b7fa6", fontsize=8)
#     ax4.set_ylabel("Count", color="#5b7fa6", fontsize=8)
#     ax4.tick_params(labelsize=7, colors="#4a6080")
#     ax4.spines[:].set_visible(False)
#     ax4.legend(fontsize=8, framealpha=0, labelcolor="#94a3b8")
#     fig4.tight_layout()
#     st.pyplot(fig4)
#     plt.close(fig4)

#     # ── Transaction type breakdown ──
#     if len(df["Type"].unique()) > 1:
#         section_header("Transaction Type Breakdown")
#         type_data = df.groupby(["Type", "Result"]).size().unstack(fill_value=0)

#         fig5, ax5 = plt.subplots(figsize=(4.5, 2.4))
#         fig5.patch.set_facecolor("#0b0f1e")
#         ax5.set_facecolor("#0b0f1e")
#         types = type_data.index.tolist()
#         x = np.arange(len(types))
#         w = 0.35
#         if "Safe" in type_data.columns:
#             ax5.bar(x - w/2, type_data["Safe"], w, color="#22c55e", alpha=0.8, label="Safe")
#         if "Fraud" in type_data.columns:
#             ax5.bar(x + w/2, type_data["Fraud"], w, color="#ef4444", alpha=0.85, label="Fraud")
#         ax5.set_xticks(x)
#         ax5.set_xticklabels(types, color="#94a3b8", fontsize=8)
#         ax5.tick_params(labelsize=7, colors="#4a6080")
#         ax5.spines[:].set_visible(False)
#         ax5.legend(fontsize=8, framealpha=0, labelcolor="#94a3b8")
#         fig5.tight_layout()
#         st.pyplot(fig5)
#         plt.close(fig5)

#     # ── Top risk insight ──
#     section_header("Risk Insights")
#     insights = []

#     high_hour_frauds = df[(df["Hour"] <= 3) & (df["Result"] == "Fraud")]
#     if len(high_hour_frauds) > 0:
#         insights.append(("🌙", f"{len(high_hour_frauds)} fraud(s) occurred between midnight and 4 AM — a high-risk window.", "#f59e0b"))

#     high_amount_frauds = df[(df["Amount"] > 50000) & (df["Result"] == "Fraud")]
#     if len(high_amount_frauds) > 0:
#         insights.append(("💸", f"{len(high_amount_frauds)} transaction(s) exceeded ₹50,000 and were flagged as fraud.", "#ef4444"))

#     if fraud_rate > 30:
#         insights.append(("⚠️", f"Fraud rate is elevated at {fraud_rate:.1f}%. Consider reviewing recent transaction patterns.", "#ef4444"))
#     elif fraud_rate == 0:
#         insights.append(("✅", "No fraud detected in this session. All transactions are clean.", "#22c55e"))

#     if not insights:
#         insights.append(("📊", "Session looks normal. Keep monitoring for unusual patterns.", "#00d4ff"))

#     for icon, text, color in insights:
#         st.markdown(f"""
#         <div style="background:#0b0f1e;border:1px solid {color}33;border-left:3px solid {color};
#             border-radius:10px;padding:14px 18px;margin-bottom:10px;
#             display:flex;align-items:flex-start;gap:12px;">
#             <span style="font-size:18px;flex-shrink:0;">{icon}</span>
#             <span style="font-family:'DM Mono',monospace;font-size:12px;color:#94a3b8;line-height:1.6;">{text}</span>
#         </div>
#         """, unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


CHART_STYLE = {
    "figure.facecolor": "#0b0f1e",
    "axes.facecolor": "#0b0f1e",
    "axes.edgecolor": "#1a2540",
    "axes.labelcolor": "#5b7fa6",
    "text.color": "#94a3b8",
    "xtick.color": "#4a6080",
    "ytick.color": "#4a6080",
    "grid.color": "#0f1a2e",
    "font.family": "monospace",
    "font.size": 8,          # reduced global font size
}


def section_header(title):
    st.markdown(f"""
    <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#3d5a80;
        letter-spacing:.2em;text-transform:uppercase;margin:20px 0 12px;
        display:flex;align-items:center;gap:8px;">
        <span style="display:inline-block;width:20px;height:2px;background:#00d4ff;border-radius:99px;"></span>
        {title}
    </div>
    """, unsafe_allow_html=True)


def show():
    st.markdown("""
    <div style="padding:48px 0 32px;border-bottom:1px solid #0f1a2e;margin-bottom:36px;">
        <div style="display:flex;align-items:center;gap:16px;">
            <div style="width:48px;height:48px;background:linear-gradient(135deg,#006688,#004499);
                border-radius:14px;display:flex;align-items:center;justify-content:center;
                font-size:24px;box-shadow:0 4px 20px rgba(0,70,150,0.4);flex-shrink:0;">📊</div>
            <div>
                <h1 style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:white;
                    letter-spacing:-0.02em;line-height:1;margin-bottom:4px;">Analytics</h1>
                <p style="color:#3d5a80;font-family:'DM Mono',monospace;font-size:11px;
                    letter-spacing:.15em;text-transform:uppercase;">Session insights & patterns</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.history

    if not history:
        st.markdown("""
        <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:20px;
            padding:60px 32px;text-align:center;margin-top:20px;">
            <div style="font-size:40px;margin-bottom:16px;">📈</div>
            <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;
                color:#3d5a80;margin-bottom:8px;">No data yet</div>
            <div style="font-family:'DM Mono',monospace;font-size:12px;color:#1e3a5f;">
                Run some analyses to see your fraud patterns
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    df = pd.DataFrame(history)
    total = len(df)
    fraud_count = int((df["Result"] == "Fraud").sum())
    safe_count = total - fraud_count
    fraud_rate = fraud_count / total * 100 if total > 0 else 0
    avg_amount = df["Amount"].mean()
    avg_fraud_amount = df[df["Result"] == "Fraud"]["Amount"].mean() if fraud_count > 0 else 0
    max_amount = df["Amount"].max()

    # ── KPI cards ──
    section_header("Key Metrics")
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:8px;">
        <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:16px;padding:20px;">
            <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;
                letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px;">Fraud Rate</div>
            <div style="font-family:'Syne',sans-serif;font-size:36px;font-weight:800;
                color:{'#f87171' if fraud_rate > 20 else '#f59e0b' if fraud_rate > 5 else '#4ade80'};">
                {fraud_rate:.1f}%</div>
            <div style="font-family:'DM Mono',monospace;font-size:11px;color:#3d5a80;margin-top:4px;">
                {fraud_count} of {total} flagged</div>
        </div>
        <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:16px;padding:20px;">
            <div style="font-size:10px;color:#3d5a80;font-family:'DM Mono',monospace;
                letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px;">Avg Transaction</div>
            <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:#00d4ff;">
                ₹{avg_amount:,.0f}</div>
            <div style="font-family:'DM Mono',monospace;font-size:11px;color:#3d5a80;margin-top:4px;">
                Max: ₹{max_amount:,.0f}</div>
        </div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:28px;">
        <div style="background:#0b0f1e;border:1px solid rgba(239,68,68,0.25);border-radius:16px;padding:20px;">
            <div style="font-size:10px;color:#7f1d1d;font-family:'DM Mono',monospace;
                letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px;">Avg Fraud Amount</div>
            <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:#f87171;">
                ₹{avg_fraud_amount:,.0f}</div>
            <div style="font-family:'DM Mono',monospace;font-size:11px;color:#7f1d1d;margin-top:4px;">
                {'Higher than avg ⚠' if avg_fraud_amount > avg_amount else 'Within normal range'}</div>
        </div>
        <div style="background:#0b0f1e;border:1px solid rgba(34,197,94,0.2);border-radius:16px;padding:20px;">
            <div style="font-size:10px;color:#166534;font-family:'DM Mono',monospace;
                letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px;">Safe Transactions</div>
            <div style="font-family:'Syne',sans-serif;font-size:36px;font-weight:800;color:#4ade80;">
                {safe_count}</div>
            <div style="font-family:'DM Mono',monospace;font-size:11px;color:#166534;margin-top:4px;">
                {100-fraud_rate:.1f}% clean</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    plt.rcParams.update(CHART_STYLE)

    # ── Results pie chart ──
    section_header("Fraud vs Safe Breakdown")

    # Constrain pie chart to a narrow column so it doesn't stretch full width
    col_pie, col_spacer = st.columns([1, 2])
    with col_pie:
        fig1, ax1 = plt.subplots(figsize=(3, 2.2))
        fig1.patch.set_facecolor("#0b0f1e")
        sizes = [fraud_count, safe_count] if fraud_count > 0 else [0.001, safe_count]
        colors = ["#ef4444", "#22c55e"]
        explode = (0.05, 0)
        wedges, texts, autotexts = ax1.pie(
            sizes, explode=explode, colors=colors,
            autopct="%1.1f%%", startangle=140,
            radius=0.6,                                    # ← shrinks the pie circle itself
            wedgeprops=dict(edgecolor="#0b0f1e", linewidth=1.5),
            textprops=dict(fontsize=7),
        )
        for t in texts:
            t.set_fontsize(0)
        for at in autotexts:
            at.set_fontsize(7)
            at.set_color("#94a3b8")
        ax1.legend(
            [mpatches.Patch(color="#ef4444"), mpatches.Patch(color="#22c55e")],
            ["Fraud", "Safe"], loc="lower right",
            fontsize=7, framealpha=0,
            labelcolor="#94a3b8",
        )
        ax1.set_facecolor("#0b0f1e")
        fig1.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    # ── Fraud by location ──
    if len(df["Location"].unique()) > 1:
        section_header("Fraud by Location")
        loc_fraud = df[df["Result"] == "Fraud"]["Location"].value_counts()
        loc_total = df["Location"].value_counts()
        loc_rate = (loc_fraud / loc_total * 100).fillna(0).sort_values(ascending=True)

        fig2, ax2 = plt.subplots(figsize=(6, max(2.5, len(loc_rate) * 0.4)))
        fig2.patch.set_facecolor("#0b0f1e")
        ax2.set_facecolor("#0b0f1e")
        bar_colors = ["#ef4444" if v > 50 else "#f59e0b" if v > 20 else "#22c55e" for v in loc_rate.values]
        bars = ax2.barh(loc_rate.index, loc_rate.values, color=bar_colors,
                        height=0.5, edgecolor="#0b0f1e")
        ax2.set_xlabel("Fraud Rate (%)", color="#5b7fa6", fontsize=8)
        ax2.tick_params(labelsize=8)
        ax2.spines[:].set_visible(False)
        ax2.tick_params(colors="#4a6080")
        for bar, val in zip(bars, loc_rate.values):
            ax2.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
                     f"{val:.0f}%", va="center", color="#94a3b8", fontsize=7)
        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    # ── Transactions by hour ──
    section_header("Transactions by Hour")
    hour_counts = df.groupby(["Hour", "Result"]).size().unstack(fill_value=0)
    hours = list(range(24))

    fraud_by_hour = [hour_counts.loc[h, "Fraud"] if h in hour_counts.index and "Fraud" in hour_counts.columns else 0 for h in hours]
    safe_by_hour  = [hour_counts.loc[h, "Safe"]  if h in hour_counts.index and "Safe"  in hour_counts.columns else 0 for h in hours]

    fig3, ax3 = plt.subplots(figsize=(7, 2.6))
    fig3.patch.set_facecolor("#0b0f1e")
    ax3.set_facecolor("#0b0f1e")
    x = np.arange(24)
    ax3.bar(x, safe_by_hour, color="#22c55e", alpha=0.7, label="Safe", width=0.7)
    ax3.bar(x, fraud_by_hour, bottom=safe_by_hour, color="#ef4444", alpha=0.85, label="Fraud", width=0.7)
    ax3.set_xticks(x)
    ax3.set_xticklabels([f"{h:02d}" for h in hours], fontsize=6, rotation=45)
    ax3.set_ylabel("Count", color="#5b7fa6", fontsize=8)
    ax3.set_xlabel("Hour of Day", color="#5b7fa6", fontsize=8)
    ax3.tick_params(labelsize=7)
    ax3.spines[:].set_visible(False)
    ax3.tick_params(colors="#4a6080")
    ax3.legend(fontsize=8, framealpha=0, labelcolor="#94a3b8")
    ax3.axvspan(0, 4, alpha=0.05, color="#ef4444")
    ax3.text(2, ax3.get_ylim()[1] * 0.9, "Risk Zone", color="#ef4444",
             fontsize=7, ha="center", alpha=0.7)
    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

    # ── Amount distribution ──
    section_header("Amount Distribution")
    fig4, ax4 = plt.subplots(figsize=(6, 2.4))
    fig4.patch.set_facecolor("#0b0f1e")
    ax4.set_facecolor("#0b0f1e")

    fraud_amounts = df[df["Result"] == "Fraud"]["Amount"]
    safe_amounts  = df[df["Result"] == "Safe"]["Amount"]

    if len(safe_amounts) > 0:
        ax4.hist(safe_amounts, bins=15, color="#22c55e", alpha=0.6, label="Safe", edgecolor="#0b0f1e")
    if len(fraud_amounts) > 0:
        ax4.hist(fraud_amounts, bins=15, color="#ef4444", alpha=0.7, label="Fraud", edgecolor="#0b0f1e")

    ax4.axvline(50000, color="#f59e0b", linestyle="--", linewidth=1.2, alpha=0.8, label="₹50k threshold")
    ax4.set_xlabel("Amount (₹)", color="#5b7fa6", fontsize=8)
    ax4.set_ylabel("Count", color="#5b7fa6", fontsize=8)
    ax4.tick_params(labelsize=7, colors="#4a6080")
    ax4.spines[:].set_visible(False)
    ax4.legend(fontsize=8, framealpha=0, labelcolor="#94a3b8")
    fig4.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)

    # ── Transaction type breakdown ──
    if len(df["Type"].unique()) > 1:
        section_header("Transaction Type Breakdown")
        type_data = df.groupby(["Type", "Result"]).size().unstack(fill_value=0)

        fig5, ax5 = plt.subplots(figsize=(4.5, 2.4))
        fig5.patch.set_facecolor("#0b0f1e")
        ax5.set_facecolor("#0b0f1e")
        types = type_data.index.tolist()
        x = np.arange(len(types))
        w = 0.35
        if "Safe" in type_data.columns:
            ax5.bar(x - w/2, type_data["Safe"], w, color="#22c55e", alpha=0.8, label="Safe")
        if "Fraud" in type_data.columns:
            ax5.bar(x + w/2, type_data["Fraud"], w, color="#ef4444", alpha=0.85, label="Fraud")
        ax5.set_xticks(x)
        ax5.set_xticklabels(types, color="#94a3b8", fontsize=8)
        ax5.tick_params(labelsize=7, colors="#4a6080")
        ax5.spines[:].set_visible(False)
        ax5.legend(fontsize=8, framealpha=0, labelcolor="#94a3b8")
        fig5.tight_layout()
        st.pyplot(fig5)
        plt.close(fig5)

    # ── Top risk insight ──
    section_header("Risk Insights")
    insights = []

    high_hour_frauds = df[(df["Hour"] <= 3) & (df["Result"] == "Fraud")]
    if len(high_hour_frauds) > 0:
        insights.append(("🌙", f"{len(high_hour_frauds)} fraud(s) occurred between midnight and 4 AM — a high-risk window.", "#f59e0b"))

    high_amount_frauds = df[(df["Amount"] > 50000) & (df["Result"] == "Fraud")]
    if len(high_amount_frauds) > 0:
        insights.append(("💸", f"{len(high_amount_frauds)} transaction(s) exceeded ₹50,000 and were flagged as fraud.", "#ef4444"))

    if fraud_rate > 30:
        insights.append(("⚠️", f"Fraud rate is elevated at {fraud_rate:.1f}%. Consider reviewing recent transaction patterns.", "#ef4444"))
    elif fraud_rate == 0:
        insights.append(("✅", "No fraud detected in this session. All transactions are clean.", "#22c55e"))

    if not insights:
        insights.append(("📊", "Session looks normal. Keep monitoring for unusual patterns.", "#00d4ff"))

    for icon, text, color in insights:
        st.markdown(f"""
        <div style="background:#0b0f1e;border:1px solid {color}33;border-left:3px solid {color};
            border-radius:10px;padding:14px 18px;margin-bottom:10px;
            display:flex;align-items:flex-start;gap:12px;">
            <span style="font-size:18px;flex-shrink:0;">{icon}</span>
            <span style="font-family:'DM Mono',monospace;font-size:12px;color:#94a3b8;line-height:1.6;">{text}</span>
        </div>
        """, unsafe_allow_html=True)
