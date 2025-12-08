import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import ast
import networkx as nx

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
# LOAD DATA FROM SUPABASE
# ---------------------------------------------
@st.cache_data
def load_data():
    df = load_fraud_data()

    # Ensure timestamp parses correctly
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Ensure keywords are lists
    def safe_list(x):
        if isinstance(x, list):
            return x
        try:
            return ast.literal_eval(x)
        except:
            return []
    df["keywords"] = df["keywords"].apply(safe_list)

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
# SECTION 0 — TOP KEYWORDS
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
# SECTION 1.5 — HEATMAP (NEW)
# ---------------------------------------------
st.subheader("🔥 Fraud Mentions Heatmap (Day vs Hour)")
st.markdown("""
<p style='color:#0A1A2F;'>Patterns of fraud-related activity by day of week and hour.</p>
""", unsafe_allow_html=True)

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
ax.set_title("Fraud Mentions by Day and Hour")
st.pyplot(fig)

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
# SECTION 2.5 — KEYWORD NETWORK GRAPH (NEW)
# ---------------------------------------------
st.subheader("🕸️ Keyword Co-Occurrence Network Graph")
st.markdown("""
<p style='color:#0A1A2F;'>Relationships between fraud keywords based on co-occurrence patterns.</p>
""", unsafe_allow_html=True)

# Generate keyword pairs
pairs = []
for kw_list in df["keywords"]:
    if len(kw_list) > 1:
        combos = itertools.combinations(kw_list, 2)
        pairs.extend(combos)

# Count frequencies
pair_counts = {}
for a, b in pairs:
    pair = tuple(sorted([a, b]))
    pair_counts[pair] = pair_counts.get(pair, 0) + 1

# Build graph
G = nx.Graph()
for (a, b), weight in pair_counts.items():
    if weight >= 2:  # threshold to reduce noise
        G.add_edge(a, b, weight=weight)

fig2, ax2 = plt.subplots(figsize=(10, 8))
pos = nx.spring_layout(G, k=0.4, seed=42)

node_sizes = [800 + (300 * G.degree(n)) for n in G.nodes()]

nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="skyblue")
nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=10)

plt.title("Keyword Co-Occurrence Network")
plt.axis("off")

st.pyplot(fig2)

# ---------------------------------------------
# SECTION 3 — Full Keyword List
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
