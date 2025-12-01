import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from intellifraud_ui import inject_light_ui, sidebar_logo

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="IntelliFraud Home", layout="wide")

# Inject global UI + sidebar logo
inject_light_ui()
sidebar_logo()

# ------------------------------------------------------------
# SEARCH HISTORY STATE
# ------------------------------------------------------------
if "search_history" not in st.session_state:
    st.session_state["search_history"] = []


# ------------------------------------------------------------
# HEADER / HERO SECTION (LIGHT MODE)
# ------------------------------------------------------------
st.markdown("""
<div style="
    padding: 30px; 
    background: #F5F7FA; 
    border-radius: 15px; 
    border: 1px solid #E6E9EF; 
    margin-bottom: 25px;
">
    <h1 style="margin-bottom: 0; color:#0A1A2F;">
        🔍 Welcome to IntelliFraud
    </h1>
    <p style="font-size: 1.1rem; margin-top: 8px; color:#0A1A2F;">
        Your interactive fraud intelligence dashboard for exploring regulatory actions,
        trends, article insights, and key fraud definitions — all in one place.
    </p>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# LOAD ARTICLE DATA
# ------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")

    df["keywords_clean"] = df["keywords"].fillna("").astype(str)

    df["search_text"] = (
        df["title"].fillna("") + " " +
        df["summary"].fillna("") + " " +
        df["keywords_clean"]
    ).str.lower()

    return df

df = load_data()


# ------------------------------------------------------------
# BUILD TF-IDF MODEL
# ------------------------------------------------------------
@st.cache_resource
def build_tfidf():
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(df["search_text"])
    return vectorizer, matrix

vectorizer, tfidf_matrix = build_tfidf()


# ------------------------------------------------------------
# BEST MATCH FUNCTION
# ------------------------------------------------------------
def best_article_match(query):
    query_vec = vectorizer.transform([query.lower()])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    best_idx = scores.argmax()
    best_score = scores[best_idx]

    return df.iloc[best_idx], float(best_score), scores


# ------------------------------------------------------------
# SEARCH BAR
# ------------------------------------------------------------
st.subheader("🔎 Search Across IntelliFraud")

query = st.text_input(
    "Ask a question or enter fraud-related keywords:",
    placeholder="Try: 'investment fraud', 'mail theft', 'AI scams', 'identity fraud'..."
)

if query:
    # ------- Top Match -------
    article, score, all_scores = best_article_match(query)

    # Save history
    st.session_state["search_history"].append({
        "query": query,
        "article_title": article["title"],
        "keywords": article["keywords"],
        "similarity_score": round(score, 4),
        "url": article["url"]
    })

    # ------- Display Top Match (LIGHT MODE CARD) -------
    st.markdown("""
        <h3 style='color:#0A65FF;'>Top Article Match</h3>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background-color:#FFFFFF;
        padding:18px; 
        margin-bottom:12px; 
        border-radius:12px; 
        border:1px solid #E6E9EF;
        box-shadow:0 1px 3px rgba(0,0,0,0.05);
    ">
        <h3 style="color:#0A1A2F;">{article['title']}</h3>
        <p>{article['summary']}</p>
        <p><strong>Keywords:</strong> {article['keywords']}</p>
        <p><strong>Similarity Score:</strong> {score:.2f}</p>
        <a href="{article['url']}" target="_blank" style="color:#0A65FF;">
            <strong>Read Full Article →</strong>
        </a>
    </div>
    """, unsafe_allow_html=True)

    
    # ------------------------------------------------------------
    # RELATED ARTICLES (Keyword-overlap filtered)
    # ------------------------------------------------------------
    st.markdown("<h3 style='color:#0A65FF; margin-top:35px;'>Related Articles</h3>", unsafe_allow_html=True)

    top_keywords = set(article["keywords"].lower().replace(",", "").split())
    top_indices = all_scores.argsort()[::-1][1:10]

    related_shown = 0

    for idx in top_indices:
        row = df.iloc[idx]
        score_val = all_scores[idx]

        # Compare keyword overlap
        other_keywords = set(row["keywords"].lower().replace(",", "").split())
        overlap = top_keywords.intersection(other_keywords)

        if len(overlap) < 2:
            continue

        if related_shown >= 3:
            break

        related_shown += 1

        st.markdown(f"""
        <div class="card">
            <h4 style="margin-bottom:4px;">{row['title']}</h4>
            <p style="font-size:15px;">{row['summary'][:220]}...</p>
            <p><strong>Shared Keywords:</strong> {', '.join(overlap)}</p>
            <p><strong>Similarity Score:</strong> {score_val:.2f}</p>
            <a href="{row['url']}" target="_blank" style="color:#0A65FF;">
                <strong>Read Article →</strong>
            </a>
        </div>
        """, unsafe_allow_html=True)

    if related_shown == 0:
        st.info("No sufficiently related articles found (must share ≥ 2 keywords).")


# ------------------------------------------------------------
# FEATURE CARDS (LIGHT MODE)
# ------------------------------------------------------------
st.subheader("📂 Navigate IntelliFraud")

col1, col2, col3, col4 = st.columns(4)

feature_cards = [
    ("🧭 Fraud Explorer", "Browse categorized fraud articles and topics."),
    ("📊 Fraud Trends", "Analyze keyword and fraud-type trends over time."),
    ("📘 Fraud Glossary", "Understand key fraud definitions and financial terms."),
    ("🔍 Article Search", "Find relevant articles using similarity scoring."),
]

for col, (title, desc) in zip([col1, col2, col3, col4], feature_cards):
    with col:
        st.markdown(f"""
        <div style="
            background-color:#FFFFFF; 
            padding:18px; 
            border-radius:12px; 
            border:1px solid #E6E9EF;
            box-shadow:0 1px 3px rgba(0,0,0,0.05);
        ">
            <h3 style="color:#0A65FF;">{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------
# SEARCH HISTORY
# ------------------------------------------------------------
st.subheader("📝 Your Search History")

if st.button("🗑️ Clear Search History"):
    st.session_state["search_history"] = []
    st.success("Search history cleared!")
    st.rerun()

history = st.session_state["search_history"]

if len(history) == 0:
    st.info("No searches yet. Try searching above!")
else:
    hist_df = pd.DataFrame(history)
    st.dataframe(hist_df, use_container_width=True)

    csv_data = hist_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Search History as CSV",
        data=csv_data,
        file_name="intellifraud_search_history.csv",
        mime="text/csv"
    )


# ------------------------------------------------------------
# SIMILARITY EXPLANATION (LIGHT MODE)
# ------------------------------------------------------------
st.markdown("""
<hr>
<h3 style="color:#0A65FF;">📈 Understanding Similarity Scores</h3>

<div style="
    background-color:#FFFFFF; 
    padding:15px; 
    border-radius:10px; 
    border:1px solid #E6E9EF;
    box-shadow:0 1px 3px rgba(0,0,0,0.05);
">
<p style="font-size:16px; color:#0A1A2F;">
Similarity scores measure how closely your query matches articles using TF-IDF and cosine similarity.
Higher scores indicate stronger relevance.
</p>

<ul style="font-size:16px; color:#0A1A2F;">
<li><strong>0.80 – 1.00:</strong> Extremely strong match</li>
<li><strong>0.60 – 0.79:</strong> Strong match</li>
<li><strong>0.40 – 0.59:</strong> Moderate match</li>
<li><strong>0.00 – 0.39:</strong> Weak or unrelated</li>
</ul>
</div>
""", unsafe_allow_html=True)
