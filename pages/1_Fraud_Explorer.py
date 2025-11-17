import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------
st.set_page_config(
    page_title="Fraud Explorer",
    page_icon="🕵️‍♀️",
    layout="wide",
)

# ------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")

    # Convert keywords string -> list
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
<h1 style="text-align:center; color:#04d9ff; font-size:52px; font-weight:800;">
🕵️‍♀️ Fraud Explorer Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; color:#cccccc; font-size:18px;">
Explore fraud-related FINRA articles by keyword, summaries, and time trends.  
Use the filters on the left to drill deeper into specific fraud topics.
</div>
""", unsafe_allow_html=True)

st.write(" ")

# ------------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------------
st.sidebar.markdown("## 🔎 Filters")

# Build keyword filter list
all_keywords = sorted({kw for lst in df["keyword_list"] for kw in lst})

selected_keywords = st.sidebar.multiselect(
    "Filter by Keyword:",
    all_keywords,
    default=[]
)

# Filter logic
if selected_keywords:
    filtered_df = df[df["keyword_list"].apply(
        lambda lst: any(kw in lst for kw in selected_keywords)
    )]
else:
    filtered_df = df.copy()

st.sidebar.markdown("---")
st.sidebar.write(f"### Showing **{len(filtered_df)}** articles")

# ------------------------------------------------------
# CHARTS SECTION
# ------------------------------------------------------
st.markdown("## 📊 Keyword Frequency Overview")

# Calculate keyword frequencies
keyword_freq = {}
for lst in df["keyword_list"]:
    for kw in lst:
        keyword_freq[kw] = keyword_freq.get(kw, 0) + 1

freq_df = pd.DataFrame({
    "keyword": list(keyword_freq.keys()),
    "count": list(keyword_freq.values())
}).sort_values("count", ascending=False)

fig = px.bar(
    freq_df.head(20),
    x="keyword",
    y="count",
    title="Top 20 Most Frequent Fraud Keywords",
    color="count",
    color_continuous_scale="Teal",
)

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#FFFFFF"),
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------
# ARTICLE TABLE SECTION
# ------------------------------------------------------
st.markdown("## 📰 Filtered Articles")

if filtered_df.empty:
    st.warning("No articles match the selected keywords.")
else:
    for idx, row in filtered_df.iterrows():
        st.markdown(f"""
        <div style="background-color:#111; padding:18px; border-radius:12px; margin-bottom:20px;">
            <h3 style="color:#04d9ff;">{row['title']}</h3>
            <p style="color:#ccc;">{row['summary']}</p>
            <p><b style="color:#04d9ff;">Keywords:</b> 
                <span style="color:#aaa;">{row['keywords']}</span></p>
            <a href="{row['url']}" target="_blank" 
               style="color:#00eaff; font-size:16px; font-weight:bold; text-decoration:none;">
                🔗 Read Full Article
            </a>
        </div>
        """, unsafe_allow_html=True)
