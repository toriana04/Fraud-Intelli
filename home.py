import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from intellifraud_ui import inject_light_ui, sidebar_logo

# NEW — load dataset from Supabase instead of local CSV
from load_data_supabase import load_fraud_data

# ----------------------------------------------
# PAGE CONFIG & UI
# ----------------------------------------------
st.set_page_config(page_title="IntelliFraud Home", layout="wide")

inject_light_ui()
sidebar_logo()

# ----------------------------------------------
# Search history (Streamlit session state)
# ----------------------------------------------
if "search_history" not in st.session_state:
    st.session_state["search_history"] = []

# ----------------------------------------------
# Header block
# ----------------------------------------------
st.markdown("""
<div class="card" style="padding:25px; margin-bottom:20px;">
    <h1 style="margin-bottom: 5px;">🔍 Welcome to IntelliFraud</h1>
    <p style="font-size:17px;">
        Explore fraud trends, regulatory actions, keyword signals, and investigative insights —
        all in one intelligent dashboard.
    </p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------
# Load Data from Supabase
# ----------------------------------------------
@st.cache_data
def load_data():
    df = load_fraud_data()

    # Convert keyword lists to clean strings for TF-IDF
    df["keywords_clean"] = df["keywords"].astype(str)

    df["search_text"] = (
        df["title"].fillna("") + " " +
        df["summary"].fillna("") + " " +
        df["keywords_clean"]
    ).str.lower()

    return df

df = load_data()

# ----------------------------------------------
# TF-IDF model
# ----------------------------------------------
@st.cache_resource
def build_tfidf():
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(df["search_text"])
    return vectorizer, matrix

vectorizer, tfidf_matrix = build_tfidf()

# ----------------------------------------------
# Best-match function
# ----------------------------------------------
def best_article_match(query):
    query_vec = vectorizer.transform([query.lower()])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    idx = scores.argmax()
    return df.iloc[idx], float(scores[idx]), scores

# ----------------------------------------------
# Search Bar
# ----------------------------------------------
st.subheader("🔎 Search Across IntelliFraud")

query = st.text_input(
    "Ask a question or enter fraud-related keywords:",
    placeholder="Try: 'mail theft', 'investment fraud', 'AI trading', 'identity theft'..."
)

if query:
    # compute match
    article, score, score_list = best_article_match(query)

    # save to history
    st.session_state["search_history"].append({
        "query": query,
        "article_title": article["title"],
        "keywords": article["keywords"],
        "similarity_score": round(score, 4),
        "url": article["url"],
    })

    # show main result
    st.markdown(f"""
    <div class="card">
        <h3>{article['title']}</h3>
        <p>{article['summary']}</p>
        <p><strong>Keywords:</strong> {article['keywords']}</p>
        <p><strong>Similarity Score:</strong> {score:.2f}</p>
        <a href="{article['url']}" target="_blank"><strong>Read Full Article →</strong></a>
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------
    # Related articles
    # ----------------------------------------------
    st.subheader("📌 Related Articles")

    # convert to sets for overlap calculations
    top_keywords = set(article["keywords"])
    ranked = score_list.argsort()[::-1][1:15]

    shown = 0
    for idx in ranked:
        row = df.iloc[idx]
        overlap = top_keywords & set(row["keywords"])

        if len(overlap) >= 2:  # must share at least 2 keywords
            shown += 1
            if shown > 3:
                break

            st.markdown(f"""
            <div class="card">
                <h4>{row['title']}</h4>
                <p>{row['summary'][:220]}...</p>
                <p><strong>Shared Keywords:</strong> {', '.join(overlap)}</p>
                <p><strong>Similarity Score:</strong> {score_list[idx]:.2f}</p>
                <a href="{row['url']}" target="_blank"><strong>Read Article →</strong></a>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------
# Feature Navigation Cards
# ----------------------------------------------
st.subheader("📂 Navigate IntelliFraud")

features = [
    ("🧭 Fraud Explorer", "Browse categorized fraud insights."),
    ("📊 Fraud Trends", "Analyze keyword and temporal patterns."),
    ("📘 Glossary", "Understand fraud terminology."),
    ("🔍 Article Search", "Find similar articles using AI."),
]

c1, c2, c3, c4 = st.columns(4)
for col, item in zip([c1, c2, c3, c4], features):
    with col:
        st.markdown(f"""
        <div class="card">
            <h3>{item[0]}</h3>
            <p>{item[1]}</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------
# Search History Section
# ----------------------------------------------
st.subheader("📝 Your Search History")

if st.button("Clear Search History"):
    st.session_state["search_history"] = []
    st.rerun()

if not st.session_state["search_history"]:
    st.info("No searches yet.")
else:
    hist_df = pd.DataFrame(st.session_state["search_history"])
    st.dataframe(hist_df, use_container_width=True)
