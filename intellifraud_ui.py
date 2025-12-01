import streamlit as st

def inject_light_ui():
    css = """
    <style>

    /* Make entire app bright and clean */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* Card style */
    .card {
        background-color: #FFFFFF;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #E6E9EF;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Titles */
    h1, h2, h3, h4 {
        color: #0A1A2F;
        font-weight: 700;
    }

    /* Search bar spacing */
    .stTextInput > div > div {
        border-radius: 10px;
    }

    /* DataFrame brightness */
    .dataframe {
        background: #FAFAFA;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #F5F7FA !important;
        border-right: 1px solid #E6E9EF;
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
