import streamlit as st
import pandas as pd

# Import UI theme (but NO sidebar logo)
from intellifraud_ui import inject_light_ui

# Import Supabase loader
from load_data_supabase import load_fraud_data

# Import your full dictionary of definitions
from definitions import TERM_DEFINITIONS


# ---------------------------------------------
# PAGE CONFIG & UI
# ---------------------------------------------
st.set_page_config(page_title="Fraud Definitions", layout="wide")
inject_light_ui()  # no sidebar_logo()


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
        Search official terminology, industry language, and key concepts used across fraud prevention, compliance, and regulatory reporting.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------
# LOAD DATA FROM SUPABASE
# ---------------------------------------------
@st.cache_data
def load_data():
    df = load_fraud_data()

    # Ensure keyword parsing
    df["keywords"] = df["keywords"].apply(
        lambda x: x if isinstance(x, list) else []
    )
    return df

df = load_data()


# Collect all keywords present in Supabase data
all_keywords = sorted({kw.lower() for kw_list in df["keywords"] for kw in kw_list})


# ---------------------------------------------
# SEARCH BAR
# ---------------------------------------------
st.subheader("🔍 Search Fraud Terms")

search = st.text_input(
    "Search for a term:",
    placeholder="Type a keyword such as 'phishing', 'markets', 'finra', 'mailboxes'..."
).lower().strip()

filtered_keywords = (
    [kw for kw in all_keywords if search in kw] if search else all_keywords
)


# ---------------------------------------------
# DISPLAY DEFINITIONS
# ---------------------------------------------
st.subheader("📖 Keyword Glossary")

if not filtered_keywords:
    st.info("No matching terms found.")
else:
    for term in filtered_keywords:
        definition = TERM_DEFINITIONS.get(term, "Definition not available.")

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
            <p style="font-size:15px; color:#0A1A2F; line-height:1.6;">
                {definition}
            </p>
        </div>
        """, unsafe_allow_html=True)
