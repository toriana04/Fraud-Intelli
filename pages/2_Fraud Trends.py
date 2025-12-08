import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import itertools
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

from intellifraud_ui import inject_light_ui, sidebar_logo
from load_data_supabase import load_fraud_data

# ---------------------------------------------
# PAGE CONFIG & UI
# ---------------------------------------------
st.set_page_config(page_title="Fraud Trends", layout="wide")
inject_light_ui()
sidebar_logo()

# ---------------------------------------------
# HEADER
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
# LOAD DATA FROM SUPABASE
# ---------------------------------------------
@st.cache_data
def load_data():
    df = load_fraud_data()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    def ensure_list(x):
        if isinstance(x, list):
            return x
        try:
            return eval(x)
        except:
            return []
    df["keywords"] = df["keywords"].apply(ensure_list)

    return df

df = load_data()

# ---------------------------------------------
# KEYWORD PROCESSING
# ---------------------------------------------
all_keywords = [kw for lst in df["keywords"] for kw in lst]
keyword_freq = pd.Series(all_keywords).value_counts().reset_index()
keyword_freq.columns = ["keyword", "count"]


# =====================================================
# SECTION 0 — TOP FRAUD KEYWORDS (MOVED TO TOP)
# =====================================================
st.subheader("🏆 Top Fraud Keywords")
st.markdown("""
<p style='font-size:16px; margin-top:-10px; color:#0A1A2F;'>
A snapshot of the most common fraud-related keywords.
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


# =====================================================
# SECTION 1 — HEATMAP (DAY vs HOUR)
# =====================================================
st.subheader("🔥 Fraud Mentions Heatmap (Day vs Hour)")
st.markdown("<p style='color:#0A1A2F;'>When do enforcement actions peak?</p>", unsafe_allow_html=True)

df["day_of_week"] = df["timestamp"].dt.day_name()
df["hour"] = df["timestamp"].dt.hour

heatmap_data = df.pivot_table(
    index="day_of_week",
    columns="hour",
    values="title",
    aggfunc="count"
).fillna(0)

ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
heatmap_data = heatmap_data.reindex(ordered_days)

fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(heatmap_data, cmap="Blues", linewidths=.5, ax=ax)
ax.set_title("Fraud Mentions by Day & Hour")
st.pyplot(fig)


# =====================================================
# SECTION 2 — KEYWORD BAR CHART
# =====================================================
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


# =====================================================
# SECTION 3 — INTERACTIVE NETWORK GRAPH (PyVis)
# =====================================================
st.subheader("🕸️ Interactive Keyword Network")
st.markdown("""
<p style='color:#0A1A2F;'>
Drag nodes • Hover to see connections • Zoom to explore the fraud landscape.
</p>
""", unsafe_allow_html=True)

# Build co-occurrence pairs
pairs = []
for kw_list in df["keywords"]:
    if len(kw_list) > 1:
        pairs.extend(itertools.combinations(kw_list, 2))

pair_counts = {}
for a, b in pairs:
    pair = tuple(sorted([a, b]))
    pair_counts[pair] = pair_counts.get(pair, 0) + 1

MIN_EDGE_WEIGHT = 3
filtered_pairs_
