import streamlit as st

def render():
    """Render the professional dashboard page"""
    
    st.markdown('<div class="card" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown("""
        <h2 style="color: #1d4ed8; margin-bottom: 1rem;">Welcome to IrisAuth</h2>
        <p style="color: #6b7280; font-size: 1.1rem; line-height: 1.6;">
        Secure and efficient iris-based authentication system.
        </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # System Overview
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #1d4ed8; text-align: center; margin-bottom: 2rem;">System Overview</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(29, 78, 216, 0.1); border: 1px solid rgba(29, 78, 216, 0.3); border-radius: 12px; padding: 1.5rem; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem; color: #2563eb;">🔒</div>
            <h4 style="color: #2563eb; margin-bottom: 0.5rem;">Iris Recognition</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Accurate and fast template matching</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 1.5rem; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem; color: #10b981;">👁️</div>
            <h4 style="color: #10b981; margin-bottom: 0.5rem;">Iris Scanning</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Seamless and secure scanning process</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(234, 88, 12, 0.1); border: 1px solid rgba(234, 88, 12, 0.3); border-radius: 12px; padding: 1.5rem; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem; color: #ea580c;">💾</div>
            <h4 style="color: #ea580c; margin-bottom: 0.5rem;">Local Storage</h4>
            <p style="color: #6b7280; font-size: 0.9rem;">Encrypted and secure local storage</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
  
    
    # Technical Details
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #4f46e5; text-align: center; margin-bottom: 1.5rem;">Technical Specifications</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #4f46e5;">
            <h4 style="color: #4f46e5; margin-bottom: 1rem;">Registration Process</h4>
            <ol style="color: #94a3b8; font-size: 0.95rem; line-height: 1.8;">
                <li>Create unique username and secure password</li>
                <li>Upload iris images (minimum 5 high-quality scans)</li>
                <li>Encrypted storage of biometric CIDs</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h4 style="color: #059669; margin-bottom: 0.5rem;">Storage</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">Decentralized IPFS with cryptographic verification</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Security Features
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #4f46e5; text-align: center; margin-bottom: 1.5rem;">Security Features</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h4 style="color: #4f46e5; margin-bottom: 0.5rem;">Encryption</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">Fernet symmetric encryption for biometric data at rest</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h4 style="color: #7c3aed; margin-bottom: 0.5rem;">Authentication</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">JWT-based password verification with SHA256 hashing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 12px; text-align: center;">
            <h4 style="color: #059669; margin-bottom: 0.5rem;">Storage</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">Decentralized IPFS with cryptographic verification</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)