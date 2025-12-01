import streamlit as st
import pandas as pd
import altair as alt

# ---------------------------------------------
# PAGE CONFIG & HEADER
# ---------------------------------------------
st.set_page_config(page_title="Fraud Trends", layout="wide")

st.markdown("""
<div style="text-align:center; margin-bottom:10px;">
    <img src="https://i.imgur.com/kIzoyP2.png" width="140" style="border-radius:20px;"/>
</div>
<h1 style="text-align:center; color:#04d9ff; font-weight:900;">📊 Fraud Trends & Analytics</h1>
<p style="text-align:center; font-size:18px;">
Explore trends in fraud-related articles, keyword frequencies, and historical patterns.
</p>
""", unsafe_allow_html=True)

# ---------------------------------------------
# LOAD DATA
# ---------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Clean keywords: convert comma-separated strings into lists
    df["keywords"] = df["keywords"].fillna("").apply(lambda x: [k.strip().lower() for k in x.split(",") if k.strip()])

    return df

df = load_data()

# ---------------------------------------------
# SECTION 1: Monthly Article Trend
# ---------------------------------------------
st.subheader("📅 Articles Published Over Time")

monthly = (
    df.groupby(df["timestamp"].dt.to_period("M"))
      .size()
      .reset_index(name="count")
)

monthly["timestamp"] = monthly["timestamp"].astype(str)

line_chart = (
    alt.Chart(monthly)
    .mark_line(point=True)
    .encode(
        x=alt.X("timestamp:N", title="Month"),
        y=alt.Y("count:Q", title="Number of Articles"),
        tooltip=["timestamp", "count"]
    )
    .properties(width="container", height=350)
)

st.altair_chart(line_chart, use_container_width=True)

# ---------------------------------------------
# SECTION 2: Keyword Frequency Bar Chart
# ---------------------------------------------
st.subheader("🔑 Most Common Fraud Keywords")

# Flatten keyword lists into one long list
all_keywords = [kw for lst in df["keywords"] for kw in lst]

keyword_freq = (
    pd.Series(all_keywords)
    .value_counts()
    .reset_index()
)

keyword_freq.columns = ["keyword", "count"]

# Bar chart (top 20)
bar_chart = (
    alt.Chart(keyword_freq.head(20))
    .mark_bar()
    .encode(
        x=alt.X("count:Q", title="Frequency"),
        y=alt.Y("keyword:N", sort="-x", title="Keyword"),
        tooltip=["keyword", "count"]
    )
    .properties(height=500)
)

st.altair_chart(bar_chart, use_container_width=True)

# ---------------------------------------------
# SECTION 3: Top Keywords Table
# ---------------------------------------------
st.subheader("🏆 Top Fraud Keywords (Full List)")

st.dataframe(keyword_freq, use_container_width=True)
