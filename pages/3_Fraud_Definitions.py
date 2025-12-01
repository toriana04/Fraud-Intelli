import streamlit as st
import pandas as pd

# ---------------------------------------------
# PAGE CONFIG & HEADER
# ---------------------------------------------
st.set_page_config(page_title="Fraud Definitions", layout="wide")

st.markdown("""
<div style="text-align:center; margin-bottom:10px;">
    <img src="https://i.imgur.com/lAVJ7Vx.png" width="140" style="border-radius:20px;"/>
</div>

<h1 style="text-align:center; color:#04d9ff; font-weight:900;">
📘 Fraud Glossary & Definitions
</h1>

<p style="text-align:center; font-size:18px;">
A searchable glossary of fraud-related terms and formal fraud categories used in compliance, regulation, and enforcement.
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

# Unique keyword list
all_keywords = sorted({kw for lst in df["keywords"] for kw in lst})


# ---------------------------------------------
# TYPES OF FRAUD (CURATED LIST)
# ---------------------------------------------
FRAUD_TYPES = {
    "Investment Fraud": "Deceptive practices that induce investors to make financial decisions based on misleading, false, or incomplete information.",
    "Securities Fraud": "Illegal activities involving the manipulation or deception of investors in financial markets.",
    "Identity Theft": "When a criminal steals and uses personal information for unauthorized financial activity.",
    "Account Takeover": "When a fraudster gains unauthorized control of an individual's financial or online accounts.",
    "Money Laundering": "The process of disguising illegal financial proceeds as legitimate funds.",
    "Wire Fraud": "Fraud conducted via electronic communication, including phone, internet, or email.",
    "Phishing": "Social engineering attacks attempting to steal sensitive information by impersonating trusted entities.",
    "Elder Fraud": "Financial exploitation targeting older adults, often through scams, coercion, or deception.",
    "Affinity Fraud": "Scams targeting members of identifiable groups such as religious, ethnic, or professional communities.",
    "Insider Trading": "The illegal act of trading securities based on material, non-public information.",
    "Market Manipulation": "Interference with financial markets to create artificial asset prices or trading activity.",
    "Ponzi Scheme": "Fraudulent investments where returns are paid using funds from new investors instead of profits.",
    "Pyramid Scheme": "A business model that recruits members with the promise of payments for enrolling others rather than actual investments or sales.",
    "Embezzlement": "Theft or misappropriation of funds placed in someone's trust or belonging to their employer.",
    "Cyber Fraud": "Fraud conducted through digital channels, including hacking, malware, and unauthorized access.",
    "Credit Card Fraud": "Unauthorized use of another person’s credit card information for financial gain.",
    "Mortgage Fraud": "Intentional misrepresentation or omission of information used to obtain a home loan.",
    "Insurance Fraud": "Deception committed to obtain a benefit from an insurance provider through false claims or statements.",
}


# ---------------------------------------------
# BUILT-IN DEFINITIONS FOR KEYWORDS
# ---------------------------------------------
DEFAULT_DEFINITIONS = {
    "ponzi scheme": "A fraudulent investment operation where earlier investors are paid using the capital of new investors.",
    "scam": "A dishonest scheme designed to trick or defraud a person or organization.",
    "fraud": "Any intentional deception used to secure financial or personal gain.",
    "securities fraud": "Deceptive practices in stock or commodities markets intended to mislead investors.",
    "insider trading": "Illegal trading of securities based on confidential, non-public information.",
    "phishing": "Cyber deception involving impersonation to steal sensitive information.",
    "money laundering": "Disguising the origins of illegally obtained money to make it appear legitimate.",
    "identity theft": "The unauthorized acquisition and use of someone’s personal data for fraud.",
    "market manipulation": "Interfering with financial markets to create artificial prices or trading levels.",
    "investment fraud": "Any deceptive practice that persuades investors to make decisions based on misinformation.",
}

def get_definition(term):
    """Return definition if exists, else fallback."""
    if term in DEFAULT_DEFINITIONS:
        return DEFAULT_DEFINITIONS[term]

    return f"{term.capitalize()} refers to activity commonly connected to financial misconduct, fraud risk, or investor harm."


# ---------------------------------------------
# SECTION 1 — TYPES OF FRAUD GLOSSARY
# ---------------------------------------------
st.subheader("🧭 Major Types of Fraud")

for fraud_type, definition in FRAUD_TYPES.items():
    st.markdown(f"""
    <div style="padding:12px; margin-bottom:10px; border-radius:10px; 
                background-color:#0e1117; border:1px solid #04d9ff;">
        <h3 style="color:#04d9ff; margin-bottom:6px;">{fraud_type}</h3>
        <p style="font-size:16px; line-height:1.5;">{definition}</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------
# SECTION 2 — SEARCH KEYWORDS
# ---------------------------------------------
st.subheader("🔍 Search Fraud Terms (Keywords from Articles)")

search = st.text_input("Search for a keyword:", placeholder="Type a term...").lower().strip()

filtered_keywords = [kw for kw in all_keywords if search in kw] if search else all_keywords


# ---------------------------------------------
# SECTION 3 — KEYWORD DEFINITIONS
# ---------------------------------------------
st.subheader("📖 Keyword Glossary Derived from Articles")

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

