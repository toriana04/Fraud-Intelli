# =====================================================================
#  FRAUD TRENDS DASHBOARD (with Filters + Export Buttons)
# =====================================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline
from datetime import datetime

# =====================================================================
#  PAGE CONFIGURATION
# =====================================================================
st.set_page_config(page_title="Fraud Trends", page_icon="📈", layout="wide")

st.markdown(
    """
    <style>
    .main-title {
        text-align:center;
        font-size:2.8rem;
        background: linear-gradient(90deg, #8b5cf6, #22d3ee, #6366f1);
        -webkit-background-clip: text;
        color: transparent;
        font-weight:800;
        margin-bottom:20px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<h1 class='main-title'>📈 Fraud Trends & Evolution</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; opacity:0.8;'>Explore how fraud types and key topics change over time, filter results, and export insights.</p>",
    unsafe_allow_html=True
)

# =====================================================================
#  LOAD DATA
# =====================================================================
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")  
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# =====================================================================
#  AI MODEL
# =====================================================================
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

ai_model = load_model()

# =====================================================================
#  FRAUD TYPE DETECTOR
# =====================================================================
def detect_fraud_type(keywords):
    k = keywords.lower()
    if "ai" in k:
        return "AI Fraud"
    if "check" in k or "mail" in k:
        return "Check Fraud"
    if "elder" in k or "older" in k:
        return "Elder Fraud"
    if "account" in k or "takeover" in k:
        return "Account Takeover"
    if "scam" in k or "crypto" in k:
        return "Scams"
    if "disaster" in k:
        return "Disaster Fraud"
    return "General Fraud"

df["fraud_type"] = df["keywords"].fillna("").apply(detect_fraud_type)

# =====================================================================
#  FILTER SECTION
# =====================================================================
st.markdown("### 🔽 Filters")

# Fraud Category Filter
fraud_types = ["All"] + sorted(df["fraud_type"].unique().tolist())
selected_type = st.selectbox("Filter by Fraud Type:", fraud_types)

# Date Range Filter
all_months = sorted(df["month"].unique().tolist())
start_month = st.selectbox("Start Month:", all_months, index=0)
end_month = st.selectbox("End Month:", all_months, index=len(all_months)-1)

# Filter logic
mask = (df["month"] >= start_month) & (df["month"] <= end_month)
filtered_df = df[mask]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["fraud_type"] == selected_type]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# =====================================================================
#  TREND VISUALIZATION
# =====================================================================
st.markdown("### 📊 Fraud Type Trends Over Time")

trend_data = filtered_df.groupby(["month", "fraud_type"]).size().reset_index(name="count")
pivot = trend_data.pivot(index="month", columns="fraud_type", values="count").fillna(0)

fig, ax = plt.subplots(figsize=(10, 5))
pivot.plot(ax=ax, linewidth=2)
plt.title("Fraud Type Frequency Over Time", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Number of Articles")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title="Fraud Type", bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig)

# =====================================================================
#  KEYWORD HEATMAP
# =====================================================================
st.markdown("### 🔥 Keyword Frequency Heatmap")

kw_split = filtered_df["keywords"].dropna().apply(lambda x: [k.strip() for k in x.split(",")])
all_keywords = [k for sublist in kw_split for k in sublist]
kw_df = pd.DataFrame({"keyword": all_keywords})
kw_counts = kw_df["keyword"].value_counts().head(15)

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.heatmap(
    kw_counts.to_frame().T,
    cmap="coolwarm",
    cbar=False,
    annot=True,
    fmt="d",
    linewidths=1,
    ax=ax2
)
plt.title("Top 15 Keywords (Filtered)", fontsize=14)
st.pyplot(fig2)

# =====================================================================
#  AI TREND INTERPRETATION
# =====================================================================
st.markdown("### 🤖 AI Interpretation of Trends")

trend_summary = (
    "Trend summary for filtered data:\n" +
    "\n".join([f"{m}: {', '.join([f'{k}={int(v)}' for k,v in pivot.loc[m].items()])}" for m in pivot.index])
)

prompt = (
    f"Analyze these month-by-month fraud frequency counts and explain trending risks, "
    f"rising or falling patterns, and potential insights.\n\n{trend_summary}"
)

with st.spinner("AI analyzing trends..."):
    ai_output = ai_model(prompt, max_length=200)[0]["generated_text"]

st.success(ai_output)

# =====================================================================
#  EXPORT DATA
# =====================================================================
st.markdown("### 💾 Export Data")

# Full filtered dataset export
csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=csv_filtered,
    file_name=f"filtered_fraud_data_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

# Trend data export
csv_trends = pivot.reset_index().to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Trend Data (CSV)",
    data=csv_trends,
    file_name=f"fraud_trends_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

# Preview table
st.markdown("### 🗂️ Filtered Data Preview")
st.dataframe(filtered_df[["title", "fraud_type", "date", "keywords"]].sort_values("date", ascending=False).head(15))
