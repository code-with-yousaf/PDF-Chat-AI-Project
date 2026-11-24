import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="AI Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS ──────────────────────────────────────────────────
with open("style.css","r",encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────
if "view" not in st.session_state:
    st.session_state.view = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-icon">✦</div>', unsafe_allow_html=True)
    
    if st.button("🏠", use_container_width=True, key="nav_home"):
        st.session_state.view = "home"
        st.rerun()
    
    if st.button("💬", use_container_width=True, key="nav_chat"):
        st.session_state.view = "chat"
        st.rerun()
    
    if st.button("📄", use_container_width=True, key="nav_sources"):
        st.session_state.view = "sources"
        st.rerun()
    
    if st.button("🎨", use_container_width=True, key="nav_studio"):
        st.session_state.view = "studio"
        st.rerun()
    
    if st.button("⚙️", use_container_width=True, key="nav_settings"):
        st.session_state.view = "settings"
        st.rerun()

# ── Main Content ──────────────────────────────────────────────
if st.session_state.view == "home":
    # Hero Section
    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="beam"></div>', unsafe_allow_html=True)
    
    # Logo
    st.markdown('''
    <div class="hero-logo">
        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path d="M50,10 L80,25 L80,55 Q80,75 50,90 Q20,75 20,55 L20,25 Z" 
                  fill="url(#shieldGrad)" stroke="#a78bfa" stroke-width="2"/>
            <circle cx="50" cy="45" r="12" fill="#fff" opacity="0.9"/>
            <path d="M50,33 L50,42 M50,48 L50,57" stroke="#667eea" stroke-width="3" stroke-linecap="round"/>
        </svg>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<h1 class="hero-title">AI Assistant Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Your intelligent workspace companion</p>', unsafe_allow_html=True)
    
    # Glass Input Card
    st.markdown('<div class="glass-input-card">', unsafe_allow_html=True)
    user_input = st.text_input(
        "Ask me anything...",
        placeholder="Type your question here...",
        label_visibility="collapsed",
        key="home_input"
    )
    if st.button("Send", use_container_width=True, type="primary"):
        if user_input:
            st.session_state.view = "chat"
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "time": datetime.now().strftime("%H:%M")
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": "This is a demo version. AI features require local Ollama installation. Beautiful UI is fully functional! 🌟",
                "time": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action Chips
    st.markdown('<div class="action-chips">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💡 Generate ideas", use_container_width=True):
            st.session_state.view = "chat"
            st.rerun()
    
    with col2:
        if st.button("🎬 Motion concept", use_container_width=True):
            st.session_state.view = "studio"
            st.rerun()
    
    with col3:
        if st.button("📊 Market analysis", use_container_width=True):
            st.session_state.view = "chat"
            st.rerun()
    
    with col4:
        if st.button("🤖 Ask AI anything", use_container_width=True):
            st.session_state.view = "chat"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == "chat":
    st.markdown('<h1 class="page-title">💬 Chat Assistant</h1>', unsafe_allow_html=True)
    
    # Chat Messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            st.caption(msg.get("time", ""))
    
    # Chat Input
    user_msg = st.chat_input("Type your message...")
    if user_msg:
        st.session_state.messages.append({
            "role": "user",
            "content": user_msg,
            "time": datetime.now().strftime("%H:%M")
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Demo response: You said '{user_msg}'. Full AI features available with local installation! ✨",
            "time": datetime.now().strftime("%H:%M")
        })
        st.rerun()

elif st.session_state.view == "sources":
    st.markdown('<h1 class="page-title">📄 Document Sources</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-input-card">', unsafe_allow_html=True)
    st.markdown("### Upload PDF Documents")
    uploaded = st.file_uploader(
        "Upload PDF files for analysis",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded:
        st.success(f"✅ {len(uploaded)} file(s) uploaded successfully!")
        st.info("💡 PDF processing requires local installation with Ollama.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == "studio":
    st.markdown('<h1 class="page-title">🎨 AI Studio</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-input-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Quick Actions")
        st.button("💡 Generate Ideas", use_container_width=True)
        st.button("📝 Write Content", use_container_width=True)
        st.button("🔍 Research Topic", use_container_width=True)
        st.button("📊 Analyze Data", use_container_width=True)
    
    with col2:
        st.markdown("### 🛠️ AI Tools")
        st.button("🌐 Web Search", use_container_width=True)
        st.button("🎙️ Voice Input", use_container_width=True)
        st.button("🔊 Text-to-Speech", use_container_width=True)
        st.button("📝 Save Notes", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == "settings":
    st.markdown('<h1 class="page-title">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-input-card">', unsafe_allow_html=True)
    
    st.markdown("### 🌐 Language")
    lang = st.selectbox(
        "Select Language",
        ["🇬🇧 English", "🇵🇰 Roman Urdu", "🇵🇰 اردو", "🇫🇷 French", "🇸🇦 Arabic"],
        label_visibility="collapsed"
    )
    
    st.markdown("### 🎨 Theme")
    st.info("✨ Deep Space theme is active")
    
    st.markdown("### 🔧 AI Settings")
    st.info("💡 AI features require local Ollama installation")
    
    st.markdown("### 📊 About")
    st.markdown("""
    **AI Assistant Dashboard v1.0**
    
    - 🌌 Beautiful deep space UI
    - ✨ Glassmorphism design
    - 🎭 Animated elements
    - 📱 Responsive layout
    
    **Full features available with:**
    - Ollama (llama3.2:3b)
    - Local installation
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown('''
<div style="text-align:center; padding:2rem; opacity:0.5; font-size:0.85rem;">
    <p>✦ AI Assistant Dashboard • Built with Streamlit • Designed by Mayan Builds</p>
</div>
''', unsafe_allow_html=True)
