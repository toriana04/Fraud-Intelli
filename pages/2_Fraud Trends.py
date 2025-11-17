import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------
st.set_page_config(
    page_title="Fraud Trends",
    page_icon="📈",
    layout="wide",
)

# ------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")

    # Convert timestamp into datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Extract month + year for trend grouping
    df["year_month"] = df["timestamp"].dt.to_period("M").astype(str)

    # Parse keyword list
    df["keyword_list"] = df["keywords"].fillna("").str.split(",")
    df["keyword_list"] = df["keyword_list"].apply(
        lambda lst: [k.strip() for k in lst if k.strip()]
    )

    return df

df = load_data()

# ------------------------------------------------------
# PAGE TITLE
# ------------------------------------------------------
st.markdown("""
<h1 style="text-align:center; color:#04d9ff; font-size:50px; font-weight:800;">
📈 Fraud Trends & Evolution
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; color:#cccccc; font-size:18px;">
Track how fraud topics develop over time using keyword trends and article volume.
</div>
""", unsafe_allow_html=True)

st.write("---")

# ------------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------------
st.sidebar.markdown("## 🔎 Trend Filters")

# Build keyword set
all_keywords = sorted({kw for lst in df["keyword_list"] for kw in lst})

selected_keyword = st.sidebar.selectbox(
    "Select a Fraud Keyword",
    options=["(All Keywords)"] + all_keywords
)

# ------------------------------------------------------
# TREND: ARTICLE COUNT OVER TIME
# ------------------------------------------------------
st.markdown("## 🗓 Article Volume Over Time")

if selected_keyword == "(All Keywords)":
    trend_df = (
        df.groupby("year_month")
        .size()
        .reset_index(name="count")
        .sort_values("year_month")
    )
else:
    trend_df = df[df["keyword_list"].apply(lambda lst: selected_keyword in lst)]
    trend_df = (
        trend_df.groupby("year_month")
        .size()
        .reset_index(name="count")
        .sort_values("year_month")
    )

fig = px.line(
    trend_df,
    x="year_month",
    y="count",
    markers=True,
    title=f"Article Trend for: {selected_keyword}",
    color_discrete_sequence=["#04d9ff"]
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Article Count",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FFFFFF"),
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------
# TOP TRENDING KEYWORDS (Frequency Over Time)
# ------------------------------------------------------
st.markdown("## 🔥 Top Trending Fraud Keywords")

# Flatten keyword + date pairs
keyword_time_rows = []

for _, row in df.iterrows():
    for kw in row["keyword_list"]:
        keyword_time_rows.append({
            "keyword": kw,
            "year_month": row["year_month"]
        })

keyword_time_df = pd.DataFrame(keyword_time_rows)

trend_keyword_freq = (
    keyword_time_df.groupby(["year_month", "keyword"])
    .size()
    .reset_index(name="count")
)

fig2 = px.line(
    trend_keyword_freq,
    x="year_month",
    y="count",
    color="keyword",
    title="Keyword Frequency Over Time",
)

fig2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FFFFFF"),
)

st.plotly_chart(fig2, use_container_width=True)
