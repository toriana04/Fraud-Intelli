def inject_light_ui():
    css = """
    <style>

    .stApp {
        background-color: #FFFFFF !important;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #F5F7FA !important;
        border-right: 1px solid #E6E9EF;
    }

    /* Force-enable visible sidebar text */
    section[data-testid="stSidebar"] * {
        color: #0A1A2F !important;
    }

    /* Card styling */
    .card {
        background-color:#FFFFFF;
        padding:1.2rem;
        border-radius:12px;
        border:1px solid #E6E9EF;
        margin-bottom:1rem;
        box-shadow:0 1px 3px rgba(0,0,0,0.05);
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
