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

st.title("🔎 Fraud Explorer")

@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")
    return df

df = load_data()

# Search bar
query = st.text_input("Search articles by keyword, title, or content:")

if query:
    query = query.lower()
    results = df[df.apply(lambda row:
        query in str(row).lower(), axis=1)]
else:
    results = df

st.write(f"### {len(results)} Articles Found")
st.dataframe(results)
