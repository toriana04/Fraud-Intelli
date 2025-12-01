import streamlit as st
import pandas as pd

# ---------------------------------------------
# PAGE CONFIG & HEADER
# ---------------------------------------------
st.set_page_config(page_title="Fraud Definitions", layout="wide")

st.markdown("""
<div style="text-align:center; margin-bottom:10px;">
    <img src="https://i.imgur.com/kIzoyP2.png" width="140" style="border-radius:20px;"/>
</div>

<h1 style="text-align:center; color:#04d9ff; font-weight:900;">
📘 Fraud Glossary & Definitions
</h1>

<p style="text-align:center; font-size:18px;">
A searchable glossary of fraud-related terms sourced from real FINRA articles.
</p>
""", unsafe_allow_html=True)


# ---------------------------------------------
# LOAD CSV & EXTRACT KEYWORDS
# ---------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")
    df["keywords"] = df["keywords"].fillna("").apply(
        lambda x: [k.strip().lower() for k in x.split(",") if k.strip()]
    )
    return df

df = load_data()

# Get unique keywords
all_keywords = sorted({kw for lst in df["keywords"] for kw in lst})


# ---------------------------------------------
# BUILT-IN DEFINITIONS (expandable later)
# ---------------------------------------------
DEFAULT_DEFINITIONS = {
    "ponzi scheme": "A fraudulent investment operation where returns are paid from new investors rather than legitimate business profits.",
    "scam": "A dishonest scheme intended to mislead, trick, or defraud someone.",
    "fraud": "Any wrongful or criminal deception intended to result in financial or personal gain.",
    "securities fraud": "A deceptive practice in the stock or commodities markets that leads investors to make financial decisions based on false information.",
    "insider trading": "The illegal practice of trading stocks or securities based on confidential, non-public information.",
    "phishing": "A cyberattack where scammers impersonate trusted entities to steal personal or financial information.",
    "money laundering": "The process of making illegally-gained proceeds appear legal through complex financial transactions.",
    "identity theft": "A crime where someone wrongfully obtains and uses another person’s personal data for fraud or deception.",
    "market manipulation": "Intentional interference with the free and fair operation of the market to create artificial prices.",
    "investment fraud": "Deceptive practices that induce investors to make decisions based on false, misleading, or incomplete information.",
}


def get_definition(term):
    """Return definition if exists, else a generic fallback."""
    if term in DEFAULT_DEFINITIONS:
        return DEFAULT_DEFINITIONS[term]

    # Generic fallback definition (safe + non-AI-generated risk)
    return f"{term.capitalize()} refers to activity or behavior commonly associated with financial misconduct, fraud risk, or deceptive practices. It may appear in regulatory alerts, investor warnings, or enforcement cases."


# ---------------------------------------------
# SEARCH BAR
# ---------------------------------------------
st.subheader("🔍 Search Fraud Terms")

search = st.text_input("Search for a keyword:", placeholder="Type a term...").lower().strip()

filtered_keywords = [kw for kw in all_keywords if search in kw] if search else all_keywords


# ---------------------------------------------
# DISPLAY GLOSSARY
# ---------------------------------------------
st.subheader("📖 Glossary of Fraud Terms")

if not filtered_keywords:
    st.info("No matching terms found.")
else:
    for term in filtered_keywords:
        st.markdown(f"""
        <div style="padding:12px; margin-bottom:10px; border-radius:10px; 
                    background-color:#0e1117; border:1px solid #04d9ff;">
            <h3 style="color:#04d9ff; margin-bottom:6px;">{term.capitalize()}</h3>
            <p style="font-size:16px; line-height:1.5;">{get_definition(term)}</p>
        </div>
        """, unsafe_allow_html=True)
