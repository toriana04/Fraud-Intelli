import streamlit as st
import pandas as pd
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from load_data_supabase import load_fraud_data
from intellifraud_ui import inject_light_ui

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Home | IntelliFraud", layout="wide")
inject_light_ui()

# ---------------------------------------------------------
# GLOBAL STYLE FIXES (SEARCH BAR + BUTTONS)
# ---------------------------------------------------------
st.markdown("""
<style>

/* LIGHTER GRAY SEARCH BAR INPUT */
div[data-baseweb="input"] {
    background-color: #F9FAFB !important;
    border-radius: 10px !important;
}

/* BLACK PLACEHOLDER TEXT */
input::placeholder {
    color: #000000 !important;
    opacity: 1 !important;
}

/* Actual text color inside input */
input {
    color: #0A1A2F !important;
}

/* FIX BLACK normal BUTTONS */
div.stButton > button {
    background-color: #F4F5F7 !important;
    color: #0A1A2F !important;
    border: 1px solid #D0D7E2 !important;
    padding: 10px 22px !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    transition: all 0.2s ease-in-out;
}
div.stButton > button:hover {
    background-color: #E6EAF0 !important;
    border-color: #0A65FF !important;
    color: #0A65FF !important;
}

/* FIX BLACK DOWNLOAD BUTTON */
div.stDownloadButton > button {
    background-color: #F4F5F7 !important;
    color: #0A1A2F !important;
    border: 1px solid #D0D7E2 !important;
    padding: 10px 18px !important;
    border-radius: 10px !important;
    font-size: 15px !important;
}
div.stDownloadButton > button:hover {
    background-color: #E6EAF0 !important;
    border-color: #0A65FF !important;
    color: #0A65FF !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# LOGO AT TOP
# ---------------------------------------------------------
st.markdown("""
<div style="text-align:center; margin-bottom: 25px;">
    <img src="https://i.imgur.com/lAVJ7Vx.png" width="240" style="border-radius:15px;">
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# LOAD DATA + MODEL
# ---------------------------------------------------------
df = load_fraud_data()
model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------------------------------------------------
# SEARCH HISTORY STATE
# ---------------------------------------------------------
if "search_history" not in st.session_state:
    st.session_state["search_history"] = []


# ---------------------------------------------------------
# SEARCH BAR
# ---------------------------------------------------------
query = st.text_input(
    "🔍 Search IntelliFraud Database",
    placeholder="Search for fraud topics, schemes, keywords, or article summaries...",
)


# ---------------------------------------------------------
# SEARCH FUNCTION
# ---------------------------------------------------------
def search_articles(query):
    if not query:
        return None, None

    query_embedding = model.encode([query])
    doc_embeddings = model.encode(df["summary"].tolist())

    sims = cosine_similarity(query_embedding, doc_embeddings)[0]
    df["similarity"] = sims

    top_row = df.sort_values("similarity", ascending=False).iloc[0]

    # Save only the top article to search history
    st.session_state["search_history"].append({
        "query": query,
        "top_title": top_row["title"],
        "similarity": float(top_row["similarity"]),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return top_row, df.sort_values("similarity", ascending=False).head(5)


# ---------------------------------------------------------
# SHOW SEARCH RESULTS
# ---------------------------------------------------------
if query:
    top_result, top5 = search_articles(query)

    if top_result is not None:
        st.markdown("---")
        st.subheader("⭐ Top Matching Article")

        st.markdown(f"""
        <div style="
            padding:20px;
            border:1px solid #E6E9EF;
            background:#FFFFFF;
            border-radius:12px;
            box-shadow:0 1px 4px rgba(0,0,0,0.05);
        ">
            <h3 style="color:#0A65FF; margin-bottom:10px;">{top_result['title']}</h3>
            <p style="font-size:15px; color:#0A1A2F;">{top_result['summary']}</p>
            <p style="font-size:14px; margin-top:8px;"><strong>Similarity Score:</strong> {top_result['similarity']:.3f}</p>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# NAVIGATION SECTION
# ---------------------------------------------------------
st.markdown("## 🌐 Navigate IntelliFraud")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Fraud Trends"):
        st.switch_page("pages/2_Fraud Trends.py")

with col2:
    if st.button("🔍 Search Engine"):
        st.switch_page("pages/1_Search.py")

with col3:
    if st.button("📚 Keyword Explorer"):
        st.switch_page("pages/3_Keyword Explorer.py")


# ---------------------------------------------------------
# DOWNLOAD & CLEAR SEARCH HISTORY
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📥 Download Your Search History")

if len(st.session_state["search_history"]) > 0:
    hist_df = pd.DataFrame(st.session_state["search_history"])
    csv = hist_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Search History as CSV",
        data=csv,
        file_name="intellifraud_search_history.csv",
        mime="text/csv"
    )
else:
    st.info("No search history yet.")


# CLEAR HISTORY BUTTON
st.markdown("### 🧹 Manage Search History")

if st.button("❌ Clear Search History"):
    st.session_state["search_history"] = []
    st.success("Search history cleared.")


# ---------------------------------------------------------
# SIMILARITY SCORE EXPLANATION
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
### ❓ How Similarity Scores Work
Similarity scores measure how closely your search matches each article using semantic embeddings.

- **0.85 – 1.00 → Extremely relevant**  
- **0.70 – 0.85 → Strongly relevant**  
- **0.50 – 0.70 → Moderately relevant**  
- **Below 0.50 → Weak match**

IntelliFraud uses a transformer model (MiniLM) to compute similarity between your search and article summaries.
""")
