# =====================================================================
#  FRAUD INTELLI APP — AI FRAUD ANALYSIS DASHBOARD
#  Author: Clara Belluci, Troy Benner, Hoang Bui, Tori-Ana McNeil
#  Partners: UNCC School of Data Science x USAA
# =====================================================================

import streamlit as st
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from keybert import KeyBERT
from bs4 import BeautifulSoup
import requests
import time

# =====================================================================
#  PAGE CONFIGURATION
# =====================================================================
st.set_page_config(page_title="Fraud Intelli Search", page_icon="🤖", layout="wide")

# =====================================================================
#  BRAND THEME CSS (FULL DARK MODE)
# =====================================================================
st.markdown("""
<style>

.main, .reportview-container {
    background-color: #0A0F24 !important;
    color: #FFFFFF !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #11172B !important;
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] * {
    color: #D6E2FF !important;
}

/* Headers */
h1, h2, h3, h4 {
    color: #00F2FF !important;
    font-weight: 800 !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #8A2BE2, #00F2FF);
    color: white !important;
    border-radius: 8px;
    border: none;
    padding: 0.6rem 1.3rem;
    font-weight: 700;
    font-size: 16px;
}
.stButton>button:hover {
    opacity: 0.85;
    transform: scale(1.02);
    transition: 0.2s ease;
}

/* Inputs */
.stTextInput>div>div>input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #121A2E;
    color: white !important;
    border: 1px solid #8A2BE2 !important;
    border-radius: 6px;
}

/* Dataframes */
.stDataFrame, .dataframe {
    background-color: #11172B !important;
    color: white !important;
}

/* Alerts */
.stAlert {
    background-color: rgba(138, 43, 226, 0.15) !important;
    border-left: 4px solid #8A2BE2 !important;
    color: #E6D9FF !important;
}

/* Scrollbars */
::-webkit-scrollbar { width: 7px; }
::-webkit-scrollbar-thumb {
    background: #8A2BE2;
    border-radius: 4px;
}

/* Fraud Intelli Cards */
.fraud-card {
    background-color: #11172B;
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid #00F2FF;
    margin-bottom: 15px;
    color: white;
}

/* DIVIDER */
hr {
    border: 1px solid rgba(255,255,255,0.05);
}

</style>
""", unsafe_allow_html=True)

# =====================================================================
#  ANIMATED SPINNER CSS + FUNCTION (OPTION C PREMIUM)
# =====================================================================
st.markdown("""
<style>

@keyframes spinpulse {
  0% {
    transform: rotate(0deg) scale(1);
    filter: drop-shadow(0 0 0 #00F2FF);
  }
  50% {
    transform: rotate(180deg) scale(1.05);
    filter: drop-shadow(0 0 12px #00F2FF);
  }
  100% {
    transform: rotate(360deg) scale(1);
    filter: drop-shadow(0 0 0 #00F2FF);
  }
}

.spinner-premium {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 40px;
}

.spinner-logo-premium {
    width: 150px;
    animation: spinpulse 2.5s infinite ease-in-out;
}

</style>
""", unsafe_allow_html=True)

def fraud_intelli_spinner(message="Fraud Intelli is analyzing..."):
    st.markdown(
        f"<h4 style='text-align:center; color:#8A2BE2;'>{message}</h4>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class="spinner-premium">
        <img src="https://i.imgur.com/kIzoyP2.png" class="spinner-logo-premium">
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
#  LOGO + TITLE
# =====================================================================
fraud_intelli_spinner("Launching Fraud Intelli...")

st.image("https://i.imgur.com/kIzoyP2.png", width=160)
st.markdown("<h1 style='text-align:center;'>Fraud Intelli Search Engine</h1>", unsafe_allow_html=True)
st.caption("AI-Powered Fraud Intelligence Dashboard")

# =====================================================================
#  LOAD MODELS (WITH SPINNER)
# =====================================================================
with st.spinner(""):
    fraud_intelli_spinner("Loading AI Models...")
    @st.cache_resource
    def load_models():
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        explain_model = pipeline("text2text-generation", model="google/flan-t5-small")
        keyword_model = KeyBERT()
        return embed_model, explain_model, keyword_model
    embed_model, explain_model, keyword_model = load_models()

# =====================================================================
#  LOAD CSV DATA
# =====================================================================
@st.cache_data
def load_data():
    return pd.read_csv("fraud_analysis_final.csv")

df = load_data()
df["summary"] = df["summary"].fillna("")
df["keywords"] = df["keywords"].fillna("")

# Embed summaries
with st.spinner(""):
    fraud_intelli_spinner("Embedding Articles...")
    @st.cache_resource
    def embed_summaries():
        return embed_model.encode(df["summary"].tolist(), convert_to_tensor=True)
    summary_embeddings = embed_summaries()

# =====================================================================
#  SEMANTIC SUGGESTIONS ENGINE
# =====================================================================
@st.cache_data
def generate_semantic_suggestions(query, top_n=5):
    all_phrases = sorted(set(df["title"].tolist() + df["keywords"].tolist()))
    corpus_embeddings = embed_model.encode(all_phrases, convert_to_tensor=True)
    q_emb = embed_model.encode(query, convert_to_tensor=True)
    cos_scores = util.cos_sim(q_emb, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=min(top_n, len(all_phrases)))
    return [all_phrases[i] for i in top_results.indices]

# =====================================================================
#  SMART SEMANTIC SEARCH BAR
# =====================================================================
st.markdown("### 🔍 Smart Semantic Search")

if "search_text" not in st.session_state:
    st.session_state.search_text = ""

def update_query():
    st.session_state.search_text = st.session_state.temp_query

st.text_input(
    "Search for fraud topics, keywords, or article titles:",
    key="temp_query",
    on_change=update_query,
    placeholder="e.g., AI Fraud, Check Scam, Account Takeover…"
)

query = st.session_state.search_text.strip()

# --- Suggestions ---
if query:
    with st.spinner(""):
        fraud_intelli_spinner("Finding Related Topics...")
        suggestions = generate_semantic_suggestions(query)

    if suggestions:
        st.markdown("#### 💡 Related Topics:")
        for s in suggestions:
            if st.button(f"🔎 {s}"):
                st.session_state.search_text = s
                st.experimental_rerun()
    st.markdown("<hr>", unsafe_allow_html=True)

# =====================================================================
#  SEMANTIC SEARCH RESULTS (WITH SPINNER)
# =====================================================================
if query:
    with st.spinner(""):
        fraud_intelli_spinner("Searching Knowledge Base...")
        q_emb = embed_model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(q_emb, summary_embeddings)[0]
        top_idx = torch.argmax(cos_scores).item()
        best = df.iloc[top_idx]

    st.markdown("### 📄 Top Matching Article")
    st.markdown(f"**{best['title']}**  \nPublished: `{best['date']}`")
    st.markdown(best["summary"])
    st.markdown(f"**Keywords:** {best['keywords']}")
    st.markdown(f"[🔗 View Full Article]({best['url']})")

    # ---- AI Insight ----
    with st.spinner(""):
        fraud_intelli_spinner("Generating AI Insight...")
        prompt = (
            f"Summarize this article in 3 sentences explaining type, risk, and relevance:\n\n{best['summary']}"
        )
        ai_explanation = explain_model(prompt, max_length=200)[0]["generated_text"]

    st.success(f"**AI Insight:** {ai_explanation}")
    st.markdown("<hr>", unsafe_allow_html=True)

# =====================================================================
#  AI Q&A SECTION
# =====================================================================
st.markdown("### 💬 Ask Anything About Fraud")

user_question = st.text_input("Enter your question:")

if user_question:
    with st.spinner(""):
        fraud_intelli_spinner("Analyzing Question...")
        q_emb = embed_model.encode(user_question, convert_to_tensor=True)
        sims = util.cos_sim(q_emb, summary_embeddings)[0]
        top_idx = torch.argmax(sims).item()
        context = df.iloc[top_idx]["summary"]

        prompt = (
            f"Based on this fraud context:\n{context}\n\n"
            f"Answer the following question clearly:\n{user_question}"
        )
        answer = explain_model(prompt, max_length=250)[0]["generated_text"]

    st.success(answer)

# =====================================================================
#  COMPARE MODE
# =====================================================================
st.markdown("### ⚖️ Compare Two Articles")

col1, col2 = st.columns(2)
with col1:
    article1 = st.selectbox("First article", df["title"].tolist())
with col2:
    article2 = st.selectbox("Second article", df["title"].tolist())

if st.button("Compare"):
    with st.spinner(""):
        fraud_intelli_spinner("Comparing Articles...")
        a = df[df["title"] == article1].iloc[0]
        b = df[df["title"] == article2].iloc[0]

        a_emb = embed_model.encode(a["summary"], convert_to_tensor=True)
        b_emb = embed_model.encode(b["summary"], convert_to_tensor=True)
        sim = util.cos_sim(a_emb, b_emb).item()

        prompt = f"Compare:\nA: {a['summary']}\n\nB: {b['summary']}\n\nExplain the similarity score {sim:.2f}."
        explanation = explain_model(prompt, max_length=200)[0]["generated_text"]

    st.info(f"Similarity: **{sim:.2f}**")
    st.success(explanation)

# =====================================================================
#  KEYWORD EXTRACTION
# =====================================================================
st.markdown("### 🧠 Extract Keywords")

user_text = st.text_area("Paste an article excerpt:")

if st.button("Extract"):
    if not user_text.strip():
        st.warning("Enter text first.")
    else:
        with st.spinner(""):
            fraud_intelli_spinner("Extracting Keywords...")
            kw = keyword_model.extract_keywords(user_text, keyphrase_ngram_range=(1,2))
        st.success(", ".join([k[0] for k in kw]))

# =====================================================================
#  FOOTER
# =====================================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align:center; opacity:0.7;'>
🚀 Built with <b>Fraud Intelli</b> |
A project by Clara Belluci, Troy Benner, Hoang Bui, and Tori-Ana McNeil<br>
In partnership with the <b>UNCC School of Data Science</b> and <b>USAA</b>.
</p>
""", unsafe_allow_html=True)
