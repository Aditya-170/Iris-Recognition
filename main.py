import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'iris_recoginition'))


# Import page modules
from pages import dashboard, registration, login_page

# no external storage; templates are kept in filesystem
store = None
storage_error = None

# Page Config
st.set_page_config(
    page_title="IrisSecure - Iris Recognition System",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Yellow-Black Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit defaults */
    [data-testid="stSidebar"] {
        display: none;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Container - Black background */
    .main-container {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
        min-height: 100vh;
        color: #f0f0f0;
        padding-top: 90px;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
    }
    
    /* Navbar - Black with yellow accents */
    .navbar {
        background: rgba(20, 20, 20, 0.98);
        backdrop-filter: blur(20px);
        border-bottom: 2px solid #FFD700;
        padding: 1.25rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 6px 25px rgba(255, 215, 0, 0.15);
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 9999;
        margin: 0;
    }
    
    .navbar-brand {
        font-size: 1.75rem;
        font-weight: 800;
        color: #FFD700;
        cursor: pointer;
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }
    
    .navbar-brand:hover {
        transform: scale(1.05);
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    .navbar-nav {
        display: flex;
        gap: 0.75rem;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .nav-link {
        padding: 0.75rem 1.75rem;
        border-radius: 8px;
        background: transparent;
        color: #e0e0e0;
        border: 1px solid transparent;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        text-decoration: none;
        font-size: 0.95rem;
        white-space: nowrap;
    }
    
    .nav-link:hover {
        background: rgba(255, 215, 0, 0.1);
        border-color: #FFD700;
        color: #FFD700;
        transform: translateY(-2px);
    }
    
    .nav-link.active {
        background: #FFD700;
        color: #0f0f0f;
        border-color: transparent;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    .navbar-stats {
        display: flex;
        align-items: center;
        gap: 1.25rem;
        padding: 0.75rem 1.25rem;
        background: rgba(255, 215, 0, 0.05);
        border-radius: 8px;
        border: 1px solid rgba(255, 215, 0, 0.2);
        flex-wrap: wrap;
    }
    
    .stat-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #e0e0e0;
        font-size: 0.9rem;
    }
    
    .stat-value {
        color: #FFD700;
        font-weight: 700;
    }
    
    .stat-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #FFD700;
        box-shadow: 0 0 8px rgba(255, 215, 0, 0.7);
    }
    
    /* Cards */
    .card {
        background: rgba(35, 35, 35, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 215, 0, 0.15);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        border-color: rgba(255, 215, 0, 0.4);
        box-shadow: 0 12px 40px rgba(255, 215, 0, 0.15);
        transform: translateY(-2px);
    }
    
    .card h2, .card h3, .card h4 {
        color: #FFD700 !important;
        text-shadow: none;
    }
    
    .card p, .card li {
        color: #d0d0d0 !important;
    }
    
    /* Status Messages */
    .status-success {
        background: linear-gradient(135deg, #2d5f2e 0%, #3d7f3e 100%);
        color: #e0f0e0;
        padding: 1.25rem 1.75rem;
        border-radius: 10px;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0;
        border-left: 4px solid #5fff5f;
        box-shadow: 0 4px 15px rgba(95, 255, 95, 0.2);
    }
    
    .status-failed {
        background: linear-gradient(135deg, #5f2f2f 0%, #7f3f3f 100%);
        color: #ffe0e0;
        padding: 1.25rem 1.75rem;
        border-radius: 10px;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0;
        border-left: 4px solid #ff7f7f;
        box-shadow: 0 4px 15px rgba(255, 127, 127, 0.2);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #7f5f2f 0%, #9f7f3f 100%);
        color: #fff8e0;
        padding: 1.25rem 1.75rem;
        border-radius: 10px;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0;
        border-left: 4px solid #FFD700;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
    }
    
    .status-info {
        background: rgba(255, 215, 0, 0.1);
        color: #ffd700;
        padding: 1.25rem 1.75rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        margin: 1rem 0;
    }
    
    .status-info strong {
        color: #FFD700;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFC700 100%);
        color: #0f0f0f !important;
        border: none;
        border-radius: 8px;
        padding: 0.875rem 2rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(255, 215, 0, 0.4);
        background: linear-gradient(135deg, #FFED4E 0%, #FFD700 100%);
    }
    
    .stButton > button:disabled {
        background: rgba(100, 100, 100, 0.5);
        cursor: not-allowed;
        transform: none;
        color: #888888 !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(50, 50, 50, 0.9) !important;
        border: 1.5px solid rgba(255, 215, 0, 0.25) !important;
        border-radius: 8px;
        color: #f0f0f0 !important;
        padding: 0.875rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #888888 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.15) !important;
    }
    
    .stTextInput label, .stNumberInput label {
        color: #FFD700 !important;
        font-weight: 600;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: rgba(50, 50, 50, 0.6);
        border: 2px dashed rgba(255, 215, 0, 0.3);
        border-radius: 10px;
        padding: 1.5rem;
    }
    
    .stFileUploader label {
        color: #FFD700 !important;
        font-weight: 600;
    }
    
    /* Metrics */
    .stMetric {
        background: rgba(50, 50, 50, 0.8);
        padding: 1.25rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 215, 0, 0.2);
    }
    
    .stMetric label {
        color: #FFD700 !important;
        font-weight: 600;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-weight: 800;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FFD700, #FFC700);
    }
    
    /* Code blocks */
    code {
        background: rgba(40, 40, 40, 0.9) !important;
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #FFD700 !important;
        border: 1px solid rgba(255, 215, 0, 0.2);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(40, 40, 40, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 215, 0, 0.5);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 215, 0, 0.7);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .navbar {
            padding: 1rem;
            flex-direction: column;
            gap: 1rem;
        }
        
        .navbar-brand {
            font-size: 1.5rem;
        }
        
        .navbar-nav {
            width: 100%;
            justify-content: center;
        }
        
        .nav-link {
            padding: 0.6rem 1rem;
            font-size: 0.85rem;
        }
        
        .navbar-stats {
            width: 100%;
            justify-content: center;
            padding: 0.5rem 1rem;
        }
        
        .stat-badge {
            font-size: 0.8rem;
        }
        
        .card {
            padding: 1.25rem;
            margin: 1rem 0;
        }
        
        .main-container {
            padding-top: 180px;
        }
    }
    
    @media (max-width: 480px) {
        .navbar-nav {
            flex-direction: column;
            width: 100%;
        }
        
        .nav-link {
            width: 100%;
            text-align: center;
        }
        
        .card h2 {
            font-size: 1.5rem;
        }
        
        .card h3 {
            font-size: 1.25rem;
        }
        
        .main-container {
            padding-top: 250px;
        }
    }
    
    /* Footer */
    .footer-custom {
        text-align: center;
        padding: 2rem;
        color: #FFD700;
        font-size: 0.9rem;
        border-top: 1px solid rgba(255, 215, 0, 0.2);
        margin-top: 3rem;
        background: rgba(20, 20, 20, 0.9);
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
def init_session_state():
    defaults = {
        'page': 'Dashboard',
        'reg_step': 0,
        'reg_username': '',
        'reg_password': '',
        'face_cid': None,
        'iris_cid': None,
        'login_step': 0,
        'login_username': '',
        'login_password': '',
        'wallet_address': None,
        'authenticated': False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# handle query params for navigation
# `st.experimental_get_query_params` is deprecated; use `st.query_params` instead
params = st.query_params
if 'page' in params:
    page_val = params['page'][0]
    if page_val in ['Dashboard','Registration','Authentication']:
        st.session_state.page = page_val

# Get user count by scanning template directory
import glob
user_count = 0
system_status = "Unknown"
try:
    paths = glob.glob(os.path.join('templates','users','*.mat'))
    user_count = len(paths)
    system_status = "Operational" if user_count >= 0 else "Error"
except Exception:
    user_count = 0
    system_status = "Error"

# Navbar
navbar_html = """
<div class="navbar">
    <div class="navbar-brand" id="brand-link">�️ IrisSecure</div>
    <div class="navbar-nav">
        <div class="nav-link {dash_active}" id="nav-dashboard">
            Home
        </div>
        <div class="nav-link {reg_active}" id="nav-registration">
            Enroll
        </div>
        <div class="nav-link {auth_active}" id="nav-authentication">
            Verify
        </div>
    </div>
    <div class="navbar-stats">
        <div class="stat-badge">
            <div class="stat-dot"></div>
            <span>{system_status}</span>
        </div>
        <div class="stat-badge">
            <span>Profiles:</span>
            <span class="stat-value">{user_count}</span>
        </div>
    </div>
</div>
<script>
    const links = ['Dashboard','Registration','Verify'];
    links.forEach(p=>{{
        let pageName = p === 'Verify' ? 'Authentication' : p;
        const el = document.getElementById('nav-'+p.toLowerCase());
        if(el){{ el.style.cursor='pointer'; el.onclick = ()=>{{ window.location.search='?page='+pageName; }}}}
    }});
    const brand = document.getElementById('brand-link');
    if(brand){{ brand.style.cursor='pointer'; brand.onclick=()=>{{ window.location.search='?page=Dashboard'; }}}}
</script>
""".format(
    dash_active='active' if st.session_state.page=='Dashboard' else '',
    reg_active='active' if st.session_state.page=='Registration' else '',
    auth_active='active' if st.session_state.page=='Authentication' else '',
    system_status=system_status,
    user_count=user_count
)

st.markdown(navbar_html, unsafe_allow_html=True)

# Create columns for navigation buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home", key="btn_dashboard", use_container_width=True):
        st.session_state.page = 'Dashboard'
        st.rerun()

with col2:
    if st.button("📝 Enroll", key="btn_registration", use_container_width=True):
        st.session_state.page = 'Registration'
        st.rerun()

with col3:
    if st.button("✓ Verify", key="btn_authentication", use_container_width=True):
        st.session_state.page = 'Authentication'
        st.rerun()

# Route to appropriate page
if st.session_state.page == "Dashboard":
    dashboard.render()
elif st.session_state.page == "Registration":
    registration.render()
elif st.session_state.page == "Authentication":
    login_page.render()

# Footer
st.markdown("""
<div class="footer-custom">
    �️ IrisSecure | Advanced Iris Recognition System | © 2026
</div>
""", unsafe_allow_html=True)