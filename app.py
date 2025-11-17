import streamlit as st
import pandas as pd
import numpy as np
import time
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="Fraud Intelli Search",
    page_icon="🔍",
    layout="wide"
)

# ------------------------------------------------------
# BRANDING HEADER
# ------------------------------------------------------
st.markdown("""
<div style="text-align:center; margin-bottom:20px;">
    <img src="https://i.imgur.com/kIzoyP2.png" width="180" style="border-radius:20px;"/>
</div>
<h1 style="text-align:center; color:#04d9ff; font-weight:900;">
🔍 Fraud Intelli Search Engine
</h1>
<p style="text-align:center; color:#cccccc; font-size:18px;">
Search, explore, and analyze FINRA fraud-related articles using AI-powered semantic matching.
</p>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")

    # Clean keywords into list format
    df["keyword_list"] = df["keywords"].fillna("").str.split(",")
    df["keyword_list"] = df["keyword_list"].apply(
        lambda lst: [k.strip() for k in lst if k.strip()]
    )

    # Convert timestamp → datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    
    return df

df = load_data()

# ------------------------------------------------------
# LOAD EMBEDDING MODEL
# ------------------------------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# Precompute article embeddings -------------------------------------------------
@st.cache_resource
def embed_articles(df):
    summaries = df["summary"].fillna("").tolist()
    return model.encode(summaries, convert_to_tensor=False)

article_embeddings = embed_articles(df)

# ------------------------------------------------------
# SEARCH BAR WITH SEMANTIC SUGGESTIONS
# ------------------------------------------------------
st.markdown("## 🔎 Search Articles")

col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "Enter your search query:",
        placeholder="e.g., investment fraud, AI scams, recovery fraud...",
    )

with col2:
    search_btn = st.button("Search", use_container_width=True)

# Generate search suggestions dynamically
def get_suggestions(text):
    if not text:
        return []
    pool = list({kw for lst in df["keyword_list"] for kw in lst})
    suggestions = [kw for kw in pool if text.lower() in kw.lower()]
    return suggestions[:8]

if query:
    suggestions = get_suggestions(query)
    if suggestions:
        st.markdown("### 🔮 Suggestions:")
        for s in suggestions:
            if st.button(s, key=f"sug_{s}"):
                query = s

st.markdown("---")


# ------------------------------------------------------
# RUN SEARCH
# ------------------------------------------------------
if search_btn and query:

    with st.spinner("🔎 Analyzing articles with AI… please wait..."):
        time.sleep(1)

        q_embedding = model.encode([query])[0]

        # Compute similarity
        sims = cosine_similarity([q_embedding], article_embeddings)[0]
        df["similarity"] = sims

        best = df.sort_values("similarity", ascending=False).iloc[0]

    # ------------------------------------------------------
    # DISPLAY TOP MATCHING RESULT
    # ------------------------------------------------------
    st.markdown("## 📄 Top Matching Article")

    # Format date safely
    if pd.notnull(best["timestamp"]):
        published_date = best["timestamp"].strftime("%B %d, %Y")
    else:
        published_date = "Unknown"

    st.markdown(f"""
    <div style="padding:20px; background:#111; border-radius:12px;">
        <h2 style="color:#04d9ff;">{best['title']}</h2>
        <p style="color:#ccc;">{best['summary']}</p>
        <p><b style="color:#04d9ff;">Published:</b> {published_date}</p>
        <p><b style="color:#04d9ff;">Keywords:</b> {best["keywords"]}</p>
        <a href="{best['url']}" target="_blank" 
           style="color:#00eaff; font-size:18px; font-weight:bold; text-decoration:none;">
           🔗 Read Full Article
        </a>
    </div>
    """, unsafe_allow_html=True)

    # ------------------------------------------------------
    # EXPORT RESULTS
    # ------------------------------------------------------
    st.markdown("---")
    st.markdown("### 📤 Export Search Results")

    export_df = df[["title", "url", "summary", "keywords", "timestamp", "similarity"]]
    csv_bytes = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Results as CSV",
        data=csv_bytes,
        file_name="fraud_intelli_search_results.csv",
        mime="text/csv",
    )

# ------------------------------------------------------
# FOOTER
# ------------------------------------------------------
st.markdown("""
<br><br>
<div style="text-align:center; color:#777; font-size:14px;">
Fraud Intelli © 2025 — Built with ❤️ by UNC Charlotte SDS Team  
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# DISPLAY TOP RELATED ARTICLES
# ------------------------------------------------------
st.markdown("## 📰 Related Articles")

# Get top 5 (excluding the already displayed best match)
top_k = 5
related_df = df.sort_values("similarity", ascending=False).iloc[1 : top_k + 1]

if related_df.empty:
    st.info("No related articles found.")
else:
    for _, row in related_df.iterrows():

        # Format date
        if pd.notnull(row["timestamp"]):
            pub_date = row["timestamp"].strftime("%B %d, %Y")
        else:
            pub_date = "Unknown"

        st.markdown(f"""
        <div style="padding:15px; background:#111; border-radius:12px; margin-bottom:15px;">
            <h3 style="color:#04d9ff;">{row['title']}</h3>
            <p style="color:#ccc;">{row['summary']}</p>
            <p><b style="color:#04d9ff;">Published:</b> {pub_date}</p>
            <p><b style="color:#04d9ff;">Keywords:</b> {row['keywords']}</p>
            <p><b style="color:#04d9ff;">Similarity:</b> {row['similarity']:.4f}</p>
            <a href="{row['url']}" target="_blank"
               style="color:#00eaff; font-size:16px; font-weight:bold; text-decoration:none;">
               🔗 Read Full Article
            </a>
        </div>
        """, unsafe_allow_html=True)

        </div>
        """, unsafe_allow_html=True)

