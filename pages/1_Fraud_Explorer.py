import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
#   FRAUD INTELLI PREMIUM BRAND THEME (FULL DARK MODE)
# ============================================================

st.markdown("""
<style>

    /* Global BG */
    .main, .reportview-container {
        background-color: #0A0F24 !important;
        color: #FFFFFF !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #11172B !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    section[data-testid="stSidebar"] * {
        color: #D6E2FF !important;
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #00F2FF !important;
        font-weight: 800 !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #8A2BE2, #00F2FF);
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.3rem;
        font-weight: 700;
        font-size: 16px;
    }

    .stButton>button:hover {
        opacity: 0.85;
        transform: scale(1.02);
        transition: 0.2s ease;
    }

    /* Text Inputs */
    .stTextInput>div>div>input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] {
        background-color: #121A2E;
        color: white !important;
        border: 1px solid #8A2BE2 !important;
        border-radius: 6px;
    }

    /* Dataframes */
    .stDataFrame, .dataframe {
        background-color: #11172B !important;
        color: white !important;
    }

    /* Alerts */
    .stAlert {
        background-color: rgba(138, 43, 226, 0.15) !important;
        border-left: 4px solid #8A2BE2 !important;
        color: #E6D9FF !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 7px; }
    ::-webkit-scrollbar-thumb {
        background: #8A2BE2;
        border-radius: 4px;
    }

    /* Fraud Intelli Cards */
    .fraud-card {
        background-color: #11172B;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00F2FF;
        margin-bottom: 15px;
        color: white;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
#   FRAUD INTELLI ANIMATED LOGO SPINNER  (Glow + Rotate Combo)
# ============================================================

st.markdown("""
<style>

@keyframes spinpulse {
  0% {
    transform: rotate(0deg) scale(1);
    filter: drop-shadow(0 0 0 #00F2FF);
  }
  50% {
    transform: rotate(180deg) scale(1.05);
    filter: drop-shadow(0 0 12px #00F2FF);
  }
  100% {
    transform: rotate(360deg) scale(1);
    filter: drop-shadow(0 0 0 #00F2FF);
  }
}

.spinner-premium {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 40px;
}

.spinner-logo-premium {
    width: 150px;
    animation: spinpulse 2.5s infinite ease-in-out;
}

</style>
""", unsafe_allow_html=True)

def fraud_intelli_spinner(message="Fraud Intelli is analyzing..."):
    st.markdown(f"""
        <h4 style='text-align:center; color:#8A2BE2;'>{message}</h4>
        <div class="spinner-premium">
            <img src="https://i.imgur.com/kIzoyP2.png" class="spinner-logo-premium">
        </div>
    """, unsafe_allow_html=True)


# =====================================================================
#  PAGE CONFIGURATION
# =====================================================================
st.set_page_config(page_title="Fraud Explorer", page_icon="🕵️", layout="wide")

# =====================================================================
#  LOGO (SAME STYLE AS OTHER PAGES)
# =====================================================================
st.markdown(
    """
    <style>
    .app-logo {
        width: 170px;
        border-radius: 20px;
        margin-top: -10px;
        margin-bottom: 10px;
        box-shadow: 0 0 15px rgba(139,92,246,0.35);
        cursor: pointer;
        transition: 0.2s;
    }
    .app-logo:hover {
        transform: scale(1.04);
        box-shadow: 0 0 22px rgba(139,92,246,0.55);
    }
    </style>

    <div style='text-align: center;'>
        <a href="/">
            <img class='app-logo' src='../logo.png'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================================
#  LOAD DATA
# =====================================================================
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")
    df["summary"] = df["summary"].astype(str)
    df["keywords"] = df["keywords"].astype(str)
    return df

df = load_data()

# =====================================================================
#  PAGE TITLE
# =====================================================================
st.markdown(
    """
    <h1 style='
        text-align: center;
        font-size: 3rem;
        background: linear-gradient(90deg, #8b5cf6, #22d3ee, #6366f1);
        -webkit-background-clip: text;
        color: transparent;
        font-weight: 800;
        margin-bottom: 20px;
    '>
        🕵️ Fraud Explorer Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.write(
    "Explore fraud-related FINRA articles by category, keywords, and summaries. "
    "Use the filters and charts below to analyze trends and review summaries interactively."
)

# =====================================================================
#  SIDEBAR FILTERS
# =====================================================================
st.sidebar.header("🔍 Filters")

fraud_types = sorted(df["tag"].dropna().unique().tolist())
selected_types = st.sidebar.multiselect(
    "Select Fraud Categories", fraud_types, default=fraud_types
)

keyword_filter = st.sidebar.text_input(
    "Filter by Keyword (optional)",
    placeholder="e.g., AI, mail theft, crypto..."
)

# Apply filters
filtered_df = df[df["tag"].isin(selected_types)]
if keyword_filter:
    keyword_filter_lower = keyword_filter.lower()
    filtered_df = filtered_df[
        filtered_df["keywords"].str.lower().str.contains(keyword_filter_lower)
        | filtered_df["summary"].str.lower().str.contains(keyword_filter_lower)
    ]

# =====================================================================
#  CATEGORY DISTRIBUTION CHART
# =====================================================================
st.markdown("### 📊 Fraud Category Distribution")

category_counts = filtered_df["tag"].value_counts().reset_index()
category_counts.columns = ["Fraud Type", "Count"]

fig = px.bar(
    category_counts,
    x="Fraud Type",
    y="Count",
    color="Fraud Type",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    text="Count",
)
fig.update_traces(textposition="outside")
fig.update_layout(
    xaxis_title="Fraud Type",
    yaxis_title="Number of Articles",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#f6f6f6",
)
st.plotly_chart(fig, use_container_width=True)

# =====================================================================
#  ARTICLE LISTINGS (CARDS)
# =====================================================================
st.markdown("### 📰 Articles by Category")

if len(filtered_df) == 0:
    st.info("No articles match your selected filters.")
else:
    for _, row in filtered_df.iterrows():
        st.markdown(
            f"""
            <div style='
                background: rgba(255,255,255,0.06);
                padding: 20px;
                margin-bottom: 18px;
                border-radius: 18px;
                border: 1px solid rgba(255,255,255,0.12);
                backdrop-filter: blur(10px);
                transition: all .3s ease;
            '>
                <h3 style='color:#8b5cf6; margin-bottom:6px;'>{row['title']}</h3>
                <p><b>Category:</b> {row['tag']}</p>
                <p style='opacity:0.85;'>{row['summary'][:350]}...</p>
                <p>
                    <b>Keywords:</b>
                    {' '.join([f"<span style='background:rgba(139,92,246,0.15);padding:4px 10px;border-radius:12px;margin:2px;display:inline-block;border:1px solid rgba(139,92,246,0.3);'>{k.strip()}</span>" for k in row['keywords'].split(',') if k.strip()])}
                </p>
                <a href='{row['url']}' target='_blank' style='color:#22d3ee;text-decoration:none;'>🔗 Read full article</a>
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================================================
#  KEYWORD CLOUD / TABLE
# =====================================================================
st.markdown("### 🧠 Top Keywords")

keywords = (
    filtered_df["keywords"]
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
    .head(20)
    .reset_index()
)
keywords.columns = ["Keyword", "Count"]

fig2 = px.bar(
    keywords,
    x="Keyword",
    y="Count",
    color="Count",
    color_continuous_scale="Purples",
)
fig2.update_layout(
    xaxis_title="Keyword",
    yaxis_title="Frequency",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#f6f6f6",
)
st.plotly_chart(fig2, use_container_width=True)
