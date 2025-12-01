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
#                   3 — INTELLIFRAUD FRAUD DEFINITIONS
# =====================================================================

import streamlit as st

st.image("https://i.imgur.com/kIzoyP2.png", width=130)
st.title("📘 Fraud Definitions")

st.write("""
This page provides concise definitions of common fraud types
based on patterns identified in FINRA publications.
""")

definitions = {
    "AI Fraud": "Scams that leverage artificial intelligence, deepfakes, voice cloning, or automated impersonation.",
    "Check Fraud": "Altering, stealing, or washing checks to illegally cash or deposit funds.",
    "Elder Fraud": "Fraud schemes that intentionally target seniors or older adults.",
    "Account Takeover": "Unauthorized access to a victim's financial or personal accounts.",
    "Investment Scam": "Fraudulent investment opportunities, including cryptocurrency schemes and pump-and-dump operations.",
    "Disaster Fraud": "Scams exploiting natural disasters, relief programs, or emergency assistance.",
    "General Fraud": "Any deceptive or misleading activity intended to steal money or information."
}

for name, desc in definitions.items():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### {name}")
    st.write(desc)
    st.markdown("</div>", unsafe_allow_html=True)
