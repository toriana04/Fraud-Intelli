import streamlit as st
import pandas as pd
import re

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Fraud Explorer", layout="wide")

st.markdown("""
<div style="text-align:center; margin-bottom:20px;">
    <img src="https://i.imgur.com/kIzoyP2.png" width="150" style="border-radius:20px;"/>
</div>

<h1 style="text-align:center; color:#04d9ff; font-weight:900;">
🗂️ Fraud Explorer
</h1>

<p style="text-align:center; font-size:18px;">
Browse enforcement actions and regulatory alerts organized by fraud category.
</p>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")

    # Parse comma-separated keywords
    df["keywords"] = df["keywords"].fillna("").apply(
        lambda x: [k.strip().lower() for k in x.split(",") if k.strip()]
    )

    return df

df = load_data()

# ------------------------------------------------------------
# CATEGORY DEFINITIONS — EXPANDED TERMS FOR BETTER MATCHING
# ------------------------------------------------------------
FRAUD_CATEGORIES = {
    "Investment Fraud": [
        "investment", "investor", "advisor", "securities", "broker", "portfolio",
        "offering", "private placement", "unregistered", "misleading"
    ],
    "Identity Theft": [
        "identity", "impersonation", "personal information", "stolen identity", 
        "fake id", "documents"
    ],
    "Market Manipulation": [
        "manipulation", "pump", "dump", "spoof", "false volume", "artificial price",
        "market manipulation"
    ],
    "Insider Trading": [
        "insider", "non-public", "material info", "tipper", "tippee"
    ],
    "Ponzi / Pyramid Schemes": [
        "ponzi", "pyramid", "high yield", "guaranteed return", "recruiting"
    ],
    "Cyber Fraud": [
        "phishing", "cyber", "breach", "hack", "malware", "email scam"
    ],
    "Money Laundering": [
        "launder", "illicit funds", "conceal", "transfer", "wire"
    ],
    "Affinity Fraud": [
        "church", "community", "group targeting", "affinity"
    ],
    "Elder Fraud": [
        "elder", "senior", "older adult", "exploitation"
    ],
    "Account Takeover": [
        "account takeover", "credential", "unauthorized access"
    ],
}


# ------------------------------------------------------------
# SMART MATCHING FUNCTION
# ------------------------------------------------------------
def keyword_matches(article_kw, category_terms):
    """
    Returns the number of partial matches between article keywords and category keywords.
    Partial match examples:
    - "manipulation" matches "manipulate"
    - "investment fraud" matches "investment"
    - "phishing email" matches "phish"
    """
    score = 0

    for a_kw in article_kw:
        for c_kw in category_terms:

            # Normalize
            a = a_kw.lower()
            c = c_kw.lower()

            # Partial match
            if c in a or a in c:
                score += 1

            # Regex root match (manipulate/manipulation)
            if re.match(rf"{c[:-2]}", a):
                score += 1

    return score


def get_articles_by_category(category_name):
    """Return articles matched to a category using smart scoring."""
    terms = FRAUD_CATEGORIES[category_name]
    results = []

    for _, row in df.iterrows():
        score = keyword_matches(row["keywords"], terms)
        if score > 0:
            results.append((score, row))

    # Sort best match first
    results.sort(key=lambda x: x[0], reverse=True)

    return [row for score, row in results]


# ------------------------------------------------------------
# CATEGORY UI
# ------------------------------------------------------------
st.subheader("🧭 Select a Fraud Category")

category = st.selectbox(
    "Choose a category:",
    list(FRAUD_CATEGORIES.keys()),
    index=0
)

st.markdown(f"<h2 style='color:#04d9ff;'>📂 {category}</h2>", unsafe_allow_html=True)


# ------------------------------------------------------------
# RETURN MATCHING ARTICLES
# ------------------------------------------------------------
articles = get_articles_by_category(category)

if not articles:
    st.warning("No articles matched — try expanding your keyword list or broadening categories.")
else:
    for row in articles:
        st.markdown(f"""
        <div style="
            background-color:#0e1117; 
            padding:18px; 
            margin-bottom:12px; 
            border-radius:12px; 
            border:1px solid #04d9ff;
        ">
            <h3 style="color:#04d9ff;">{row['title']}</h3>
            <p>{row['summary']}</p>
            <p><strong>Keywords:</strong> {", ".join(row['keywords'])}</p>
            <a href="{row['url']}" target="_blank" style="color:#04d9ff;"><strong>Read Full Article</strong></a>
        </div>
        """, unsafe_allow_html=True)
