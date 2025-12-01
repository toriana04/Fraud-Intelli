import streamlit as st

def inject_light_ui():
    css = """
    <style>

    .stApp {
        background-color: #FFFFFF !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F5F7FA !important;
        border-right: 1px solid #E6E9EF;
    }

    /* App headers */
    h1, h2, h3, h4 {
        color: #0A1A2F !important;
        font-weight: 700 !important;
    }

    /* Explorer Cards */
    .card {
        background-color: #FFFFFF;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #E6E9EF;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def sidebar_logo():
    st.sidebar.image("your_logo.png", use_container_width=True)
    st.sidebar.markdown("<h2 style='text-align:center; color:#0A1A2F;'>IntelliFraud</h2>", unsafe_allow_html=True)
