import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit import rerun
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
# GLOBAL STYLE FIXES
# ---------------------------------------------------------
st.markdown("""
<style>

.stTextInput > div > div {
    background-color: #F3F4F6 !important;
    border-radius: 10px !important;
    border: 1px solid #D1D5DB !important;
}

.stTextInput input::placeholder {
    color: #000 !important;
    opacity: 1 !important;
}

.stTextInput input {
    color: #0A1A2F !important;
    font-size: 15px !important;
}

div.stButton > button,
div.stDownloadButton > button {
    background-color: #F4F5F7 !important;
    color: #0A1A2F !important;
    border: 1px solid #D0D7E2 !important;
    padding: 10px 22px !important;
    border-radius: 10px !important;
    font-size: 15px !important;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background-color: #E6EAF0 !important;
    border-color: #0A65FF !important;
    color: #0A65FF !important;
}

ul li {
    color: #0A1A2F !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOGO
# ---------------------------------------------------------
st.markdown("""
<div style="text-align:center; margin-bottom: 25px;">
    <img src="https://i.imgur.com/lAVJ7Vx.png" width="240" style="border-radius:15px;">
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD FRAUD DATA & MODEL
# ---------------------------------------------------------
df = load_fraud_data()
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------------------------------------------------
# SEARCH HISTORY (SESSION)
# ---------------------------------------------------------
if "search_history" not in st.session_state:
    st.session_state["search_history"] = []

# ---------------------------------------------------------
# SEARCH BAR
# ---------------------------------------------------------
query = st.text_input(
    "🔍 Search IntelliFraud Database",
    placeholder="Search for fraud topics, keywords, or summaries...",
    key="home_search"
)

# ---------------------------------------------------------
# SEARCH FUNCTION
# ---------------------------------------------------------
def search_articles(query):
    if not query or query.strip() == "":
        return None, None

    query_emb = model.encode([query])
    doc_emb = model.encode(df["summary"].tolist())

    sims = cosine_similarity(query_emb, doc_emb)[0]
    df["similarity"] = sims

    top_row = df.sort_values("similarity", ascending=False).iloc[0]
    return top_row, df.sort_values("similarity", ascending=False).head(5)

# ---------------------------------------------------------
# PROCESS SEARCH + SAVE HISTORY
# ---------------------------------------------------------
if query and query.strip() != "":
    top_result, top5 = search_articles(query)

    if top_result is not None:

        # ⭐ SAVE SEARCH HISTORY ⭐
        history_entry = {
            "query": query,
            "top_title": top_result["title"],
            "similarity": float(top_result["similarity"]),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        st.session_state["search_history"].append(history_entry)

        # ⭐ FORCE PAGE TO RERUN SO HISTORY DISPLAYS ⭐
        rerun()

# ---------------------------------------------------------
# NAVIGATION BUTTONS
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

history_df = pd.DataFrame(st.session_state["search_history"])

if len(history_df) > 0:
    csv_data = history_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Search History as CSV",
        data=csv_data,
        file_name="intellifraud_search_history.csv",
        mime="text/csv",
        key="download_history"
    )
else:
    st.info("No search history yet.")

if st.button("❌ Clear Search History"):
    st.session_state["search_history"] = []
    rerun()

# ---------------------------------------------------------
# SIMILARITY EXPLANATION
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
### ❓ How Similarity Scores Work
Similarity scores measure semantic closeness between your query and each article.

- **0.85 – 1.00** → Extremely relevant  
- **0.70 – 0.85** → Strong relevance  
- **0.50 – 0.70** → Moderate match  
- **Below 0.50** → Weak match  

Powered by transformer embeddings (MiniLM).
""")
