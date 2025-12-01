import streamlit as st
import pandas as pd
import altair as alt
from intellifraud_ui import inject_light_ui, sidebar_logo

# ---------------------------------------------
# PAGE CONFIG & UI
# ---------------------------------------------
st.set_page_config(page_title="Fraud Trends", layout="wide")
inject_light_ui()
sidebar_logo()

# ---------------------------------------------
# HEADER HERO
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
    <p style="font-size:17px; color:#0A1A2F;">
        Explore trends in regulatory enforcement, keyword activity, and historical fraud patterns.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------
# LOAD DATA
# ---------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    df["keywords"] = df["keywords"].fillna("").apply(
        lambda x: [k.strip().lower() for k in x.split(",") if k.strip()]
    )

    return df

df = load_data()

# ---------------------------------------------
# EXTRACT & COUNT KEYWORDS
# ---------------------------------------------
all_keywords = [kw for lst in df["keywords"] for kw in lst]

keyword_freq = (
    pd.Series(all_keywords)
    .value_counts()
    .reset_index()
)

keyword_freq.columns = ["keyword", "count"]

# ---------------------------------------------
# SECTION 0 — TOP KEYWORDS (Light Mode Cards)
# ---------------------------------------------
st.subheader("🏆 Top Fraud Keywords")
st.markdown("""
<p style='font-size:16px; margin-top:-10px; color:#0A1A2F;'>
A snapshot of the most common fraud-related keywords appearing across enforcement articles.
</p>
""", unsafe_allow_html=True)

for _, row in keyword_freq.head(10).iterrows():
    st.markdown(f"""
    <div style="
        padding:14px; 
        margin-bottom:12px; 
        border-radius:10px; 
        background-color:#FFFFFF; 
        border:1px solid #E6E9EF;
        box-shadow:0 1px 3px rgba(0,0,0,0.05);
    ">
        <h3 style="color:#0A65FF; margin-bottom:4px;">{row['keyword'].capitalize()}</h3>
        <p style="font-size:15px; margin:0; color:#0A1A2F;">
            <strong>Frequency:</strong> {row['count']}
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------
# SECTION 1 — Articles Published Over Time
# ---------------------------------------------
st.subheader("📅 Articles Published Over Time")
st.markdown("""
<p style='color:#0A1A2F;'>A month-by-month view of regulatory enforcement activity.</p>
""", unsafe_allow_html=True)

monthly = (
    df.groupby(df["timestamp"].dt.to_period("M"))
      .size()
      .reset_index(name="count")
)

monthly["timestamp"] = monthly["timestamp"].astype(str)

line_chart = (
    alt.Chart(monthly)
    .mark_line(point=True, color="#0A65FF")
    .encode(
        x=alt.X("timestamp:N", title="Month"),
        y=alt.Y("count:Q", title="Number of Articles"),
        tooltip=["timestamp", "count"]
    )
    .properties(width="container", height=350)
)

st.altair_chart(line_chart, use_container_width=True)


# ---------------------------------------------
# SECTION 2 — Keyword Frequency Bar Chart
# ---------------------------------------------
st.subheader("🔑 Most Common Fraud Keywords (Bar Chart)")

bar_chart = (
    alt.Chart(keyword_freq.head(20))
    .mark_bar(color="#0A65FF")
    .encode(
        x=alt.X("count:Q", title="Frequency"),
        y=alt.Y("keyword:N", sort="-x", title="Keyword"),
        tooltip=["keyword", "count"]
    )
    .properties(height=500)
)

st.altair_chart(bar_chart, use_container_width=True)


# ---------------------------------------------
# SECTION 3 — Full Keyword List (Light Mode Cards)
# ---------------------------------------------
st.subheader("📖 Full Fraud Keyword List")

for _, row in keyword_freq.iterrows():
    st.markdown(f"""
    <div style="
        padding:14px; 
        margin-bottom:12px; 
        border-radius:10px; 
        background-color:#FFFFFF; 
        border:1px solid #E6E9EF;
        box-shadow:0 1px 3px rgba(0,0,0,0.05);
    ">
        <h3 style="color:#0A65FF; margin-bottom:4px;">
            {row['keyword'].capitalize()}
        </h3>
        <p style="font-size:15px; margin:0; color:#0A1A2F;">
            <strong>Frequency:</strong> {row['count']}
        </p>
    </div>
    """, unsafe_allow_html=True)
