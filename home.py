import streamlit as st
import pandas as pd
import os
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
# GLOBAL STYLE FIXES
# ---------------------------------------------------------
st.markdown("""
<style>

/* Light gray search bar */
.stTextInput > div > div {
    background-color: #F3F4F6 !important;
    border-radius: 10px !important;
    border: 1px solid #D1D5DB !important;
}

/* Placeholder text black */
.stTextInput input::placeholder {
    color: #000000 !important;
    opacity: 1 !important;
}

/* Actual text */
.stTextInput input {
    color: #0A1A2F !important;
    font-size: 15px !important;
}

/* Buttons */
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

/* Bullet list visibility */
ul li {
    color: #0A1A2F !important;
    font-size: 15px !important;
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
# ROOT-BASED SEARCH HISTORY SYSTEM
# ---------------------------------------------------------
HISTORY_FILE = "search_history.csv"

def load_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)
    return pd.DataFrame(columns=["query", "top_title", "similarity", "timestamp"])

def save_history(entry):
    history_df = load_history()
    history_df = pd.concat([history_df, pd.DataFrame([entry])], ignore_index=True)
    history_df.to_csv(HISTORY_FILE, index=False)

# ---------------------------------------------------------
# SEARCH BAR
# ---------------------------------------------------------
query = st.text_input(
    "🔍 Search IntelliFraud Database",
    placeholder="Search for fraud topics, schemes, keywords, or summaries...",
    key="search_input"
)

# ---------------------------------------------------------
# SEARCH FUNCTION
# ---------------------------------------------------------
def search_articles(query):
    if query is None or query.strip() == "":
        return None, None

    query_embedding = model.encode([query])
    doc_embeddings = model.encode(df["summary"].tolist())

    sims = cosine_similarity(query_embedding, doc_embeddings)[0]
    df["similarity"] = sims

    top_row = df.sort_values("similarity", ascending=False).iloc[0]

    # Create new entry
    entry = {
        "query": query,
        "top_title": top_row["title"],
        "similarity": float(top_row["similarity"]),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    save_history(entry)

    return top_row, df.sort_values("similarity", ascending=False).head(5)

# ---------------------------------------------------------
# SHOW SEARCH RESULTS
# ---------------------------------------------------------
if query and query.strip() != "":
    top_result, top5 = search_articles(query)

    if top_result is not None:
        st.markdown("---")
        st.subheader("⭐ Top Matching Article")

        st.markdown(f"""
        <div style="
            padding:20px;
            border:1px solid #E6E9EF;
            background:white;
            border-radius:12px;
            box-shadow:0 1px 4px rgba(0,0,0,0.05);
        ">
            <h3 style="color:#0A65FF;">{top_result['title']}</h3>
            <p style="color:#0A1A2F; font-size:15px;">{top_result['summary']}</p>
            <p><strong>Similarity:</strong> {top_result['similarity']:.3f}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# NAVIGATION
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
# DOWNLOAD + CLEAR HISTORY
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📥 Download Your Search History")

history_df = load_history()

if len(history_df) > 0:
    csv = history_df.to_csv(index=False).encode("utf-8")
    
    st.download_button(
        label="⬇️ Download Search History as CSV",
        data=csv,
        file_name="search_history.csv",
        mime="text/csv",
        key="download_btn"
    )
else:
    st.info("No search history yet.")

if st.button("❌ Clear Search History"):
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    st.success("Search history cleared.")

# ---------------------------------------------------------
# SIMILARITY EXPLANATION
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
### ❓ How Similarity Scores Work
Similarity scores measure your search text against article summaries using embeddings.

- **0.85 – 1.00 → Extremely relevant**  
- **0.70 – 0.85 → Strongly relevant**  
- **0.50 – 0.70 → Moderately relevant**  
- **Below 0.50 → Weak match**
""")
