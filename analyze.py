import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
from io import BytesIO


def page_header(title, subtitle):
    st.markdown(f"""
    <div style="padding:48px 0 32px;border-bottom:1px solid #0f1a2e;margin-bottom:36px;">
        <div style="display:flex;align-items:center;gap:16px;">
            <div style="width:48px;height:48px;background:linear-gradient(135deg,#0099cc,#0044ff);
                border-radius:14px;display:flex;align-items:center;justify-content:center;
                font-size:24px;box-shadow:0 4px 20px rgba(0,100,255,0.4);flex-shrink:0;">⚡</div>
            <div>
                <h1 style="font-family:'Syne',sans-serif;font-size:32px;font-weight:800;color:white;
                    letter-spacing:-0.02em;line-height:1;margin-bottom:4px;">{title}</h1>
                <p style="color:#3d5a80;font-family:'DM Mono',monospace;font-size:11px;
                    letter-spacing:.15em;text-transform:uppercase;">{subtitle}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


@st.cache_resource
def load_files():
    try:
        model = joblib.load("model.pkl")
        columns = joblib.load("columns.pkl")
        return model, columns
    except Exception as e:
        st.error(f"Model load error: {e}")
        return None, None


def show():
    page_header("Transaction Analysis", "Real-time fraud detection")

    model, columns = load_files()

    # ── Input form ──
    st.markdown("""
    <div style="background:#0b0f1e;border:1px solid #1a2540;border-radius:20px;padding:32px;margin-bottom:24px;">
        <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#3d5a80;
            letter-spacing:.2em;text-transform:uppercase;margin-bottom:24px;
            display:flex;align-items:center;gap:8px;">
            <span style="display:inline-block;width:20px;height:2px;background:#00d4ff;border-radius:99px;"></span>
            Transaction Details
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        Amount = st.number_input("Amount (₹)", min_value=0.0, value=100.0, step=1.0)
    with col2:
        TransactionType = st.selectbox("Transaction Type", ["Purchase", "Refund"])

    Location = st.selectbox("Location", [
        "Dallas", "Houston", "Los Angeles", "New York",
        "Philadelphia", "Phoenix", "San Antonio", "San Diego", "San Jose"
    ])

    col3, col4 = st.columns(2)
    time_options = [f"{h:02d}:00" for h in range(24)]
    with col3:
        selected_time = st.selectbox("Hour", time_options)
        Hour = int(selected_time.split(":")[0])

    day_options = {"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4,"Saturday":5,"Sunday":6}
    with col4:
        selected_day = st.selectbox("Day of Week", list(day_options.keys()), index=2)
        DayOfWeek = day_options[selected_day]

    month_options = {
        "January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
        "July":7,"August":8,"September":9,"October":10,"November":11,"December":12
    }
    selected_month = st.selectbox("Month", list(month_options.keys()), index=5)
    Month = month_options[selected_month]

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Feature engineering ──
    refund_value = 1 if TransactionType == "Refund" else 0
    location_columns = {
        "Location_Dallas":0,"Location_Houston":0,"Location_Los Angeles":0,
        "Location_New York":0,"Location_Philadelphia":0,"Location_Phoenix":0,
        "Location_San Antonio":0,"Location_San Diego":0,"Location_San Jose":0
    }
    selected_location = f"Location_{Location}"
    if selected_location in location_columns:
        location_columns[selected_location] = 1

    input_data = {
        "Amount": Amount,
        "TransactionType_refund": refund_value,
        **location_columns,
        "Hour": Hour,
        "DayOfWeek": DayOfWeek,
        "Month": Month
    }
    features = pd.DataFrame([input_data])

    # ── Predict button ──
    if st.button("⚡  Run Fraud Analysis", key="predict_btn"):
        if Amount <= 0:
            st.warning("Enter a valid transaction amount.")
            st.stop()
        if model is None or columns is None:
            st.stop()

        try:
            features = features.reindex(columns=columns, fill_value=0).fillna(0)
            prediction = model.predict(features)[0]
            probability = 0
            if hasattr(model, "predict_proba"):
                probability = model.predict_proba(features)[0][1]

            if Amount > 50000 or Hour <= 3:
                final_prediction = 1
            else:
                final_prediction = 1 if probability > 0.10 else 0

            # ── Result card ──
            if final_prediction == 1:
                risk_pct = max(probability * 100, 85 if Amount > 50000 else 60)
                bar_w = min(int(risk_pct), 100)
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,rgba(239,68,68,0.08),rgba(185,28,28,0.04));
                    border:1px solid rgba(239,68,68,0.35);border-radius:20px;padding:32px;margin:8px 0 24px;
                    position:relative;overflow:hidden;">
                    <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;
                        background:radial-gradient(circle,rgba(239,68,68,0.12) 0%,transparent 70%);border-radius:50%;"></div>
                    <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px;">
                        <div style="width:44px;height:44px;background:rgba(239,68,68,0.15);
                            border:1px solid rgba(239,68,68,0.4);border-radius:12px;
                            display:flex;align-items:center;justify-content:center;font-size:20px;">⚠️</div>
                        <div>
                            <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
                                color:#f87171;letter-spacing:-0.01em;">Fraudulent Transaction</div>
                            <div style="font-family:'DM Mono',monospace;font-size:11px;color:#7f1d1d;
                                letter-spacing:.12em;text-transform:uppercase;">High risk — action required</div>
                        </div>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <span style="font-family:'DM Mono',monospace;font-size:11px;color:#7f1d1d;
                            letter-spacing:.1em;text-transform:uppercase;">Risk Score</span>
                        <span style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#f87171;">{risk_pct:.1f}%</span>
                    </div>
                    <div style="height:6px;background:rgba(239,68,68,0.15);border-radius:99px;overflow:hidden;">
                        <div style="height:100%;width:{bar_w}%;background:linear-gradient(90deg,#dc2626,#f87171);border-radius:99px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                safe_pct = (1 - probability) * 100
                bar_w = max(int(safe_pct), 10)
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,rgba(34,197,94,0.06),rgba(21,128,61,0.03));
                    border:1px solid rgba(34,197,94,0.3);border-radius:20px;padding:32px;margin:8px 0 24px;
                    position:relative;overflow:hidden;">
                    <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;
                        background:radial-gradient(circle,rgba(34,197,94,0.08) 0%,transparent 70%);border-radius:50%;"></div>
                    <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px;">
                        <div style="width:44px;height:44px;background:rgba(34,197,94,0.12);
                            border:1px solid rgba(34,197,94,0.35);border-radius:12px;
                            display:flex;align-items:center;justify-content:center;font-size:20px;">✅</div>
                        <div>
                            <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
                                color:#4ade80;letter-spacing:-0.01em;">Legitimate Transaction</div>
                            <div style="font-family:'DM Mono',monospace;font-size:11px;color:#166534;
                                letter-spacing:.12em;text-transform:uppercase;">No fraud signals detected</div>
                        </div>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <span style="font-family:'DM Mono',monospace;font-size:11px;color:#166534;
                            letter-spacing:.1em;text-transform:uppercase;">Safety Score</span>
                        <span style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#4ade80;">{safe_pct:.1f}%</span>
                    </div>
                    <div style="height:6px;background:rgba(34,197,94,0.12);border-radius:99px;overflow:hidden;">
                        <div style="height:100%;width:{bar_w}%;background:linear-gradient(90deg,#16a34a,#4ade80);border-radius:99px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── Save to history ──
            st.session_state.history.append({
                "Amount": Amount,
                "Type": TransactionType,
                "Location": Location,
                "Hour": Hour,
                "Day": selected_day,
                "Month": selected_month,
                "Result": "Fraud" if final_prediction == 1 else "Safe",
                "Probability": round(probability * 100, 2)
            })

            # ── SHAP ──
            st.markdown("""
            <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#3d5a80;
                letter-spacing:.2em;text-transform:uppercase;margin:32px 0 16px;
                display:flex;align-items:center;gap:8px;">
                <span style="display:inline-block;width:20px;height:2px;background:#00d4ff;border-radius:99px;"></span>
                Feature Explainability (SHAP)
            </div>
            """, unsafe_allow_html=True)

            try:
                if "RandomForest" in str(type(model)):
                    explainer = shap.TreeExplainer(model)
                else:
                    explainer = shap.Explainer(model)
                shap_values = explainer(features)

                plt.rcParams.update({
                    "figure.facecolor": "#0b0f1e", "axes.facecolor": "#0b0f1e",
                    "axes.edgecolor": "#1a2540", "axes.labelcolor": "#94a3b8",
                    "text.color": "#94a3b8", "xtick.color": "#4a6080",
                    "ytick.color": "#94a3b8", "grid.color": "#0f1a2e",
                    "font.family": "monospace", "font.size": 11,
                })
                fig = plt.figure(figsize=(10, 5))
                shap.plots.waterfall(shap_values[0, :, 1], max_display=10, show=False)
                fig.patch.set_facecolor("#0b0f1e")
                st.pyplot(fig)

                pdf_buffer = BytesIO()
                fig.savefig(pdf_buffer, format="pdf", bbox_inches="tight", facecolor="#0b0f1e")
                pdf_buffer.seek(0)
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                st.download_button(
                    label="↓  Download SHAP Report (PDF)",
                    data=pdf_buffer,
                    file_name="safeswipe_shap_report.pdf",
                    mime="application/pdf"
                )
                plt.close(fig)
            except Exception as e:
                st.warning(f"SHAP explanation unavailable: {e}")

            # ── Recent transactions ──
            if len(st.session_state.history) > 1:
                st.markdown("""
                <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;color:#3d5a80;
                    letter-spacing:.2em;text-transform:uppercase;margin:32px 0 16px;
                    display:flex;align-items:center;gap:8px;">
                    <span style="display:inline-block;width:20px;height:2px;background:#00d4ff;border-radius:99px;"></span>
                    Recent Transactions
                </div>
                """, unsafe_allow_html=True)

                last_3 = st.session_state.history[-4:-1][::-1]
                for tx in last_3:
                    is_fraud = tx["Result"] == "Fraud"
                    bc = "rgba(239,68,68,0.3)" if is_fraud else "rgba(34,197,94,0.25)"
                    fc = "#f87171" if is_fraud else "#4ade80"
                    bg = "rgba(239,68,68,0.1)" if is_fraud else "rgba(34,197,94,0.08)"
                    label = "⚠ FRAUD" if is_fraud else "✓ SAFE"
                    st.markdown(f"""
                    <div style="background:#0b0f1e;border:1px solid {bc};border-radius:14px;
                        padding:16px 20px;margin-bottom:10px;display:flex;
                        align-items:center;justify-content:space-between;gap:12px;">
                        <div style="display:flex;align-items:center;gap:12px;flex:1;">
                            <div style="background:{bg};color:{fc};font-family:'DM Mono',monospace;
                                font-size:10px;letter-spacing:.1em;padding:4px 10px;
                                border-radius:6px;border:1px solid {bc};white-space:nowrap;">{label}</div>
                            <div>
                                <div style="font-family:'Syne',sans-serif;font-weight:700;color:white;font-size:15px;">₹{tx['Amount']:,.2f}</div>
                                <div style="font-family:'DM Mono',monospace;font-size:11px;color:#3d5a80;">{tx['Type']} · {tx['Location']}</div>
                            </div>
                        </div>
                        <div style="text-align:right;font-family:'DM Mono',monospace;font-size:11px;color:#3d5a80;">
                            <div>{tx['Hour']:02d}:00</div>
                            <div style="color:{fc}">{tx['Probability']}%</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Prediction error: {e}")
