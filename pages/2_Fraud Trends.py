import streamlit as st
import pandas as pd
import altair as alt
from intellifraud_ui import inject_light_ui, sidebar_logo

# NEW — load data from Supabase instead of a local CSV
from load_data_supabase import load_fraud_data

# ---------------------------------------------
# PAGE CONFIG & UI
# ---------------------------------------------
st.set_page_config(page_title="Fraud Trends", layout="wide")
inject_light_ui()
sidebar_logo()

# ---------------------------------------------
# HEADER HERO (YOUR ORIGINAL)
# ---------------------------------------------
st.markdown("""
<div style="
    padding: 25px; 
    background: #F5F7FA; 
    border-radius: 15px; 
    border: 1px solid #E6E9EF; 
    margin-bottom: 20px;
    text-align:center;
">
    <h1 style="color:#0A1A2F; margin-bottom:5px;">
        📊 Fraud Trends & Analytics
    </h1>
    <p style="color:#4A5B6E; font-size:16px; margin-top:0;">
        Explore top fraud patterns, keyword activity, and signals across published reports.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------
# LOAD DATA FROM SUPABASE
# ---------------------------------------------
df = load_fraud_data()

# ---------------------------------------------
# TOP FRAUD KEYWORDS — ORIGINAL VERSION
# ---------------------------------------------
st.subheader("🔑 Top Fraud Keywords")

keyword_counts = (
    df["keywords"]
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .reset_index()
)
keyword_counts.columns = ["Keyword", "Count"]

chart = (
    alt.Chart(keyword_counts[:20])
        .mark_bar()
        .encode(
            x=alt.X("Count:Q", title="Frequency"),
            y=alt.Y("Keyword:N", sort="-x", title="Keyword")
        )
        .properties(height=450)
)

st.altair_chart(chart, use_container_width=True)

# ---------------------------------------------
# FULL KEYWORD LIST — ORIGINAL VERSION
# ---------------------------------------------
st.subheader("📄 Full Fraud Keyword List")

all_keywords = (
    df["keywords"]
        .str.split(",")
        .explode()
        .str.strip()
        .reset_index(drop=True)
)

full_keyword_df = pd.DataFrame({"Keyword": all_keywords})

st.dataframe(full_keyword_df, use_container_width=True)
