import streamlit as st
import pandas as pd

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Fraud Explorer", layout="wide")

st.markdown("""
<div style="text-align:center; margin-bottom:20px;">
    <img src="https://i.imgur.com/lAVJ7Vx.png" width="150" style="border-radius:20px;"/>
</div>

<h1 style="text-align:center; color:#04d9ff; font-weight:900;">
🗂️ Fraud Explorer
</h1>

<p style="text-align:center; font-size:18px;">
Explore regulatory enforcement articles organized by real-world fraud types.
</p>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")

    # Parse keywords
    df["keywords"] = df["keywords"].fillna("").apply(
        lambda x: [k.strip().lower() for k in x.split(",") if k.strip()]
    )
    return df

df = load_data()


# ------------------------------------------------------------
# FRAUD CATEGORIES — BUILT FROM YOUR REAL DATA
# ------------------------------------------------------------
FRAUD_CATEGORIES = {
    "Investment Fraud": [
        "investment fraud", "investment scams", "investment scam", "investing",
        "fraud investment", "fraud investors", "investment frauds", "invest ai",
        "ai investment", "ai trading"
    ],
    
    "Financial Fraud": [
        "financial fraud", "financial scam", "fraud recovering", "fraud recovery",
        "fraud collaboration", "fighting fraud", "stop fraud", "fraud awareness",
        "fraud findings", "fraud specialists", "fraud trends"
    ],

    "Cyber & AI Fraud": [
        "genai fraud", "accounts genai", "computer fraudsters", "fraudsters using",
        "ai trading", "ai investment", "artificial fraud"
    ],

    "Mail & Check Fraud": [
        "check fraud", "stolen checks", "mail theft", "mail check", "mail fraud"
    ],

    "Elder Fraud": [
        "older adults", "increase fraud", "fraud exposure", "fraud risk"
    ],

    "Disaster & Emergency Fraud": [
        "disaster fraud", "natural disasters", "disaster contribute"
    ],

    "Money Laundering": [
        "money laundering", "laundering fraud", "laundering frauds", "illicit finance"
    ],
}

# Lowercase category keywords once
for cat in FRAUD_CATEGORIES:
    FRAUD_CATEGORIES[cat] = [kw.lower() for kw in FRAUD_CATEGORIES[cat]]


# ------------------------------------------------------------
# MATCHING FUNCTION
# ------------------------------------------------------------
def match_score(article_keywords, category_keywords):
    score = 0
    for a_kw in article_keywords:
        for c_kw in category_keywords:

            # Phrase-in-keyword OR keyword-in-phrase match
            if c_kw in a_kw or a_kw in c_kw:
                score += 1

    return score


def get_articles(category_name):
    """Return list of best-matching articles for a fraud category."""
    cat_keywords = FRAUD_CATEGORIES[category_name]
    results = []

    for _, row in df.iterrows():
        score = match_score(row["keywords"], cat_keywords)
        if score > 0:
            results.append((score, row))

    # Best match first
    results.sort(key=lambda x: x[0], reverse=True)

    return [row for score, row in results]


# ------------------------------------------------------------
# UI — CATEGORY PICKER
# ------------------------------------------------------------
st.subheader("🧭 Select a Fraud Category")

selected_category = st.selectbox(
    "Choose a category to explore:",
    list(FRAUD_CATEGORIES.keys())
)

st.markdown(f"<h2 style='color:#04d9ff;'>📂 {selected_category}</h2>", unsafe_allow_html=True)


# ------------------------------------------------------------
# DISPLAY MATCHING ARTICLES
# ------------------------------------------------------------
articles = get_articles(selected_category)

if not articles:
    st.warning("No matching articles found for this category yet.")
else:
    for row in articles:
        title = row["title"]
        summary = row["summary"]
        url = row["url"]
        keywords = ", ".join(row["keywords"])

        st.markdown(f"""
        <div style="
            background-color:#0e1117; 
            padding:18px; 
            margin-bottom:12px; 
            border-radius:12px; 
            border:1px solid #04d9ff;
        ">
            <h3 style="color:#04d9ff;">{title}</h3>
            <p>{summary}</p>
            <p><strong>Keywords:</strong> {keywords}</p>
            <a href="{url}" target="_blank" style="color:#04d9ff;"><strong>Read Full Article</strong></a>
        </div>
        """, unsafe_allow_html=True)

