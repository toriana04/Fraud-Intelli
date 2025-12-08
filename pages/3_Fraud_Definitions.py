import streamlit as st
import pandas as pd
from intellifraud_ui import inject_light_ui

# NEW — load live data from Supabase
from load_data_supabase import load_fraud_data

# ---------------------------------------------
# PAGE CONFIG & UI
# ---------------------------------------------
st.set_page_config(page_title="Fraud Definitions", layout="wide")
inject_light_ui()

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
# LOAD SUPABASE DATA
# ---------------------------------------------
@st.cache_data
def load_data():
    df = load_fraud_data()

    # Parse keywords if necessary
    df["keywords"] = df["keywords"].apply(
        lambda x: x if isinstance(x, list) else []
    )
    return df

df = load_data()

# gather unique keywords
all_keywords = sorted({kw.lower().strip() for kw_list in df["keywords"] for kw in kw_list})

# ---------------------------------------------
# EXPANDED KEYWORD DEFINITIONS (MUCH BROADER)
# ---------------------------------------------
KEYWORD_DEFINITIONS = {
    "ponzi scheme": "A fraud where returns for older investors are paid using new investor funds rather than actual profits.",
    "ponzi": "A form of investment fraud using new investor money to pay old investors.",
    "scam": "A deceptive operation intended to defraud a victim.",
    "fraud": "Intentional deception for financial or personal gain.",
    "securities fraud": "Illegal manipulation or deception in stock or commodities markets.",
    "insider trading": "Buying or selling securities based on confidential, non-public information.",
    "phishing": "A cyberattack where criminals impersonate trusted entities to steal data.",
    "smishing": "Text-message-based phishing designed to steal credentials or money.",
    "vishing": "Voice-based phishing using fraudulent phone calls.",
    "money laundering": "The process of disguising illegally obtained money as legitimate income.",
    "identity theft": "Using another person's personal information without permission for fraud.",
    "market manipulation": "Artificially influencing market prices or trading volume.",
    "investment fraud": "Deceiving investors using false information, fake opportunities, or misleading claims.",
    "account takeover": "Unauthorized access and control of a victim's login-protected accounts.",
    "cyber fraud": "Fraud executed through digital systems, malware, or unauthorized access.",
    "credit card fraud": "Unauthorized use of a cardholder’s financial information.",
    "wire fraud": "Using electronic communications (email, phone, internet) to execute a fraudulent scheme.",
    "elder fraud": "Scams that target older adults through coercion, deception, or financial manipulation.",
    "pump and dump": "Artificially inflating a stock price through misleading statements before selling it off.",
}

def get_definition(term):
    """Match definitions flexibly and avoid repetitive fallback text."""
    t = term.lower().strip()

    # Direct match
    if t in KEYWORD_DEFINITIONS:
        return KEYWORD_DEFINITIONS[t]

    # Partial match (e.g., "phishing scams" → "phishing")
    for key in KEYWORD_DEFINITIONS:
        if key in t:
            return KEYWORD_DEFINITIONS[key]

    # Unique fallback (no repetition)
    return f"{term.capitalize()} is a term commonly associated with fraud, risk, or financial misconduct within regulatory and compliance contexts."

# ---------------------------------------------
# SECTION 1 — MAJOR FRAUD TYPES
# ---------------------------------------------
st.subheader("🧭 Major Types of Fraud")

FRAUD_TYPES = {
    "Investment Fraud": "Deceptive practices that induce investors to make financial decisions based on misleading or incomplete information.",
    "Securities Fraud": "Illegal activities involving deception or manipulation in securities markets.",
    "Identity Theft": "Criminal use of stolen personal information for unauthorized financial activity.",
    "Account Takeover": "Unauthorized access and control of a customer's financial or digital accounts.",
    "Money Laundering": "Disguising illicit financial proceeds to appear legitimate.",
    "Wire Fraud": "Fraud using electronic communication such as phone, internet, or email.",
    "Phishing": "Impersonation attacks to steal sensitive information.",
    "Elder Fraud": "Financial exploitation targeting older adults.",
    "Affinity Fraud": "Scams targeting members of identifiable social or community groups.",
    "Insider Trading": "Illegal trading of securities based on confidential information.",
    "Market Manipulation": "Artificially influencing market activity or prices.",
    "Ponzi Scheme": "Paying earlier investors with funds from new investors rather than profit.",
}

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
# SECTION 2 — SEARCH FIELD
# ---------------------------------------------
st.subheader("🔍 Search Fraud Terms (Keywords from Articles)")

search = st.text_input(
    "Search for a keyword:",
    placeholder="Type a term such as 'phishing', 'laundering', 'identity'..."
).lower().strip()

filtered_keywords = (
    [kw for kw in all_keywords if search in kw] if search else all_keywords
)

# ---------------------------------------------
# SECTION 3 — KEYWORD GLOSSARY
# ---------------------------------------------
st.subheader("📖 Keyword Glossary Derived from Articles")

if not filtered_keywords:
    st.info("No matching terms found.")
else:
    for term in filtered_keywords:
        definition = get_definition(term)
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
                {definition}
            </p>
        </div>
        """, unsafe_allow_html=True)
