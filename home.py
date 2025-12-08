import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

from intellifraud_ui import inject_light_ui
from load_data_supabase import load_fraud_data

st.set_page_config(page_title="IntelliFraud Home", layout="wide")
inject_light_ui()

# -------------------------------------------------
# CSS FIXES (search bar, buttons, card layout)
# -------------------------------------------------
st.markdown("""
<style>

.stTextInput > div > div {
    background-color: #F3F4F6 !important;
    border-radius: 10px !important;
    border: 1px solid #D1D5DB !important;
    padding: 6px;
}

.stTextInput input::placeholder {
    color: #000 !important;
}

.stTextInput input {
    color: #0A1A2F !important;
    font-size: 15px !important;
}

/* Prevent black Streamlit buttons */
div.stButton > button,
div.stDownloadButton > button {
    background-color: #F4F5F7 !important;
    color: #0A1A2F !important;
    border: 1px solid #D0D7E2 !important;
    padding: 8px 20px !important;
    border-radius: 8px !important;
    font-size: 15px !important;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background-color: #E6EAF0 !important;
    border-color: #0A65FF !important;
    color: #0A65FF !important;
}

/* Card styling */
.card {
    padding: 20px;
    background: white;
    border: 1px solid #E6E9EF;
    border-radius: 12px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TOP LOGO
# -------------------------------------------------
st.markdown("""
<div style="text-align:center; margin-bottom:25px;">
    <img src="https://i.imgur.com/lAVJ7Vx.png" width="240" style="border-radius:15px;">
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SEARCH HISTORY (session state)
# -------------------------------------------------
if "search_history" not in st.session_state:
    st.session_state["search_history"] = []

# -------------------------------------------------
# HEADER SECTION
# -------------------------------------------------
st.markdown("""
<div class="card" style="padding:25px; margin-bottom:20px;">
    <h1 style="margin-bottom: 5px;">🔍 Welcome to IntelliFraud</h1>
    <p style="font-size:17px;">
        Explore fraud trends, regulatory actions, keyword signals, and investigative insights —
        all in one intelligent dashboard.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA FROM SUPABASE
# -------------------------------------------------
@st.cache_data
def load_articles():
    df = load_fraud_data()

    df.columns = [c.lower() for c in df.columns]

    for col in ["title", "summary", "keywords", "url"]:
        if col not in df.columns:
            df[col] = ""

    # convert keywords list → string
    def format_keywords(x):
        if isinstance(x, list):
            return ", ".join(x)
        return str(x)

    df["keywords"] = df["keywords"].apply(format_keywords)

    df["title"] = df["title"].fillna("Untitled Article")
    df["summary"] = df["summary"].fillna("")

    df["search_text"] = (
        df["title"] + " " + df["summary"] + " " + df["keywords"]
    ).str.lower()

    return df

df = load_articles()

# -------------------------------------------------
# BUILD TF-IDF MODEL
# -------------------------------------------------
@st.cache_resource
def build_tfidf(df):
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(df["search_text"])
    return vectorizer, matrix

vectorizer, tfidf_matrix = build_tfidf(df)

# -------------------------------------------------
# ARTICLE MATCHING
# -------------------------------------------------
def best_article_match(query):
    if df.empty:
        return None, 0.0, []

    query_vec = vectorizer.transform([query.lower()])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    idx = scores.argmax()
    if idx >= len(df):
        return None, 0.0, scores

    return df.iloc[idx], float(scores[idx]), scores

# -------------------------------------------------
# SEARCH BAR
# -------------------------------------------------
st.subheader("🔎 Search Across IntelliFraud")

query = st.text_input(
    "Ask a question or enter fraud-related keywords:",
    placeholder="Try: 'mail theft', 'investment fraud', 'AI trading', 'identity theft'..."
)

# -------------------------------------------------
# SEARCH PROCESSING
# -------------------------------------------------
if query:
    article, score, score_list = best_article_match(query)

    if article is None:
        st.error("⚠️ No matching results found.")
    else:

        # Save to session search history
        st.session_state["search_history"].append({
            "query": query,
            "article_title": article["title"],
            "similarity_score": round(score, 4),
            "keywords": article["keywords"],
            "url": article["url"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # MAIN MATCH CARD
        st.markdown(f"""
        <div class="card">
            <h3>{article['title']}</h3>
            <p>{article['summary']}</p>
            <p><strong>Keywords:</strong> {article['keywords']}</p>
            <p><strong>Similarity Score:</strong> {score:.2f}</p>
            <a href="{article['url']}" target="_blank"><strong>Read Full Article →</strong></a>
        </div>
        """, unsafe_allow_html=True)

        # RELATED ARTICLES
        st.subheader("📌 Related Articles")

        base_kw = set(article["keywords"].lower().replace(",", "").split())
        ranked = score_list.argsort()[::-1][1:25]

        shown = 0
        for idx in ranked:
            row = df.iloc[idx]
            overlap = base_kw & set(row["keywords"].lower().replace(",", "").split())

            if len(overlap) >= 2:
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


# -------------------------------------------------
# SEARCH HISTORY
# -------------------------------------------------
st.subheader("📝 Your Search History")

if st.button("Clear Search History"):
    st.session_state["search_history"] = []
    st.rerun()

if st.session_state["search_history"]:
    hist_df = pd.DataFrame(st.session_state["search_history"])
    st.dataframe(hist_df, use_container_width=True)

    # CSV DOWNLOAD BUTTON
    csv_data = hist_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Search History CSV",
        data=csv_data,
        file_name="intellifraud_search_history.csv",
        mime="text/csv"
    )
else:
    st.info("No searches yet.")

# -------------------------------------------------
# SIMILARITY SCORE EXPLANATION (HTML FIXED)
# -------------------------------------------------
st.markdown("""
<div class="card">
    <h3 style="margin-top:0;">📈 Understanding Similarity Scores</h3>
    <p>Similarity scores measure how closely your query aligns with article text using TF-IDF + cosine similarity.</p>

    <div style="color:#0A1A2F; font-size:15px;">
        <ul>
            <li><strong>0.80 – 1.00:</strong> Extremely strong match</li>
            <li><strong>0.60 – 0.79:</strong> Strong match</li>
            <li><strong>0.40 – 0.59:</strong> Moderate match</li>
            <li><strong>0.00 – 0.39:</strong> Weak match</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)
