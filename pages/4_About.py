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
#                       4 — ABOUT INTELLIFRAUD
# =====================================================================

import streamlit as st

st.image("https://i.imgur.com/kIzoyP2.png", width=150)
st.title("ℹ️ About IntelliFraud")

st.markdown("""
IntelliFraud is an AI-powered fraud intelligence engine developed by:

- Clara Belluci  
- Troy Benner  
- Hoang Bui  
- Tori-Ana McNeil  

for the UNC Charlotte School of Data Science in partnership with USAA.

The system integrates a hybrid Selenium + Playwright web scraper,
Supabase cloud storage, NLP summarization, semantic search, and
a multi-page Streamlit dashboard.
""")
