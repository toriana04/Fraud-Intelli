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
#                   1 — INTELLIFRAUD FRAUD EXPLORER
# =====================================================================

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

# =====================================================================
#                            PAGE UI
# =====================================================================
st.image("https://i.imgur.com/kIzoyP2.png", width=130)
st.title("🔍 IntelliFraud Explorer")

st.write("Browse all FINRA fraud-related articles, filter by category, date, and keywords.")

# Filters
col1, col2 = st.columns(2)

with col1:
    fraud_filter = st.selectbox(
        "Filter by Fraud Category",
        ["All"] + list(FRAUD_TAGS.keys())
    )

with col2:
    date_range = st.date_input(
        "Filter by Date Range",
        value=(df["date"].min(), df["date"].max())
    )

keyword_search = st.text_input("Keyword Search (optional):")

# Apply filters
filtered = df.copy()

if fraud_filter != "All":
    filtered = filtered[filtered["tag"] == fraud_filter]

start, end = date_range
filtered = filtered[(filtered["date"] >= pd.to_datetime(start)) &
                    (filtered["date"] <= pd.to_datetime(end))]

if keyword_search:
    k = keyword_search.lower()
    filtered = filtered[filtered["summary"].str.lower().str.contains(k) |
                        filtered["keywords"].str.lower().str.contains(k)]

# =====================================================================
#                        DISPLAY RESULTS
# =====================================================================
st.subheader(f"Found {len(filtered)} Articles")

for _, row in filtered.iterrows():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown(f"### **{row['title']}**")
    st.write(f"📅 **Published:** {row['date'].date()}")
    st.write(f"🏷 **Category:** `{row['tag']}`")
    st.write(f"🔗 [Read Article]({row['url']})")

    with st.expander("Summary"):
        st.write(row["summary"])

    st.markdown("**Keywords:**")
    for kw in row["keywords"].split(","):
        st.markdown(f"<span class='keyword-chip'>{kw.strip()}</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
