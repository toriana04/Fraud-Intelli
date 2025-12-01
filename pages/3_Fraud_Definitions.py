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

import streamlit as st
import pandas as pd

st.title("📘 Fraud Definitions")

@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")
    return df

df = load_data()

if "fraud_type" in df.columns:
    fraud_types = sorted(df["fraud_type"].dropna().unique())
    selected = st.selectbox("Select fraud category:", fraud_types)

    filtered = df[df["fraud_type"] == selected]
    st.write(f"### {len(filtered)} Articles")
    st.dataframe(filtered)
else:
    st.info("This dataset does not contain fraud categories. Definitions will be added later.")
