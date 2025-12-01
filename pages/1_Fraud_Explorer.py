import streamlit as st
import pandas as pd

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
    
    # Parse keywords
    df["keywords"] = df["keywords"].fillna("").apply(
        lambda x: [k.strip().lower() for k in x.split(",") if k.strip()]
    )
    return df

df = load_data()


# ------------------------------------------------------------
# CATEGORY DEFINITIONS + MAPPING KEYWORDS
# ------------------------------------------------------------
FRAUD_CATEGORIES = {
    "Investment Fraud": ["investment", "scheme", "securities", "advisor", "portfolio", "investor"],
    "Identity Theft": ["identity", "theft", "impersonation", "documents", "personal info"],
    "Market Manipulation": ["manipulation", "pump", "dump", "trading volume", "artificial"],
    "Insider Trading": ["insider", "non-public", "material info"],
    "Ponzi / Pyramid Schemes": ["ponzi", "pyramid", "recruit", "returns", "high-yield"],
    "Cyber Fraud": ["phishing", "hacking", "cyber", "breach", "email scam"],
    "Money Laundering": ["laundering", "illicit funds", "conceal", "transactions"],
    "Affinity Fraud": ["church", "community", "targeting group", "affinity"],
    "Elder Fraud": ["elder", "senior", "older adults"],
    "Account Takeover": ["account takeover", "unauthorized access", "credentials"],
}


# ------------------------------------------------------------
# MATCH ARTICLES TO CATEGORY (automatic classification)
# ------------------------------------------------------------
def score_article_for_category(article_keywords, category_keywords):
    """Return how many category keywords overlap with article keywords."""
    return sum(1 for kw in article_keywords if kw in category_keywords)


def get_articles_by_category(category_name):
    """Return articles matched to a category in descending score order."""
    keywords_for_category = [k.lower() for k in FRAUD_CATEGORIES[category_name]]

    scored = []

    for _, row in df.iterrows():
        score = score_article_for_category(row["keywords"], keywords_for_category)
        if score > 0:
            scored.append((score, row))

    # Sort by best match
    scored.sort(key=lambda x: x[0], reverse=True)

    return [row for score, row in scored]


# ------------------------------------------------------------
# CATEGORY SELECTION UI
# ------------------------------------------------------------
st.subheader("🧭 Select a Fraud Category")

category = st.selectbox(
    "Choose a category:",
    list(FRAUD_CATEGORIES.keys()),
    index=0
)

st.markdown(f"""
<h2 style="color:#04d9ff; margin-top:10px;">📂 {category}</h2>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# DISPLAY MATCHED ARTICLES FOR SELECTED CATEGORY
# ------------------------------------------------------------
articles = get_articles_by_category(category)

if not articles:
    st.info("No articles matched this category based on keyword similarity.")
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
