import streamlit as st

# Page settings
st.set_page_config(page_title="About", page_icon="💠", layout="wide")

# =====================================================================
#  LOGO AT TOP (SAME STYLE AS HOME PAGE)
# =====================================================================
st.markdown(
    """
    <style>
    .app-logo {
        width: 170px;
        border-radius: 20px;
        margin-top: -10px;
        margin-bottom: 10px;
        box-shadow: 0 0 15px rgba(139,92,246,0.35);
        cursor: pointer;
        transition: 0.2s;
    }
    .app-logo:hover {
        transform: scale(1.04);
        box-shadow: 0 0 22px rgba(139,92,246,0.55);
    }
    </style>

    <div style='text-align: center;'>
        <a href="/">
            <img class='app-logo' src='../logo.png'>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================================
#  PAGE TITLE
# =====================================================================

st.markdown(
    """
    <h1 style='
        text-align: center;
        font-size: 3rem;
        background: linear-gradient(90deg, #8b5cf6, #22d3ee, #6366f1);
        -webkit-background-clip: text;
        color: transparent;
        font-weight: 800;
        margin-bottom: 20px;
    '>
        About This Project
    </h1>
    """,
    unsafe_allow_html=True
)

# =====================================================================
#  CONTENT CARD
# =====================================================================

st.markdown(
    """
    <div style='
        background: rgba(255,255,255,0.06);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        font-size: 1.18rem;
        line-height: 1.75;
        color: #e0e0e0;
        max-width: 900px;
        margin: 0 auto;
    '>
        This project was created by 
        <b>Clara Belluci</b>, 
        <b>Troy Benner</b>, 
        <b>Hoang Bui</b>, and 
        <b>Tori-Ana McNeil</b> 
        in partnership with the 
        <b>UNC Charlotte School of Data Science</b> and <b>USAA</b>.
        <br/><br/>
        The FINRA Fraud Intelligence Engine is a modern, AI-powered platform
        built using Natural Language Processing (NLP), semantic search, and
        transformer-based models. Its goal is to help users explore fraud-related
        insights, understand relationships between concepts, and analyze
        patterns across multiple FINRA articles.
        <br/><br/>
        This project includes:
        <ul>
            <li>Semantic search using BERT embeddings</li>
            <li>Fraud category classification</li>
            <li>AI-powered article explanation (FLAN-T5)</li>
            <li>Interactive comparison tools</li>
            <li>A modern, sleek user interface with a premium design</li>
        </ul>
        <br/>
        This platform demonstrates the power of combining data science, 
        machine learning, and user-friendly design to create an intelligent, 
        intuitive fraud analysis tool.
    </div>
    """,
    unsafe_allow_html=True
)
