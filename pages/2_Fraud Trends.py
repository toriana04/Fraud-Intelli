import streamlit as st
import pandas as pd
import altair as alt

from intellifraud_ui import inject_light_ui
from load_data_supabase import load_fraud_data

# ---------------------------------------------
# PAGE CONFIG & UI
# ---------------------------------------------
st.set_page_config(page_title="Fraud Trends", layout="wide")
inject_light_ui()

# ---------------------------------------------
# LOGO AT THE TOP (NEW)
# ---------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top:10px; margin-bottom:25px;">
        <img src="https://i.imgur.com/lAVJ7Vx.png" width="180">
        <h1 style="color:#0A1A2F; margin-top:5px;">
            Fraud Trends & Analytics
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------
# LOAD DATA
# ---------------------------------------------
df = load_fraud_data()

# ---------------------------------------------
# TOP FRAUD KEYWORDS SECTION
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
# FULL KEYWORD LIST — ALWAYS VISIBLE (NO SEARCHABLE INPUT)
# ---------------------------------------------
st.subheader("📄 Full Fraud Keyword List (Not Searchable)")

# Convert comma-separated keywords into rows
all_keywords = (
    df["keywords"]
    .str.split(",")
    .explode()
    .str.strip()
    .reset_index(drop=True)
)

full_keyword_df = pd.DataFrame({"Keyword": all_keywords})

st.dataframe(full_keyword_df, use_container_width=True)
