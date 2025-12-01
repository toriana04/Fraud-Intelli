import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="HOME", layout="wide")

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
st.markdown("""
<div style="text-align:center; margin-bottom:20px;">
    <img src="https://i.imgur.com/kIzoyP2.png" width="160" style="border-radius:20px;"/>
</div>

<h1 style="text-align:center; color:#04d9ff; font-weight:900;">
🔍 Welcome to IntelliFraud
</h1>

<p style="text-align:center; font-size:18px; max-width:700px; margin:auto;">
Your interactive fraud intelligence dashboard for exploring regulatory actions, fraud trends, keyword insights, and core definitions — all in one place.
</p>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")

    # Prepare cleaned text for similarity search
    df["keywords_clean"] = df["keywords"].fillna("").astype(str)

    df["search_text"] = (
        df["title"].fillna("") + " " +
        df["summary"].fillna("") + " " +
        df["keywords_clean"]
    ).str.lower()

    return df

df = load_data()


# ------------------------------------------------------------
# TF-IDF MODEL
# ------------------------------------------------------------
@st.cache_resource
def build_tfidf():
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(df["search_text"])
    return vectorizer, matrix

vectorizer, tfidf_matrix = build_tfidf()


def get_best_article(query):
    """Return best-matching article + similarity score."""
    query_vec = vectorizer.transform([query.lower()])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    best_idx = scores.argmax()
    best_score = scores[best_idx]

    return df.iloc[best_idx], float(best_score)


# ------------------------------------------------------------
# SMART ROUTER
# ------------------------------------------------------------
def route_query(query):
    q = query.lower().strip()

    # Trends Routing
    trend_words = ["trend", "trends", "pattern", "patterns", "keyword", "keywords", "analysis", "chart"]
    if any(w in q for w in trend_words):
        st.session_state["page"] = "trends"
        st.switch_page("pages/2_Fraud Trends.py")

    # Glossary Routing
    glossary_words = ["definition", "define", "term", "terms", "glossary", "what is", "types of fraud"]
    if any(w in q for w in glossary_words):
        st.session_state["page"] = "glossary"
        st.switch_page("pages/3_Fraud Definitions.py")

    # Explorer Routing
    explorer_words = ["category", "categories", "explore", "fraud types", "fraud category"]
    if any(w in q for w in explorer_words):
        st.session_state["page"] = "explorer"
        st.switch_page("pages/1_Fraud Explorer.py")

    # Otherwise → do article similarity search
    return None


# ------------------------------------------------------------
# SEARCH BAR UI
# ------------------------------------------------------------
st.subheader("🔎 Search Across IntelliFraud")

query = st.text_input(
    "Ask a question, look up a trend, search a fraud term, or enter keywords:",
    placeholder="Try things like 'GenAI fraud', 'investment scams', or 'trend analysis'..."
)

if query:
    # First try routing
    if route_query(query) is None:
        # Then show the best article match
        best_article, score = get_best_article(query)

        st.markdown("<h3 style='color:#04d9ff;'>Top Article Match</h3>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
            background-color:#0e1117; 
            padding:18px; 
            margin-bottom:12px; 
            border-radius:12px; 
            border:1px solid #04d9ff;
        ">
            <h3 style="color:#04d9ff;">{best_article['title']}</h3>
            <p>{best_article['summary']}</p>
            <p><strong>Keywords:</strong> {best_article['keywords']}</p>
            <p><strong>Similarity Score:</strong> {score:.2f}</p>
            <a href="{best_article['url']}" target="_blank" style="color:#04d9ff;"><strong>Read Full Article</strong></a>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------
# FEATURE CARDS
# ------------------------------------------------------------
st.subheader("📂 Navigate IntelliFraud")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="background-color:#0e1117; padding:18px; border-radius:12px; border:1px solid #04d9ff;">
        <h3 style="color:#04d9ff;">🧭 Fraud Explorer</h3>
        <p>Browse fraud categories and matched articles.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color:#0e1117; padding:18px; border-radius:12px; border:1px solid #04d9ff;">
        <h3 style="color:#04d9ff;">📊 Fraud Trends</h3>
        <p>See keyword frequencies and activity over time.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background-color:#0e1117; padding:18px; border-radius:12px; border:1px solid #04d9ff;">
        <h3 style="color:#04d9ff;">📘 Fraud Glossary</h3>
        <p>Learn definitions of core fraud concepts.</p>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown("""
    <div style="background-color:#0e1117; padding:18px; border-radius:12px; border:1px solid #04d9ff;">
        <h3 style="color:#04d9ff;">🔍 Search Engine</h3>
        <p>Find the best article based on relevance.</p>
    </div>
    """, unsafe_allow_html=True)



# ------------------------------------------------------------
# SIMILARITY SCORE EXPLANATION
# ------------------------------------------------------------
st.markdown("""
<hr>
<h3 style="color:#04d9ff;">📈 What is a Similarity Score?</h3>

<div style="background-color:#0e1117; padding:15px; border-radius:10px; border:1px solid #04d9ff;">
<p style="font-size:16px;">
The similarity score shows how closely your search query matches an article 
based on its title, summary, and keywords. Scores range from:
</p>

<ul style="font-size:16px;">
<li><strong>0.80 – 1.00:</strong> Extremely strong match</li>
<li><strong>0.60 – 0.79:</strong> Strong match</li>
<li><strong>0.40 – 0.59:</strong> Moderate match</li>
<li><strong>0.00 – 0.39:</strong> Weak or unrelated</li>
</ul>

<p style="font-size:16px;">
Similarity is calculated using TF-IDF (Term Frequency–Inverse Document Frequency) 
and cosine similarity, a technique commonly used in information retrieval and NLP.
</p>
</div>
""", unsafe_allow_html=True)
