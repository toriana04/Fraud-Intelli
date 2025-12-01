import streamlit as st

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(page_title="About", layout="wide")

# ------------------------------------------------------
# HEADER
# ------------------------------------------------------
st.markdown("""
<div style="text-align:center; margin-bottom:10px;">
    <img src="https://i.imgur.com/kIzoyP2.png" width="150" style="border-radius:20px;"/>
</div>

<h1 style="text-align:center; color:#04d9ff; font-weight:900;">
ℹ️ About IntelliFraud
</h1>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# ABOUT DESCRIPTION
# ------------------------------------------------------
st.markdown("""
<div style="background-color:#0e1117; padding:25px; border-radius:12px; border:1px solid #04d9ff; margin-top:20px;">

<p style="font-size:18px; line-height:1.6;">
<strong style="color:#04d9ff;">IntelliFraud</strong> is an interactive fraud intelligence dashboard designed to help users explore 
regulatory actions, fraud trends, and enforcement insights.
</p>

<p style="font-size:18px; line-height:1.6;">
This dashboard is powered by publicly available data and built with <strong>Streamlit</strong>.
</p>

<p style="font-size:18px; line-height:1.6;">
Created by <strong>Clara Belluci</strong>, <strong>Troy Brenner</strong>, <strong>Hoang Bui</strong>, and <strong>Tori-Ana McNeil</strong> 
in collaboration with the <strong>UNC Charlotte School of Data Science</strong> and <strong>USAA</strong>.
</p>

</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# OPTIONAL FOOTER
# ------------------------------------------------------
st.markdown("""
<div style="text-align:center; margin-top:40px; color:#bdbdbd; font-size:14px;">
This project is intended for educational and analytical purposes only.
</div>
""", unsafe_allow_html=True)
