import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="DSS Workforce Dashboard",
    layout="wide"
)
# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.stApp {
    background-color: #F5F7FA;
}

h1, h2, h3, h4 {
    color: #1E293B;
}

p, div {
    color: #334155;
}

div[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    padding: 15px;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

div[data-testid="metric-container"]:hover {
    border: 1px solid #2563EB;
}

.block-container {
    padding-top: 2rem;
}

section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #E2E8F0;
}

</style>
""", unsafe_allow_html=True)
# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Dashboard Menu")

st.sidebar.info("""
DSS Workforce Performance Dashboard

Monitoring:
- Engagement
- AI Support
- Stress
- Digital Capability
- Self-Regulation
""")

st.sidebar.success("🟢 System Active")
st.markdown("""
<div style='
    background: linear-gradient(90deg, #2563EB, #1D4ED8);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
'>

    <h1 style='color:white;text-align:center;'>
        DSS Workforce Performance Dashboard
    </h1>

    <p style='color:white;text-align:center;'>
        Real-Time Workforce Monitoring & Decision Support System
    </p>

</div>
""", unsafe_allow_html=True)

gauge_fig.update_layout(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    font={'color': "#1E293B"},
    height=400
)
# =========================
# TITLE
# =========================
st.title("📊 DSS Workforce Performance Dashboard")

st.markdown("""
Dashboard Decision Support System (DSS) untuk monitoring workforce performance berbasis Artificial Intelligence.
""")

st.divider()

# =========================
# INPUT SECTION
# =========================
st.markdown("## 📝 Input Workforce Variables")

input_col1, input_col2 = st.columns(2)

with input_col1:
    eng = st.slider("Engagement Level (ENG)", 1, 100, 75)
    ais = st.slider("AI System Support (AIS)", 1, 100, 70)
    dc = st.slider("Digital Capability (DC)", 1, 100, 68)

with input_col2:
    strr = st.slider("Operational Stress (STR)", 1, 100, 40)
    src = st.slider("Self-Regulation Capability (SRC)", 1, 100, 42)

# =========================
# CALCULATION
# =========================

mb = (
    (eng * 0.519) +
    (ais * 0.522) +
    (dc * 0.494)
) / (0.519 + 0.522 + 0.494)

md = strr * 0.131

cf = (mb - md) / 100

# Stress dibalik agar visual radar masuk akal
stress_score = 100 - strr

# =========================
# PERFORMANCE CATEGORY
# =========================
if cf > 0.2:
    kategori = "TINGGI"
    warna = "🟢"

elif cf >= -0.2:
    kategori = "SEDANG"
    warna = "🟡"

else:
    kategori = "RENDAH"
    warna = "🔴"

# =========================
# BOTTLENECK
# =========================
if src < 40:
    bottleneck = "TINGGI 🔴"

elif src <= 70:
    bottleneck = "MODERAT 🟡"

else:
    bottleneck = "RENDAH 🟢"

st.divider()

# =========================
# KPI SECTION
# =========================
st.subheader("📌 Workforce Performance Result")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "Certainty Factor",
    f"{cf:.2f}"
)

kpi2.metric(
    "Performance",
    f"{warna} {kategori}"
)

kpi3.metric(
    "SRC Bottleneck",
    bottleneck
)

kpi4.metric(
    "Stress Score",
    f"{stress_score}"
)

# =========================
# PERFORMANCE PROGRESS
# =========================
st.subheader("📊 Workforce Score")

progress_value = int((cf + 1) / 2 * 100)

st.progress(progress_value)

st.write(f"Overall Workforce Score: {progress_value}%")

st.divider()

# =========================
# VISUALIZATION SECTION
# =========================
st.subheader("📈 Workforce Visualization")

left_col, right_col = st.columns(2)

# =========================
# GAUGE CHART
# =========================
with left_col:

    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=cf,
        title={'text': "Certainty Factor"},
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'thickness': 0.3},
            'steps': [
                {'range': [-1, -0.2], 'color': "red"},
                {'range': [-0.2, 0.2], 'color': "yellow"},
                {'range': [0.2, 1], 'color': "green"}
            ],
        }
    ))

    gauge_fig.update_layout(height=400)

    st.plotly_chart(
        gauge_fig,
        use_container_width=True
    )

# =========================
# RADAR CHART
# =========================
with right_col:

    radar_fig = go.Figure()

    radar_fig.add_trace(go.Scatterpolar(
        r=[eng, ais, stress_score, dc, src],
        theta=['ENG', 'AIS', 'Stress Control', 'DC', 'SRC'],
        fill='toself',
        name='Performance'
    ))

    radar_fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={'color': "#1E293B"},
        polar=dict(
            bgcolor="#FFFFFF",
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=400
)

    st.plotly_chart(
        radar_fig,
        use_container_width=True
    )

st.divider()

# =========================
# SUMMARY TABLE
# =========================
st.subheader("📋 Summary Data")

summary_data = {
    "Variabel": [
        "Engagement Level",
        "AI System Support",
        "Operational Stress",
        "Digital Capability",
        "Self-Regulation Capability"
    ],
    "Nilai": [
        eng,
        ais,
        strr,
        dc,
        src
    ]
}

summary_df = pd.DataFrame(summary_data)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =========================
# RECOMMENDATION SECTION
# =========================
st.subheader("💡 Recommendation System")

ada_rekomendasi = False

if eng < 50:
    st.warning(
        "Engagement Level rendah. Tingkatkan keterlibatan kerja."
    )
    ada_rekomendasi = True

if ais < 50:
    st.warning(
        "AI System Support rendah. Optimalkan sistem AI."
    )
    ada_rekomendasi = True

if strr > 70:
    st.error(
        "Operational Stress tinggi. Risiko burnout meningkat."
    )
    ada_rekomendasi = True

if src < 40:
    st.error(
        "SRC menjadi bottleneck utama."
    )
    ada_rekomendasi = True

if dc < 50:
    st.warning(
        "Digital Capability rendah. Perlu pelatihan digital."
    )
    ada_rekomendasi = True

if kategori == "TINGGI":
    st.success(
        "Workforce performance dalam kondisi optimal."
    )
    ada_rekomendasi = True

if not ada_rekomendasi:
    st.info(
        "Tidak ada warning kritis. Sistem workforce stabil."
    )

st.divider()
st.divider()

st.subheader("💾 Save Evaluation")

save_data = {
    "ENG": eng,
    "AIS": ais,
    "STR": strr,
    "DC": dc,
    "SRC": src,
    "CF": round(cf, 2),
    "Kategori": kategori,
    "Bottleneck": bottleneck
}

if st.button(
    "💾 Save Evaluation",
    use_container_width=True
):

    df_new = pd.DataFrame([save_data])

    if os.path.exists("history.csv"):
        df_old = pd.read_csv("history.csv")
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv("history.csv", index=False)

    st.success("Evaluation saved successfully!")

st.subheader("📁 Evaluation History")

if os.path.exists("history.csv"):

    history_df = pd.read_csv("history.csv")

    st.dataframe(
        history_df,
        use_container_width=True
    )

else:
    st.info("No evaluation history available.")

st.subheader("📈 Workforce Performance Trend")

if os.path.exists("history.csv"):

    trend_fig = go.Figure()

    trend_fig.add_trace(go.Scatter(
        y=history_df["CF"],
        mode='lines+markers',
        name='CF Trend'
    ))

    trend_fig.update_layout(
        title="Certainty Factor Trend",
        xaxis_title="Evaluation Index",
        yaxis_title="CF Value",
        height=400
    )

    st.plotly_chart(
        trend_fig,
        use_container_width=True
    )
st.subheader("📊 Performance Distribution")

if os.path.exists("history.csv"):

    category_count = history_df["Kategori"].value_counts()

    pie_fig = go.Figure(
        data=[
            go.Pie(
                labels=category_count.index,
                values=category_count.values,
                hole=0.4
            )
        ]
    )

    pie_fig.update_layout(
        height=400
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )
st.subheader("📌 Average Workforce Metrics")

if os.path.exists("history.csv"):

    avg1, avg2, avg3, avg4, avg5 = st.columns(5)

    avg1.metric(
        "Avg ENG",
        round(history_df["ENG"].mean(), 1)
    )

    avg2.metric(
        "Avg AIS",
        round(history_df["AIS"].mean(), 1)
    )

    avg3.metric(
        "Avg STR",
        round(history_df["STR"].mean(), 1)
    )

    avg4.metric(
        "Avg DC",
        round(history_df["DC"].mean(), 1)
    )

    avg5.metric(
        "Avg SRC",
        round(history_df["SRC"].mean(), 1)
    )
if os.path.exists("history.csv"):

    with open("history.csv", "rb") as file:

        st.download_button(
            label="⬇️ Download History CSV",
            data=file,
            file_name="history.csv",
            mime="text/csv"
        )

else:
    st.info("No history file available yet.")
# =========================
# SYSTEM STATUS
# =========================
st.subheader("📌 System Status")

if kategori == "TINGGI":
    st.success(
        "🟢 Workforce system berada dalam kondisi optimal."
    )

elif kategori == "SEDANG":
    st.warning(
        "🟡 Workforce performance perlu monitoring lanjutan."
    )

else:
    st.error(
        "🔴 Workforce performance dalam kondisi kritis."
    )

st.divider()

st.markdown("""
<div style='text-align:center; color:gray; padding:10px;'>
    DSS Workforce Performance Dashboard <br>
    Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)