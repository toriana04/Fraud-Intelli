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

    # Parse keywords properly
    df["keywords"] = df["keywords"].apply(
        lambda x: x if isinstance(x, list) else []
    )
    return df

df = load_data()

# Gather and normalize unique keywords
all_keywords = sorted({kw.lower().strip() for kw_list in df["keywords"] for kw in kw_list})


# ---------------------------------------------
# NLP-BASED SMART DEFINITION ENGINE (Option C)
# ---------------------------------------------
import re

def generate_smart_definition(term):
    """
    Automatically generate a fraud-aware, context-sensitive definition.
    Fraud-heavy terms get strong definitions; generic words get soft contextual ones.
    """
    t = term.lower().strip()

    # ----------------------------------------------------------
    # 1. Strong fraud / cyber / finance category classifications
    # ----------------------------------------------------------

    # Cyber Fraud Terms
    cyber_patterns = [
        "phish", "smish", "vish", "malware", "botnet", "breach",
        "credential", "ransom", "trojan", "spyware", "ddos",
        "spoof", "hack", "cyber", "attack"
    ]
    if any(p in t for p in cyber_patterns):
        return (
            f"{term.capitalize()} refers to cyber or digital threat activity commonly used "
            "to steal credentials, access accounts, or compromise financial systems."
        )

    # Crypto Fraud Terms
    crypto_patterns = [
        "crypto", "bitcoin", "wallet", "token", "nft", "blockchain", "defi"
    ]
    if any(p in t for p in crypto_patterns):
        return (
            f"{term.capitalize()} relates to digital assets or blockchain-based financial activity, "
            "which can be targeted through scams, unauthorized transfers, or misleading investment schemes."
        )

    # Financial & Investment Fraud Terms
    financial_patterns = [
        "investment", "investing", "investor", "investors", "securities",
        "broker", "brokerage", "stock", "stocks", "market", "markets",
        "pump", "dump", "forex", "finra", "fincen", "fintech",
        "finfluencers", "finfluencer", "finpro"
    ]
    if any(p in t for p in financial_patterns):
        return (
            f"{term.capitalize()} is associated with financial markets, brokerage services, or investment "
            "activity, which may be vulnerable to manipulation, misrepresentation, or fraud."
        )

    # Money Laundering & Financial Crime
    laundering_patterns = [
        "launder", "laundering", "embezzle", "fraudul", "fraudster",
        "fraudsters", "frauds", "fraud"
    ]
    if any(p in t for p in laundering_patterns):
        return (
            f"{term.capitalize()} refers to illicit financial activity involving deception, "
            "concealment of funds, or manipulation of financial transactions for unlawful gain."
        )

    # Identity Theft & Credential Misuse
    identity_patterns = [
        "identity", "id", "takeover", "compromised", "account",
        "ssn", "imposter", "impersonation", "authentication"
    ]
    if any(p in t for p in identity_patterns):
        return (
            f"{term.capitalize()} relates to identity misuse, unauthorized account access, or credential theft "
            "commonly observed in fraud events."
        )

    # Social Engineering & Scam Tactics
    scam_patterns = [
        "scam", "scams", "scammer", "scammers", "scheme", "sweepstakes",
        "telemarketing", "telemarketers"
    ]
    if any(p in t for p in scam_patterns):
        return (
            f"{term.capitalize()} involves deceptive communication intended to manipulate victims into "
            "sending money, revealing information, or granting unauthorized access."
        )

    # Mail Theft / Interception
    mail_patterns = [
        "mail", "mailbox", "mailboxes", "postal", "fedex", "usps",
        "envelopes", "deliveries", "courier"
    ]
    if any(p in t for p in mail_patterns):
        return (
            f"{term.capitalize()} is referenced in fraud cases involving stolen mail, intercepted packages, "
            "or unauthorized redirection of delivery services."
        )

    # Elder / Vulnerable Populations Fraud
    elder_patterns = [
        "elder", "elderly", "retirees", "seniors", "vulnerable"
    ]
    if any(p in t for p in elder_patterns):
        return (
            f"{term.capitalize()} is often used in discussions of fraud targeting older adults, who may be "
            "more vulnerable to coercion, deception, or financial exploitation."
        )

    # Regulatory / Compliance Terms
    regulatory_patterns = [
        "sec", "compliance", "committee", "committees", "subcommittee",
        "regulatory", "enforcement", "filings", "initiatives", "officers"
    ]
    if any(p in t for p in regulatory_patterns):
        return (
            f"{term.capitalize()} is frequently referenced in regulatory, oversight, or compliance contexts "
            "related to preventing, monitoring, or responding to fraud."
        )

    # ----------------------------------------------------------
    # 2. Generic soft-context definitions for non-fraud words
    # ----------------------------------------------------------
    soft_context_words = [
        # Administrative / organizational
        "agencies", "committee", "committees", "shareholders", "firms",
        "officers", "provider", "providers", "institutions", "notes",

        # Technology / devices
        "technology", "mobile", "smartphones", "phones", "sim",

        # Generic business or financial words
        "finance", "financial", "transactions", "exchanges", "markets",
        "offerings", "loans", "collateral",

        # Misc context terms
        "checklist", "initiatives", "legitimate", "increasingly",
        "breakthroughs", "carrier", "estate", "survey", "surveys",
        "vulnerable", "consumer", "consumers"
    ]

    if t in soft_context_words or len(t.split()) == 1:
        return (
            f"{term.capitalize()} is referenced in discussions related to fraud, compliance, or financial safety, "
            "serving as contextual information rather than describing a specific fraud technique."
        )

    # ----------------------------------------------------------
    # 3. Final fallback (rarely used now)
    # ----------------------------------------------------------
    return (
        f"{term.capitalize()} is mentioned in fraud-related contexts and contributes to understanding patterns, "
        "risks, or discussions surrounding financial crime."
    )


def get_definition(term):
    return generate_smart_definition(term)


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
    "Affinity Fraud": "Scams targeting identifiable community groups.",
    "Insider Trading": "Illegal trading of securities based on confidential information.",
    "Market Manipulation": "Artificially influencing market activity or prices.",
    "Ponzi Scheme": "Paying earlier investors with funds from new investors rather than profits.",
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
# SECTION 2 — SEARCH BAR
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
