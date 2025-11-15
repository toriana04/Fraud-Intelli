# ============================================================
#   FRAUD INTELLI PREMIUM BRAND THEME (FULL DARK MODE)
# ============================================================

st.markdown("""
<style>

    /* Global BG */
    .main, .reportview-container {
        background-color: #0A0F24 !important;
        color: #FFFFFF !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #11172B !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    section[data-testid="stSidebar"] * {
        color: #D6E2FF !important;
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #00F2FF !important;
        font-weight: 800 !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #8A2BE2, #00F2FF);
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.3rem;
        font-weight: 700;
        font-size: 16px;
    }

    .stButton>button:hover {
        opacity: 0.85;
        transform: scale(1.02);
        transition: 0.2s ease;
    }

    /* Text Inputs */
    .stTextInput>div>div>input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] {
        background-color: #121A2E;
        color: white !important;
        border: 1px solid #8A2BE2 !important;
        border-radius: 6px;
    }

    /* Dataframes */
    .stDataFrame, .dataframe {
        background-color: #11172B !important;
        color: white !important;
    }

    /* Alerts */
    .stAlert {
        background-color: rgba(138, 43, 226, 0.15) !important;
        border-left: 4px solid #8A2BE2 !important;
        color: #E6D9FF !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 7px; }
    ::-webkit-scrollbar-thumb {
        background: #8A2BE2;
        border-radius: 4px;
    }

    /* Fraud Intelli Cards */
    .fraud-card {
        background-color: #11172B;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00F2FF;
        margin-bottom: 15px;
        color: white;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
#   FRAUD INTELLI ANIMATED LOGO SPINNER  (Glow + Rotate Combo)
# ============================================================

st.markdown("""
<style>

@keyframes spinpulse {
  0% {
    transform: rotate(0deg) scale(1);
    filter: drop-shadow(0 0 0 #00F2FF);
  }
  50% {
    transform: rotate(180deg) scale(1.05);
    filter: drop-shadow(0 0 12px #00F2FF);
  }
  100% {
    transform: rotate(360deg) scale(1);
    filter: drop-shadow(0 0 0 #00F2FF);
  }
}

.spinner-premium {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 40px;
}

.spinner-logo-premium {
    width: 150px;
    animation: spinpulse 2.5s infinite ease-in-out;
}

</style>
""", unsafe_allow_html=True)

def fraud_intelli_spinner(message="Fraud Intelli is analyzing..."):
    st.markdown(f"""
        <h4 style='text-align:center; color:#8A2BE2;'>{message}</h4>
        <div class="spinner-premium">
            <img src="https://i.imgur.com/kIzoyP2.png" class="spinner-logo-premium">
        </div>
    """, unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline
from datetime import datetime

# ===== BRAND THEME CSS (included as shown above) =====

st.image("https://i.imgur.com/kIzoyP2.png", width=140)
st.markdown("<h1 style='text-align:center;'>📈 Fraud Trends & Evolution</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.8;'>Track how fraud topics develop over time.</p>", unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# --- Fraud Type Classification ---
def detect_fraud_type(keywords):
    k = keywords.lower()
    if "ai" in k: return "AI Fraud"
    if "check" in k: return "Check Fraud"
    if "elder" in k or "older" in k: return "Elder Fraud"
    if "account" in k: return "Account Takeover"
    if "scam" in k: return "Scams"
    if "disaster" in k: return "Disaster Fraud"
    return "General Fraud"

df["fraud_type"] = df["keywords"].fillna("").apply(detect_fraud_type)

# --- Filters ---
st.markdown("### 🔽 Filters")
fraud_types = ["All"] + sorted(df["fraud_type"].unique())
selected_type = st.selectbox("Fraud Type:", fraud_types)

months = sorted(df["month"].unique())
start_month = st.selectbox("Start:", months, index=0)
end_month = st.selectbox("End:", months, index=len(months)-1)

filtered = df[(df["month"] >= start_month) & (df["month"] <= end_month)]
if selected_type != "All":
    filtered = filtered[filtered["fraud_type"] == selected_type]

# --- Trend Chart ---
st.markdown("### 📊 Frequency Over Time")

trend = filtered.groupby(["month", "fraud_type"]).size().reset_index(name="count")
pivot = trend.pivot(index="month", columns="fraud_type", values="count").fillna(0)

fig, ax = plt.subplots(figsize=(10,5))
colors = ["#00F2FF", "#8A2BE2", "#5EE7FF", "#FF66C4", "#0097A7"]
pivot.plot(ax=ax, linewidth=2, color=colors[:len(pivot.columns)])

ax.set_facecolor("#0A0F24")
fig.set_facecolor("#0A0F24")
plt.xlabel("Month", color="white")
plt.ylabel("Count", color="white")
plt.title("Fraud Trends Over Time", color="#00F2FF")
plt.xticks(color="white", rotation=45)
plt.yticks(color="white")
plt.grid(color="#333333", linestyle="--", alpha=0.3)

st.pyplot(fig)

# --- Heatmap ---
st.markdown("### 🔥 Keyword Heatmap")

kw_split = filtered["keywords"].dropna().apply(lambda x: x.split(","))
all_kw = [w.strip() for sub in kw_split for w in sub]
kw_df = pd.DataFrame({"keyword": all_kw})
top_kw = kw_df["keyword"].value_counts().head(15)

fig2, ax2 = plt.subplots(figsize=(8,3))
sns.heatmap(
    top_kw.to_frame().T,
    cmap=sns.color_palette(["#8A2BE2", "#00F2FF"], as_cmap=True),
    annot=True, fmt="d", cbar=False, linewidths=1
)
ax2.set_facecolor("#0A0F24")
plt.title("Keyword Density", color="#00F2FF")
plt.xticks(color="white", rotation=45)
plt.yticks(color="white")

st.pyplot(fig2)

# --- Export ---
st.markdown("### 💾 Export Data")
st.download_button(
    "Download Filtered Data (CSV)",
    filtered.to_csv(index=False),
    file_name="filtered_fraud_data.csv",
    mime="text/csv"
)