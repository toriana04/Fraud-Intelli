# ============================================================
#   FRAUD INTELLI PREMIUM BRAND THEME (FULL DARK MODE)
# ============================================================

st.markdown("""
<style>

    /* Global BG */
    .main, .reportview-container {
        background-color: #0A0F24 !important;
        color: #FFFFFF !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #11172B !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    section[data-testid="stSidebar"] * {
        color: #D6E2FF !important;
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #00F2FF !important;
        font-weight: 800 !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #8A2BE2, #00F2FF);
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.3rem;
        font-weight: 700;
        font-size: 16px;
    }

    .stButton>button:hover {
        opacity: 0.85;
        transform: scale(1.02);
        transition: 0.2s ease;
    }

    /* Text Inputs */
    .stTextInput>div>div>input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] {
        background-color: #121A2E;
        color: white !important;
        border: 1px solid #8A2BE2 !important;
        border-radius: 6px;
    }

    /* Dataframes */
    .stDataFrame, .dataframe {
        background-color: #11172B !important;
        color: white !important;
    }

    /* Alerts */
    .stAlert {
        background-color: rgba(138, 43, 226, 0.15) !important;
        border-left: 4px solid #8A2BE2 !important;
        color: #E6D9FF !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 7px; }
    ::-webkit-scrollbar-thumb {
        background: #8A2BE2;
        border-radius: 4px;
    }

    /* Fraud Intelli Cards */
    .fraud-card {
        background-color: #11172B;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00F2FF;
        margin-bottom: 15px;
        color: white;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
#   FRAUD INTELLI ANIMATED LOGO SPINNER  (Glow + Rotate Combo)
# ============================================================

st.markdown("""
<style>

@keyframes spinpulse {
  0% {
    transform: rotate(0deg) scale(1);
    filter: drop-shadow(0 0 0 #00F2FF);
  }
  50% {
    transform: rotate(180deg) scale(1.05);
    filter: drop-shadow(0 0 12px #00F2FF);
  }
  100% {
    transform: rotate(360deg) scale(1);
    filter: drop-shadow(0 0 0 #00F2FF);
  }
}

.spinner-premium {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 40px;
}

.spinner-logo-premium {
    width: 150px;
    animation: spinpulse 2.5s infinite ease-in-out;
}

</style>
""", unsafe_allow_html=True)

def fraud_intelli_spinner(message="Fraud Intelli is analyzing..."):
    st.markdown(f"""
        <h4 style='text-align:center; color:#8A2BE2;'>{message}</h4>
        <div class="spinner-premium">
            <img src="https://i.imgur.com/kIzoyP2.png" class="spinner-logo-premium">
        </div>
    """, unsafe_allow_html=True)

import streamlit as st

# ===== BRAND CSS (same block as above) =====

st.markdown("""
<div style='text-align:center;'>
    <img src='https://i.imgur.com/kIzoyP2.png' width='170'>
</div>

<h1 style='text-align:center;'>About Fraud Intelli</h1>
<p style='text-align:center; opacity:0.8;'>
AI-Powered Fraud Intelligence Platform
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class='fraud-card'>
    <h2>🛡️ Mission</h2>
    <p>
    Fraud Intelli leverages advanced AI, natural language understanding, 
    and modern analytics to help organizations detect, understand, and 
    respond to evolving fraud threats.
    </p>
</div>

<div class='fraud-card'>
    <h2>👥 Project Team</h2>
    <p>
    This project was created by <b>Clara Belluci, Troy Benner, Hoang Bui, and 
    Tori-Ana McNeil</b> in partnership with the <b>UNC Charlotte School of Data 
    Science</b> and <b>USAA</b>.
    </p>
</div>
""", unsafe_allow_html=True)