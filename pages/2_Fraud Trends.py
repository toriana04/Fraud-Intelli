import streamlit as st
import pandas as pd
import io
import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = "DTSC_project"
SUPABASE_CSV_PATH = "csv/fraud_articles.csv"

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_data
def load_data():
    sb = get_supabase()
    file_bytes = sb.storage.from_(SUPABASE_BUCKET).download(SUPABASE_CSV_PATH)
    df = pd.read_csv(io.BytesIO(file_bytes))

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["summary"] = df["summary"].astype(str)
    df["keywords"] = df["keywords"].astype(str)

    return df
# =====================================================================
#                       2 — INTELLIFRAUD TRENDS
# =====================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import io
import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = "DTSC_project"
SUPABASE_CSV_PATH = "csv/fraud_articles.csv"

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_data
def load_data():
    sb = get_supabase()
    file_bytes = sb.storage.from_(SUPABASE_BUCKET).download(SUPABASE_CSV_PATH)
    df = pd.read_csv(io.BytesIO(file_bytes))

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

df = load_data()

# Fraud categories
FRAUD_TAGS = {
    "AI Fraud": ["ai", "deepfake", "artificial intelligence"],
    "Check Fraud": ["check fraud", "check washing"],
    "Elder Fraud": ["older adult", "senior"],
    "Account Takeover": ["account takeover", "hacked"],
    "Investment Scam": ["crypto", "investment scam", "pump and dump"],
    "Disaster Fraud": ["disaster", "relief scam"],
    "General Fraud": ["fraud", "scam"]
}

def classify(text):
    t = str(text).lower()
    for tag, words in FRAUD_TAGS.items():
        if any(w in t for w in words):
            return tag
    return "General Fraud"

df["tag"] = df["summary"].apply(classify)
df["month"] = df["date"].dt.to_period("M")

# =====================================================================
#                           PAGE UI
# =====================================================================
st.image("https://i.imgur.com/kIzoyP2.png", width=130)
st.title("📈 IntelliFraud — Fraud Trends")

st.write("Analyze fraud-related publication trends using FINRA article dates.")

# =====================================================================
#                       CHART 1 — MONTHLY COUNTS
# =====================================================================
monthly_counts = df.groupby("month").size().reset_index(name="count")
monthly_counts["month"] = monthly_counts["month"].astype(str)

fig1 = px.line(
    monthly_counts,
    x="month",
    y="count",
    title="Fraud Articles Per Month",
    markers=True
)
st.plotly_chart(fig1, use_container_width=True)

# =====================================================================
#                       CHART 2 — CATEGORY OVER TIME
# =====================================================================
cat_month = df.groupby(["month", "tag"]).size().reset_index(name="count")
cat_month["month"] = cat_month["month"].astype(str)

fig2 = px.line(
    cat_month,
    x="month",
    y="count",
    color="tag",
    title="Fraud Categories Over Time"
)
st.plotly_chart(fig2, use_container_width=True)
