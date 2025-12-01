import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")
    # Optional: parse date column if it exists
    if "article_date" in df.columns:
        df["article_date"] = pd.to_datetime(df["article_date"], errors="coerce")
    return df

df = load_data()
import streamlit as st
import pandas as pd

st.set_page_config(page_title="IntelliFraud", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")
    return df

df = load_data()

st.title("🔍 IntelliFraud — Fraud Intelligence Dashboard")

st.write("""
Welcome to IntelliFraud, your centralized hub for fraud insights, trends, and enforcement actions.
Use the sidebar navigation to explore more.
""")

st.metric("Total Articles", len(df))

if "article_date" in df.columns:
    st.write("### Recent Articles")
    st.dataframe(df.sort_values("article_date", ascending=False).head(10))
else:
    st.write("### Sample of Articles")
    st.dataframe(df.head(10))
