import streamlit as st
from intellifraud_ui import inject_light_ui, sidebar_logo

# ------------------------------------------------------
# PAGE CONFIG & UI
# ------------------------------------------------------
st.set_page_config(page_title="About IntelliFraud", layout="wide")
inject_light_ui()
sidebar_logo()

# ------------------------------------------------------
# HEADER HERO
# ------------------------------------------------------
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
        ℹ️ About IntelliFraud
    </h1>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# ABOUT SECTION (Light Mode Card)
# ------------------------------------------------------
st.markdown("""
<div style="
    background-color:#FFFFFF; 
    padding:25px; 
    border-radius:12px; 
    border:1px solid #E6E9EF; 
    box-shadow:0 1px 3px rgba(0,0,0,0.05);
    line-height:1.6;
">
    <p style="font-size:18px; color:#0A1A2F;">
        <strong style="color:#0A65FF;">IntelliFraud</strong> is an interactive fraud intelligence dashboard designed to help users explore 
        regulatory enforcement actions, fraud trends, keyword signals, and investigative insights.
    </p>

    <p style="font-size:18px; color:#0A1A2F;">
        This dashboard is powered by publicly available data such as FINRA enforcement actions 
        and built using <strong>Python</strong>, <strong>Streamlit</strong>, and modern data science workflows.
    </p>

    <p style="font-size:18px; color:#0A1A2F;">
        IntelliFraud was created by 
        <strong>Clara Belluci</strong>, 
        <strong>Troy Benner</strong>, 
        <strong>Hoang Bui</strong>, and 
        <strong>Tori-Ana McNeil</strong>, 
        in collaboration with the 
        <strong>UNC Charlotte School of Data Science</strong> and <strong>USAA</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# OPTIONAL FOOTER
# ------------------------------------------------------
st.markdown("""
<div style="
    text-align:center; 
    margin-top:40px; 
    color:#666; 
    font-size:14px;
">
    This project is intended for educational and analytical purposes only.
</div>
""", unsafe_allow_html=True)
