import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="HOME", layout="wide")


# ------------------------------------------------------------
# SEARCH HISTORY STATE
# ------------------------------------------------------------
if "search_history" not in st.session_state:
    st.session_state["search_history"] = []


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
Your interactive fraud intelligence dashboard for exploring regulatory actions, 
fraud trends, article insights, and key definitions — all in one place.
</p>
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

    return df.iloc[best_idx], float(best_score)


# ------------------------------------------------------------
# SEARCH BAR (MATCH ARTICLES ONLY)
# ------------------------------------------------------------
st.subheader("🔎 Search Across IntelliFraud")

query = st.text_input(
    "Ask a question or enter fraud-related keywords:",
    placeholder="Try: 'AI fraud', 'investment scams', 'mail theft', 'older adults fraud'..."
)

if query:
    article, score = best_article_match(query)

    # Save search entry to history (INCLUDING KEYWORDS)
    st.session_state["search_history"].append({
        "query": query,
        "article_title": article["title"],
        "keywords": article["keywords"],
        "similarity_score": round(score, 4),
        "url": article["url"]
    })

    st.markdown("<h3 style='color:#04d9ff;'>Top Article Match</h3>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background-color:#0e1117; 
        padding:18px; 
        margin-bottom:12px; 
        border-radius:12px; 
        border:1px solid #04d9ff;
    ">
        <h3 style="color:#04d9ff;">{article['title']}</h3>
        <p>{article['summary']}</p>
        <p><strong>Keywords:</strong> {article['keywords']}</p>
        <p><strong>Similarity Score:</strong> {score:.2f}</p>
        <a href="{article['url']}" target="_blank" style="color:#04d9ff;"><strong>Read Article</strong></a>
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
        <p>View keyword patterns and activity over time.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background-color:#0e1117; padding:18px; border-radius:12px; border:1px solid #04d9ff;">
        <h3 style="color:#04d9ff;">📘 Fraud Glossary</h3>
        <p>Understand key fraud definitions and terms.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="background-color:#0e1117; padding:18px; border-radius:12px; border:1px solid #04d9ff;">
        <h3 style="color:#04d9ff;">🔍 Article Search</h3>
        <p>Find the most relevant article using similarity scoring.</p>
    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------
# SEARCH HISTORY SECTION
# ------------------------------------------------------------
st.subheader("📝 Your Search History")

# Clear history button
if st.button("🗑️ Clear Search History"):
    st.session_state["search_history"] = []
    st.success("Search history cleared!")
    st.experimental_rerun()

history = st.session_state["search_history"]

if len(history) == 0:
    st.info("No searches yet. Try searching for something above!")
else:
    hist_df = pd.DataFrame(history)

    st.dataframe(hist_df, use_container_width=True)

    # Create CSV for download
    csv_data = hist_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Search History as CSV",
        data=csv_data,
        file_name="intellifraud_search_history.csv",
        mime="text/csv"
    )


# ------------------------------------------------------------
# SIMILARITY SCORE EXPLANATION
# ------------------------------------------------------------
st.markdown("""
<hr>
<h3 style="color:#04d9ff;">📈 What is a Similarity Score?</h3>

<div style="background-color:#0e1117; padding:15px; border-radius:10px; border:1px solid #04d9ff;">
<p style="font-size:16px;">
A similarity score shows how closely your search query matches an article  
based on its title, summary, and keywords. Scores range from:
</p>

<ul style="font-size:16px;">
<li><strong>0.80 – 1.00:</strong> Extremely strong match</li>
<li><strong>0.60 – 0.79:</strong> Strong match</li>
<li><strong>0.40 – 0.59:</strong> Moderate match</li>
<li><strong>0.00 – 0.39:</strong> Weak or unrelated</li>
</ul>

<p style="font-size:16px;">
The scoring is calculated using TF-IDF and cosine similarity —  
the same method used in many modern search engines.
</p>
</div>
""", unsafe_allow_html=True)
