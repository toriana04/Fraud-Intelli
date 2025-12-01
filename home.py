# =====================================================================
#                           INTELLIFRAUD APP
#      Supabase-Powered AI Fraud Intelligence & Search Platform
# =====================================================================

import streamlit as st
import pandas as pd
import torch
import time
import io
import os
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# =====================================================================
#  STREAMLIT PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="IntelliFraud",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================================
#  LOAD ENVIRONMENT VARIABLES
# =====================================================================
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

SUPABASE_BUCKET = "DTSC_project"
SUPABASE_CSV_PATH = "csv/fraud_articles.csv"

# =====================================================================
#  INTELLIFRAUD PREMIUM NEON DARK THEME
# =====================================================================
st.markdown("""
<style>

.main, .reportview-container {
    background-color: #0A0F24 !important;
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] {
    background-color: #11172B !important;
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] * {
    color: #D6E2FF !important;
}

h1, h2, h3, h4 {
    color: #00F2FF !important;
    font-weight: 800 !important;
}

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
    opacity: 0.8;
    transform: scale(1.02);
    transition: 0.2s ease;
}

.stTextInput>div>div>input,
.stTextArea textarea {
    background-color: #121A2E;
    color: white !important;
    border: 1px solid #8A2BE2 !important;
    border-radius: 6px;
}

.card {
    background: rgba(255,255,255,0.07);
    padding: 22px;
    margin-bottom: 20px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(10px);
}

.keyword-chip {
    background: rgba(138, 43, 226, 0.25);
    display: inline-block;
    padding: 6px 12px;
    margin: 3px;
    border-radius: 12px;
    border: 1px solid #8A2BE2;
}
</style>
""", unsafe_allow_html=True)

# =====================================================================
#  SPINNER ANIMATION
# =====================================================================
st.markdown("""
<style>
@keyframes spinpulse {
  0% { transform: rotate(0deg) scale(1); filter: drop-shadow(0 0 0 #00F2FF); }
  50% { transform: rotate(180deg) scale(1.06); filter: drop-shadow(0 0 15px #00F2FF); }
  100% { transform: rotate(360deg) scale(1); filter: drop-shadow(0 0 0 #00F2FF); }
}
.spinner-premium {
    display: flex;
    justify-content: center;
    align-items: center;
}
.spinner-logo-premium {
    width: 130px;
    animation: spinpulse 2.4s infinite ease-in-out;
}
</style>
""", unsafe_allow_html=True)

def show_spinner(text="IntelliFraud is analyzing…"):
    st.markdown(f"<h4 style='text-align:center;color:#8A2BE2;'>{text}</h4>", unsafe_allow_html=True)
    st.markdown("""
        <div class='spinner-premium'>
            <img src='https://i.imgur.com/kIzoyP2.png' class='spinner-logo-premium'>
        </div>
    """, unsafe_allow_html=True)

# =====================================================================
#  SUPABASE FUNCTIONS
# =====================================================================
@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@st.cache_data
def load_data():
    sb = get_supabase()
    file_bytes = sb.storage.from_(SUPABASE_BUCKET).download(SUPABASE_CSV_PATH)

    df = pd.read_csv(io.BytesIO(file_bytes))
    
    # Normalize types
    df["summary"] = df["summary"].astype(str)
    df["keywords"] = df["keywords"].astype(str)
    df["date"] = df["date"].astype(str)

    return df

# =====================================================================
#  LOAD MODELS
# =====================================================================
show_spinner("Loading IntelliFraud NLP Models...")
@st.cache_resource
def load_models():
    embed = SentenceTransformer("all-MiniLM-L6-v2")
    explain = pipeline("text2text-generation", model="google/flan-t5-small")
    return embed, explain

embed_model, explain_model = load_models()

# Load article data
show_spinner("Loading Fraud Articles from Supabase...")
df = load_data()
summary_embeddings = embed_model.encode(df["summary"].tolist(), convert_to_tensor=True)

# =====================================================================
#  FRAUD TAGGING LOGIC
# =====================================================================
FRAUD_TAGS = {
    "AI Fraud": ["ai", "deepfake", "artificial intelligence"],
    "Check Fraud": ["check fraud", "check washing"],
    "Elder Fraud": ["older adult", "senior"],
    "Account Takeover": ["account takeover", "hacked"],
    "Investment Scam": ["crypto", "investment scam", "pump and dump"],
    "Disaster Fraud": ["disaster", "relief scam"],
    "General Fraud": ["fraud", "scam"]
}

def classify(text):
    t = text.lower()
    for tag, words in FRAUD_TAGS.items():
        if any(w in t for w in words):
            return tag
    return "General Fraud"

df["tag"] = df["summary"].apply(classify)

# =====================================================================
#  SIDEBAR CONTENT
# =====================================================================
st.sidebar.image("https://i.imgur.com/kIzoyP2.png", width=130)
st.sidebar.header("🧭 IntelliFraud Menu")

# Search history
if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.subheader("Search History")
if st.session_state.history:
    for q in st.session_state.history[-10:]:
        st.sidebar.write(f"• {q}")
else:
    st.sidebar.write("No searches yet.")

if st.sidebar.button("Clear History"):
    st.session_state.history = []
    st.sidebar.success("History cleared.")

fraud_filter = st.sidebar.selectbox("Filter by Fraud Category", ["All"] + list(FRAUD_TAGS.keys()))

# =====================================================================
#  TABS
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["🔎 IntelliFraud Search", "🤖 AI Explain", "⚖️ Compare", "📚 About"]
)

# =====================================================================
#  TAB 1 — SEARCH
# =====================================================================
with tab1:
    st.image("https://i.imgur.com/kIzoyP2.png", width=150)
    st.markdown("<h1 style='text-align:center;'>IntelliFraud Search Engine</h1>", unsafe_allow_html=True)

    query = st.text_input("Search for a fraud topic, article summary, or pattern:")

    if query:
        st.session_state.history.append(query)

        with st.spinner("Searching…"):
            q_emb = embed_model.encode(query, convert_to_tensor=True)
            sims = util.cos_sim(q_emb, summary_embeddings)[0]
            best_idx = torch.argmax(sims).item()
            best_score = float(sims[best_idx])
            best = df.iloc[best_idx]

        if fraud_filter != "All" and best["tag"] != fraud_filter:
            st.info(f"No direct match for '{fraud_filter}'. Showing closest overall result.")

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### 🏆 Best Match: **{best['title']}**")
        st.write(f"📅 **Published:** `{best['date']}`")
        st.write(f"🔗 [Read Article]({best['url']})")
        st.write(f"📊 **Relevance Score:** `{best_score:.4f}`")
        st.write(f"🏷 **Category:** `{best['tag']}`")

        st.markdown("### Summary")
        st.write(best["summary"])

        st.markdown("### Keywords")
        for kw in best["keywords"].split(","):
            st.markdown(f"<span class='keyword-chip'>{kw.strip()}</span>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
#  TAB 2 — AI EXPLAIN
# =====================================================================
with tab2:
    st.image("https://i.imgur.com/kIzoyP2.png", width=150)
    st.markdown("<h1 style='text-align:center;'>Explain a Fraud Concept</h1>", unsafe_allow_html=True)

    explain_input = st.text_area("Paste an article snippet, scam description, or fraud pattern:")

    if st.button("Generate Explanation"):
        with st.spinner("Generating explanation…"):
            out = explain_model(
                f"Explain this fraud concept in simple terms: {explain_input}",
                max_length=180
            )[0]["generated_text"]

        st.success(out)

# =====================================================================
#  TAB 3 — COMPARE
# =====================================================================
with tab3:
    st.image("https://i.imgur.com/kIzoyP2.png", width=150)
    st.markdown("<h1 style='text-align:center;'>Compare Two Articles</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        a1 = st.selectbox("Select first article", df["title"].tolist())
    with col2:
        a2 = st.selectbox("Select second article", df["title"].tolist())

    if st.button("Compare Articles"):
        article1 = df[df["title"] == a1].iloc[0]
        article2 = df[df["title"] == a2].iloc[0]

        e1 = embed_model.encode(article1["summary"], convert_to_tensor=True)
        e2 = embed_model.encode(article2["summary"], convert_to_tensor=True)
        sim = float(util.cos_sim(e1, e2)[0][0])

        st.write(f"### Similarity Score: `{sim:.4f}`")

        with st.spinner("Generating comparison insights…"):
            explanation = explain_model(
                f"Compare these two fraud summaries:\n"
                f"A: {article1['summary']}\n"
                f"B: {article2['summary']}\n"
                f"Explain what a similarity score of {sim:.4f} means.",
                max_length=200
            )[0]["generated_text"]

        st.success(explanation)

# =====================================================================
#  TAB 4 — ABOUT
# =====================================================================
with tab4:
    st.image("https://i.imgur.com/kIzoyP2.png", width=150)
    st.markdown("<h1 style='text-align:center;'>About IntelliFraud</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
        <h3>What is IntelliFraud?</h3>
        <p>
        IntelliFraud is an AI-powered fraud intelligence engine that uses semantic search,
        natural language understanding, and Supabase cloud storage to analyze FINRA fraud-related articles.
        </p>

        <h3>Project Team</h3>
        <p>
        Created by <b>Clara Belluci</b>, <b>Troy Benner</b>, <b>Hoang Bui</b>, and <b>Tori-Ana McNeil</b>
        for the UNC Charlotte School of Data Science in partnership with USAA.
        </p>
    </div>
    """, unsafe_allow_html=True)
