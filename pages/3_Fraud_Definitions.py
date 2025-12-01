import streamlit as st
import pandas as pd
from intellifraud_ui import inject_light_ui, sidebar_logo

# ---------------------------------------------
# PAGE CONFIG & UI
# ---------------------------------------------
st.set_page_config(page_title="Fraud Definitions", layout="wide")
inject_light_ui()
sidebar_logo()

# ---------------------------------------------
# HEADER HERO
# ---------------------------------------------
st.markdown("""
<div style="
    padding: 25px; 
    background: #F5F7FA; 
    border-radius: 15px; 
    border: 1px solid #E6E9EF; 
    margin-bottom: 20px;
    text-align:center;
">
    <h1 style="color:#0A1A2F; margin-bottom:5px;">
        📘 Fraud Glossary & Definitions
    </h1>
    <p style="font-size:17px; color:#0A1A2F;">
        A searchable glossary of fraud-related terms and formal regulatory categories used in compliance and enforcement.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------
# LOAD DATA & KEYWORDS
# ---------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("fraud_analysis_final.csv")
    df["keywords"] = df["keywords"].fillna("").apply(
        lambda x: [k.strip().lower() for k in x.split(",") if k.strip()]
    )
    return df

df = load_data()

all_keywords = sorted({kw for lst in df["keywords"] for kw in lst})

# ---------------------------------------------
# FRAUD TYPE DEFINITIONS (Your curated list)
# ---------------------------------------------
FRAUD_TYPES = {
    "Investment Fraud": "Deceptive practices that induce investors to make financial decisions based on misleading or incomplete information.",
    "Securities Fraud": "Illegal activities involving deception or manipulation in securities markets.",
    "Identity Theft": "Criminal use of stolen personal information for unauthorized financial activity.",
    "Account Takeover": "Unauthorized access and control of a customer's financial or digital accounts.",
    "Money Laundering": "Disguising illicit financial proceeds to appear legitimate.",
    "Wire Fraud": "Fraud using electronic communication such as phone, internet, or email.",
    "Phishing": "Impersonation attacks to steal sensitive information.",
    "Elder Fraud": "Financial exploitation targeting older adults, often involving coercion or deception.",
    "Affinity Fraud": "Scams targeting members of identifiable groups such as religious or ethnic communities.",
    "Insider Trading": "Illegal trading of securities based on confidential, non-public information.",
    "Market Manipulation": "Interference with markets to artificially influence prices or trading volume.",
    "Ponzi Scheme": "Paying returns to investors using new investor money rather than profits.",
    "Pyramid Scheme": "Recruitment-based fraud where payouts depend on enrolling others.",
    "Embezzlement": "Theft or misappropriation of funds entrusted to someone.",
    "Cyber Fraud": "Fraud conducted via digital channels including hacking or malware.",
    "Credit Card Fraud": "Unauthorized use of someone’s credit card information.",
    "Mortgage Fraud": "Misrepresentation or omission of data to obtain a home loan.",
    "Insurance Fraud": "False claims or information to obtain illegitimate insurance benefits.",
}

# ---------------------------------------------
# BUILT-IN KEYWORD DEFINITIONS
# ---------------------------------------------
DEFAULT_DEFINITIONS = {
    "ponzi scheme": "A fraudulent operation where earlier investors are paid using funds from new investors.",
    "scam": "A dishonest scheme intended to deceive or defraud.",
    "fraud": "Intentional deception for financial or personal gain.",
    "securities fraud": "Deception in stock or commodities markets to mislead investors.",
    "insider trading": "Illegal trading based on confidential, non-public information.",
    "phishing": "Cyber deception involving impersonation to steal data.",
    "money laundering": "Disguising the origins of illegal money.",
    "identity theft": "Unauthorized use of someone's personal data.",
    "market manipulation": "Creating artificial market activity or prices.",
    "investment fraud": "Deceiving investors using misleading financial information.",
}

def get_definition(term):
    """Return an official or fallback definition."""
    if term in DEFAULT_DEFINITIONS:
        return DEFAULT_DEFINITIONS[term]
    return f"{term.capitalize()} refers to activity commonly associated with financial misconduct or fraud-related risk."

# ---------------------------------------------
# SECTION 1 — Major Fraud Types
# ---------------------------------------------
st.subheader("🧭 Major Types of Fraud")

for fraud_type, definition in FRAUD_TYPES.items():
    st.markdown(f"""
    <div style="
        padding:14px; 
        margin-bottom:12px; 
        border-radius:10px; 
        background-color:#FFFFFF; 
        border:1px solid #E6E9EF;
        box-shadow:0 1px 3px rgba(0,0,0,0.05);
    ">
        <h3 style="color:#0A65FF; margin-bottom:6px;">{fraud_type}</h3>
        <p style="font-size:15px; color:#0A1A2F; line-height:1.5;">
            {definition}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------
# SECTION 2 — Search Field
# ---------------------------------------------
st.subheader("🔍 Search Fraud Terms (Keywords from Articles)")

search = st.text_input(
    "Search for a keyword:",
    placeholder="Type a term such as 'phishing', 'laundering', 'identity'..."
).lower().strip()

filtered_keywords = [kw for kw in all_keywords if search in kw] if search else all_keywords

# ---------------------------------------------
# SECTION 3 — Keyword Glossary
# ---------------------------------------------
st.subheader("📖 Keyword Glossary Derived from Articles")

if not filtered_keywords:
    st.info("No matching terms found.")
else:
    for term in filtered_keywords:
        st.markdown(f"""
        <div style="
            padding:14px; 
            margin-bottom:12px; 
            border-radius:10px; 
            background-color:#FFFFFF; 
            border:1px solid #E6E9EF;
            box-shadow:0 1px 3px rgba(0,0,0,0.05);
        ">
            <h3 style="color:#0A65FF; margin-bottom:6px;">{term.capitalize()}</h3>
            <p style="font-size:15px; color:#0A1A2F; line-height:1.5;">
                {get_definition(term)}
            </p>
        </div>
        """, unsafe_allow_html=True)
