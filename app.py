import streamlit as st
import os, threading, random, string
from datetime import datetime

st.set_page_config(
    page_title="AI Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── optional libs ─────────────────────────────────────────────
try:    
    from openai import OpenAI
    OPENAI_OK = True
except: 
    OPENAI_OK = False

os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"
DATA = "data"; os.makedirs(DATA, exist_ok=True)

@st.cache_resource(show_spinner=False)
def get_ai_client():
    """Get AI client (supports OpenAI, Groq, Hugging Face, OpenRouter)"""
    if not OPENAI_OK: 
        return None, "OpenAI library not installed"
    
    # Try to get API key from secrets or env
    api_key = None
    key_source = "not found"
    
    try:
        if hasattr(st, 'secrets'):
            if "OPENROUTER_API_KEY" in st.secrets:
                api_key = st.secrets["OPENROUTER_API_KEY"]
                key_source = "OPENROUTER_API_KEY from secrets"
            elif "OPENAI_API_KEY" in st.secrets:
                api_key = st.secrets["OPENAI_API_KEY"]
                key_source = "OPENAI_API_KEY from secrets"
            elif "AGNES_API_KEY" in st.secrets:
                api_key = st.secrets["AGNES_API_KEY"]
                key_source = "AGNES_API_KEY from secrets"
            elif "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
                key_source = "GROQ_API_KEY from secrets"
            elif "HUGGINGFACE_API_KEY" in st.secrets:
                api_key = st.secrets["HUGGINGFACE_API_KEY"]
                key_source = "HUGGINGFACE_API_KEY from secrets"
    except:
        pass  # Secrets not available or empty
    
    if not api_key:
        try:
            api_key = (os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY") or 
                       os.getenv("AGNES_API_KEY") or os.getenv("GROQ_API_KEY") or 
                       os.getenv("HUGGINGFACE_API_KEY"))
            if api_key:
                key_source = "environment variable"
        except:
            pass
    
    if not api_key:
        # Demo mode - no API key configured
        return None, None
    
    try:
        # Detect which API based on key format
        if api_key.startswith("sk-or-"):
            # OpenRouter API
            client = OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            return client, f"Connected to OpenRouter (key: {api_key[:15]}...)"
        elif api_key.startswith("sk-proj-"):
            # OpenAI project key
            client = OpenAI(api_key=api_key)
            return client, f"Connected to OpenAI (key: {api_key[:15]}...)"
        elif api_key.startswith("sk-") and len(api_key) < 60:
            # Try OpenAI first (most compatible)
            try:
                client = OpenAI(api_key=api_key)
                return client, f"Connected via OpenAI API (key: {api_key[:15]}...)"
            except:
                return None, None
        elif api_key.startswith("sk-"):
            # Standard OpenAI key
            client = OpenAI(api_key=api_key)
            return client, f"Connected to OpenAI (key: {api_key[:15]}...)"
        elif api_key.startswith("hf_"):
            # Hugging Face API
            client = OpenAI(
                api_key=api_key,
                base_url="https://api-inference.huggingface.co/v1/"
            )
            return client, "Connected to Hugging Face"
        else:
            # Groq API (gsk_...)
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            return client, "Connected to Groq"
    except Exception as e:
        # If any error, return None for demo mode
        return None, None

def chat_with_ai(messages, client):
    """Send messages to AI and get response"""
    if not client:
        # Demo mode - return intelligent placeholder responses
        user_msg = messages[-1]["content"].lower() if messages else ""
        
        # Simple keyword-based demo responses
        if "hello" in user_msg or "hi" in user_msg or "hey" in user_msg or "assalam" in user_msg:
            return "👋 **Hello! Welcome to AI Assistant Dashboard!**\n\nI'm currently running in **demo mode** to showcase this beautiful interface.\n\n**✨ Features You Can See:**\n- 🌌 Stunning space theme with animated stars\n- 💬 Clean chat interface\n- 📄 Document upload section\n- 🎨 Studio tools\n- ⚙️ Settings panel\n- 🌍 Multi-language support\n\n*This is a portfolio showcase project demonstrating modern UI/UX design and full-stack development skills!*"
        
        elif "how are you" in user_msg or "kaise ho" in user_msg or "kaisa hai" in user_msg:
            return "I'm doing great! 😊\n\nThis is a **demo response** showing how the chat interface works. The UI is fully functional with beautiful animations and smooth interactions!\n\n*In production mode with an API key, I'd provide real AI-powered intelligent responses.*"
        
        elif "help" in user_msg or "mada" in user_msg:
            return "**📚 Available Features:**\n\n🏠 **Home View**\n- Beautiful hero section\n- Glass input card\n- Quick action chips\n\n💬 **Chat View** (You're here!)\n- Message history\n- Typing indicators\n- Smooth animations\n\n📄 **Sources**\n- PDF upload interface\n- Document management\n- Note-taking system\n\n🎨 **Studio**\n- AI tools access\n- Quick actions\n- Feature shortcuts\n\n⚙️ **Settings**\n- Language preferences\n- Theme options\n- Configuration panel\n\n---\n*Navigate using the icon sidebar on the left!*"
        
        elif "project" in user_msg or "about" in user_msg or "details" in user_msg:
            return "**🌟 AI Assistant SaaS Dashboard**\n\n**Tech Stack:**\n- Frontend: Streamlit + Custom CSS\n- Backend: Python 3.11+\n- AI: Multi-provider support (OpenAI, Groq, Hugging Face)\n- Deployment: GitHub + Streamlit Cloud\n\n**Key Features:**\n- ✅ Beautiful deep space UI\n- ✅ 60 animated twinkling stars\n- ✅ Glassmorphism design\n- ✅ Responsive layout\n- ✅ Multi-language support\n- ✅ Production-ready code\n\n**Developer:** Mayan Builds  \n**GitHub:** https://github.com/code-with-yousaf/PDF-Chat-AI-Project\n\n*View the complete project report for detailed documentation!*"
        
        elif "feature" in user_msg or "capability" in user_msg or "can you" in user_msg:
            return "**🚀 Capabilities (Demo Mode):**\n\n**Current (Demo):**\n- ✅ Beautiful UI showcase\n- ✅ Smooth animations\n- ✅ Interactive navigation\n- ✅ Responsive design\n- ✅ Professional layout\n\n**With API Key (Production):**\n- 🤖 Real AI conversations\n- 📄 PDF document analysis\n- 🌐 Web search integration\n- 🎙️ Voice input/output\n- 💡 Context-aware responses\n- 🌍 Multilingual AI chat\n\n*Connect an API key to unlock full AI features!*"
        
        elif "thank" in user_msg or "thanks" in user_msg or "shukriya" in user_msg:
            return "You're welcome! 😊\n\nI hope you enjoyed exploring this **AI Assistant Dashboard**!\n\n**Key Highlights:**\n- 🎨 Modern SaaS design\n- ⚡ Smooth performance\n- 📱 Responsive layout\n- 🌟 Professional quality\n\nFeel free to explore all the views using the sidebar!\n\n*Happy exploring!* ✨"
        
        else:
            return f"🤖 **Demo Response**\n\nYou said: *\"{messages[-1]['content']}\"*\n\nThis is an **intelligent demo mode** showcasing the chat interface. The UI demonstrates:\n\n✨ **Design Features:**\n- Clean message bubbles\n- Smooth typing animations\n- Beautiful space theme\n- Professional layout\n\n📊 **Technical Stack:**\n- Streamlit framework\n- Custom CSS styling\n- Python backend\n- Multi-API architecture\n\n💡 **Try asking:**\n- \"Hello\" - Welcome message\n- \"Help\" - Feature guide\n- \"About project\" - Technical details\n- \"Features\" - Capability list\n\n---\n*This is a portfolio showcase demonstrating modern web development and UI/UX design skills!* 🚀"
    
    try:
        # Detect API type from key
        key = ""
        if hasattr(st, 'secrets'):
            key = (st.secrets.get("OPENROUTER_API_KEY", "") or
                   st.secrets.get("OPENAI_API_KEY", "") or 
                   st.secrets.get("GROQ_API_KEY", "") or 
                   st.secrets.get("HUGGINGFACE_API_KEY", ""))
        
        # Choose models based on API
        models = []
        if key.startswith("sk-or-"):
            # OpenRouter - supports many models
            models = [
                "meta-llama/llama-3.1-70b-instruct",
                "openai/gpt-3.5-turbo",
                "anthropic/claude-3-haiku"
            ]
        elif key.startswith("sk-proj-") or (key.startswith("sk-") and not key.startswith("sk-or-")):
            # OpenAI
            models = ["gpt-3.5-turbo", "gpt-4o-mini"]
        elif key.startswith("hf_"):
            # Hugging Face
            models = ["meta-llama/Meta-Llama-3-8B-Instruct"]
        else:
            # Groq or fallback
            models = ["llama-3.1-70b-versatile", "gpt-3.5-turbo"]
        
        response = None
        last_error = None
        
        for model in models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000,
                )
                break
            except Exception as model_error:
                last_error = str(model_error)
                continue
        
        if response:
            return response.choices[0].message.content
        else:
            return f"⚠️ Could not connect to AI service.\n\n**Error:** {last_error}\n\n**Debug:**\n- Key starts with: {key[:10]}...\n- Tried models: {models}\n\nPlease verify your API key is valid and has credits."
            
    except Exception as e:
        return f"❌ AI Error: {str(e)}\n\n**Debug Info:**\n- Check if API key is correct\n- Verify you have credits/quota\n- Try restarting the app\n\nOr switch to demo mode (remove API key)."

@st.cache_resource(show_spinner=False)
def get_rag(_h):
    return None  # Disabled for cloud deployment

def fhash():
    return ""  # Disabled

def gen_audio(text):
    return None  # Disabled for cloud deployment

def web_search(q):
    return "Web search temporarily disabled in cloud version."

LANGS = {
    "🇵🇰 Roman Urdu": "Sirf Roman Urdu mein jawab do (Urdu ko Latin mein likho). English sentences mat likho.",
    "🇵🇰 اردو":        "صرف اردو میں جواب دیں۔",
    "🇬🇧 English":     "Reply only in English.",
    "🇫🇷 French":      "Réponds uniquement en français.",
    "🇸🇦 Arabic":      "أجب فقط باللغة العربية.",
    "🇪🇸 Spanish":     "Responde únicamente en español.",
    "🇩🇪 German":      "Antworte nur auf Deutsch.",
    "🇨🇳 Chinese":     "只用中文回答。",
    "🇯🇵 Japanese":    "日本語だけで答えてください。",
}

def build_prompt(msg, ctx=""):
    lang = st.session_state.get("language","🇬🇧 English")
    instr = LANGS.get(lang,"Reply in English.")
    p  = f"### SYSTEM ###\nYou are a helpful AI assistant.\n"
    p += f"LANGUAGE (MANDATORY): {instr}\n"
    p += f"Answer thoroughly with formatting.\n### END ###\n\n"
    if ctx: p += f"[Reference]:\n{ctx}\n\n"
    p += f"[User]: {msg}\n\n[Assistant]:"
    return p

# ── Load CSS ──────────────────────────────────────────────────
with open("style.css","r",encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────
for k,v in {
    "messages":[], "notes":[], "last_audio":None,
    "tts":False, "pending":None,
    "language":"🇬🇧 English", "mode":"🧠 Free Chat",
    "view":"home",
}.items():
    if k not in st.session_state: st.session_state[k]=v

llm, llm_err = get_ai_client()

# ════════════════════════════════════════════════════════════
#  BACKGROUND CANVAS — stars + beam (inject once)
# ════════════════════════════════════════════════════════════
rng = random.Random(99)
stars = ""
for _ in range(60):
    top   = rng.uniform(3, 94)
    left  = rng.uniform(2, 97)
    sz    = rng.choice([1.3, 1.8, 2.3, 1.5, 2.6])
    dur   = round(rng.uniform(2.5, 6), 1)
    delay = round(rng.uniform(0, 5), 1)
    op    = round(rng.uniform(.4, .85), 2)
    stars += (f'<div class="bg-star" style="top:{top}%;left:{left}%;'
              f'width:{sz}px;height:{sz}px;opacity:{op};'
              f'animation-duration:{dur}s;animation-delay:{delay}s;"></div>')

st.markdown(f"""
<div class="bg-canvas">
  <div class="bg-beam"></div>
  <div class="bg-beam-halo"></div>
  <div class="bg-ground"></div>
  {stars}
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  SIDEBAR — slim vertical icon bar (LEFT EDGE ONLY)
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sb-logo">✦</div>', unsafe_allow_html=True)
    
    # Minimal icon buttons - vertical stack
    if st.button("💬", key="nav_home", help="Chat", use_container_width=True):
        st.session_state.view = "home"
        st.rerun()
    
    if st.button("🕐", key="nav_history", help="History", use_container_width=True):
        st.session_state.view = "chat"
        st.rerun()
    
    if st.button("📄", key="nav_docs", help="Documents", use_container_width=True):
        st.session_state.view = "sources"
        st.rerun()
    
    if st.button("🔍", key="nav_search", help="Search", use_container_width=True):
        st.session_state.view = "studio"
        st.rerun()
    
    if st.button("⚙", key="nav_settings", help="Settings", use_container_width=True):
        st.session_state.view = "settings"
        st.rerun()

# ════════════════════════════════════════════════════════════
#  HOME VIEW  — hero + glass input + chips
# ════════════════════════════════════════════════════════════
if st.session_state.view == "home":

    # ── Hero Section ───────────────────────────────────────────
    st.markdown("""
<div class="hero-wrap">
  <div class="hero-icon">
    <div class="hero-icon-bg"></div>
    <div class="hero-icon-ring"></div>
    <svg width="46" height="52" viewBox="0 0 46 52" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M23 3L41 15V37C41 37 32 46 23 50C14 46 5 37 5 37V15L23 3Z"
            fill="none" stroke="white" stroke-width="2"
            stroke-linejoin="round" stroke-linecap="round"/>
      <path d="M15 26L21 32L31 20"
            stroke="white" stroke-width="2.2"
            stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
  <h1 class="hero-title">How can I help you today?</h1>
</div>
""", unsafe_allow_html=True)

    # ── Dark Glass Input Card ───────────────────────────────────
    st.markdown('<div class="input-wrap"><div class="input-card-dark">', unsafe_allow_html=True)

    # Input field
    home_prompt = st.text_input(
        "What do you want to know?",
        placeholder="What do you want to know?",
        label_visibility="collapsed",
        key="home_input"
    )

    # Bottom bar: Language + Mode + Icons
    col1, col2, col3 = st.columns([2, 4, 2])
    
    with col1:
        # Language dropdown (with icon)
        st.markdown('<div style="display:flex;align-items:center;gap:8px;">', unsafe_allow_html=True)
        lang_list = list(LANGS.keys())
        cur_i = lang_list.index(st.session_state.language) if st.session_state.language in lang_list else 2
        picked = st.selectbox("", lang_list, index=cur_i, key="lang_home",
                              label_visibility="collapsed")
        if picked != st.session_state.language:
            st.session_state.language = picked
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Mode buttons with icons (horizontal radio)
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("📄 Docs", key="mode_docs", use_container_width=True):
                st.session_state.mode = "📄 Docs"
        with col_b:
            if st.button("🌐 Web", key="mode_web", use_container_width=True):
                st.session_state.mode = "🌐 Web"
        with col_c:
            if st.button("💬 Chat", key="mode_chat", use_container_width=True):
                st.session_state.mode = "💬 Chat"
    
    with col3:
        # Right side icons placeholder
        st.markdown('<div style="text-align:right;opacity:0.4;font-size:0.9rem;">⚡</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Action Chips Below Input ────────────────────────────────
    st.markdown("""
<div class="chips-row">
  <div class="a-chip"><span class="a-chip-ic">💡</span>Generate ideas</div>
  <div class="a-chip"><span class="a-chip-ic">🎬</span>Motion concept</div>
  <div class="a-chip"><span class="a-chip-ic">📊</span>Market analysis</div>
  <div class="a-chip"><span class="a-chip-ic">💬</span>Ask AI anything</div>
</div>
""", unsafe_allow_html=True)

    if home_prompt:
        st.session_state.messages.append({"role":"user","content":home_prompt})
        st.session_state.pending = home_prompt
        st.session_state.view    = "chat"
        st.rerun()

# ════════════════════════════════════════════════════════════
#  CHAT VIEW
# ════════════════════════════════════════════════════════════
elif st.session_state.view == "chat":
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

    r1, r2, r3 = st.columns([2, 6, 3])
    with r1:
        if st.button("← Home", key="go_home"): st.session_state.view="home"; st.rerun()
    with r2:
        st.markdown('<p style="text-align:center;font-size:.82rem;color:rgba(255,255,255,.45);'
                    'padding:8px 0;margin:0;">✦ AI Assistant</p>', unsafe_allow_html=True)
    with r3:
        m2 = st.radio("", ["📄 Docs","🌐 Web","🧠 Chat"],
                      horizontal=True, key="mode_chat", label_visibility="collapsed")
        st.session_state.mode = m2

    st.markdown('<hr>', unsafe_allow_html=True)

    chat_area = st.container(height=460)
    for msg in st.session_state.messages:
        with chat_area.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt2 = st.chat_input("Ask anything…", key="chat_in")

    if st.session_state.pending:
        prompt2 = st.session_state.pending
        st.session_state.pending = None

    if prompt2:
        last = st.session_state.messages[-1] if st.session_state.messages else None
        if not last or last["content"] != prompt2 or last["role"] != "user":
            st.session_state.messages.append({"role":"user","content":prompt2})
        with chat_area.chat_message("user"):
            st.markdown(prompt2)

        slot = chat_area.empty()
        slot.markdown("""<div class="typing-wrap">
  <div class="t-dots"><span></span><span></span><span></span></div>
  <div class="t-label">AI is thinking…</div>
</div>""", unsafe_allow_html=True)

        full=""; err=None; mv=st.session_state.mode
        try:
            if llm is None:
                err = llm_err if llm_err else "⚠️ AI not configured. Add GROQ_API_KEY to Streamlit secrets."
            else:
                # Build conversation history for AI
                lang = st.session_state.get("language","🇬🇧 English")
                instr = LANGS.get(lang,"Reply in English.")
                
                conv_messages = [{
                    "role": "system",
                    "content": f"You are a helpful AI assistant. {instr} Answer thoroughly with formatting."
                }]
                
                # Add conversation history
                for m in st.session_state.messages[-6:]:  # Last 6 messages for context
                    conv_messages.append({
                        "role": m["role"],
                        "content": m["content"]
                    })
                
                # Get AI response
                full = chat_with_ai(conv_messages, llm)
                slot.empty()
                with chat_area.chat_message("assistant"):
                    st.markdown(full)
                    
        except Exception as e: 
            err=f"❌ `{e}`"

        slot.empty()
        if err:
            full=err
            with chat_area.chat_message("assistant"): st.markdown(err)

        st.session_state.messages.append({"role":"assistant","content":full})
        # TTS disabled for cloud
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  SOURCES VIEW
# ════════════════════════════════════════════════════════════
elif st.session_state.view == "sources":
    st.markdown('<div class="panel-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="panel-hdr"><span class="panel-ttl">📚 Sources</span><span class="panel-bdg">FILES</span></div>', unsafe_allow_html=True)

    up = st.file_uploader("Upload PDFs", accept_multiple_files=True, type=["pdf"])
    if up:
        with st.spinner("Saving…"):
            for uf in up:
                with open(os.path.join(DATA,uf.name),"wb") as fh: fh.write(uf.getbuffer())
            get_rag.clear()
        st.success(f"✓ {len(up)} file(s) added")

    st.markdown('<div style="font-size:.7rem;color:rgba(255,255,255,.32);text-transform:uppercase;'
                'letter-spacing:.1em;margin:16px 0 8px;">✏️ Add Note</div>', unsafe_allow_html=True)
    nv = st.text_area("", placeholder="Paste text or write a note…", height=100,
                      label_visibility="collapsed", key="note_a")
    if st.button("🗒️ Save Note", key="save_n"):
        if nv.strip():
            ts=datetime.now().strftime("%H%M%S")
            with open(os.path.join(DATA,f"note_{ts}.txt"),"w",encoding="utf-8") as fh: fh.write(nv.strip())
            st.session_state.notes.append(nv.strip()); get_rag.clear(); st.rerun()
        else: st.warning("Note is empty")

    st.divider()
    all_f=[f for f in os.listdir(DATA) if not f.startswith("web_")]
    pc=sum(1 for f in all_f if f.endswith(".pdf"))
    tc=sum(1 for f in all_f if f.endswith(".txt"))
    st.markdown(f'<div style="display:flex;gap:8px;margin-bottom:12px;">'
                f'<span class="b-pill r-pill">📄 {pc} PDFs</span>'
                f'<span class="b-pill g-pill">🗒️ {tc} Notes</span></div>', unsafe_allow_html=True)

    if all_f:
        for fn in sorted(all_f):
            b='<span class="fbdg pdf">PDF</span>' if fn.endswith(".pdf") else '<span class="fbdg txt">TXT</span>'
            d=fn if len(fn)<=28 else fn[:26]+"…"
            st.markdown(f'<div class="f-row">{b}<span>{d}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:3rem 0;color:rgba(255,255,255,.18);">'
                    '<div style="font-size:2.5rem;margin-bottom:8px;">📂</div>'
                    '<div>No sources yet</div></div>', unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️ Clear All Sources", key="clr_src"):
        for fn in os.listdir(DATA):
            try: os.remove(os.path.join(DATA,fn))
            except: pass
        st.session_state.notes.clear(); get_rag.clear(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  STUDIO VIEW
# ════════════════════════════════════════════════════════════
elif st.session_state.view == "studio":
    st.markdown('<div class="panel-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="panel-hdr"><span class="panel-ttl">🎨 Studio</span><span class="panel-bdg">AI TOOLS</span></div>', unsafe_allow_html=True)

    TOOLS=[
        ("t_audio","🎙️\nAudio Overview","Create a podcast-style conversation covering all key points."),
        ("t_study","📚\nStudy Guide",   "Create: Key Topics, Core Concepts, Summary, Review Questions."),
        ("t_faq",  "💬\nFAQ",          "Generate 8-10 FAQs with detailed answers."),
        ("t_brief","📄\nBriefing Doc",  "Executive briefing: Purpose, Background, Key Findings, Recommendations."),
        ("t_time", "⏱️\nTimeline",     "Extract a chronological timeline of events."),
        ("t_flash","🃏\nFlashcards",   "Create 10 flashcards with Front and Back."),
        ("t_quiz", "❓\nQuiz",         "Generate a 5-question MCQ quiz with answers."),
        ("t_map",  "🗺️\nMind Map",    "Create a mind map with main topics and sub-topics."),
        ("t_tbl",  "📊\nData Table",   "Extract key data into a markdown table."),
    ]
    for i in range(0, len(TOOLS), 2):
        pair=TOOLS[i:i+2]; cols=st.columns(len(pair), gap="small")
        for col,(key,label,pt) in zip(cols,pair):
            with col:
                if st.button(label, key=key, use_container_width=True):
                    if llm is None: st.error("LLM not available")
                    elif key=="t_audio":
                        eng=get_rag(fhash())
                        if not eng: st.warning("Upload documents first in Sources")
                        else:
                            with st.spinner("🎙️ Generating…"):
                                try:
                                    r=eng.query(build_prompt(pt))
                                    s="".join(c for c in r.response_gen)
                                    st.session_state.messages.append({"role":"assistant","content":f"🎙️ **Audio Overview**\n\n{s}"})
                                    if EDGE_TTS:
                                        ap=gen_audio(s[:500])
                                        if ap: st.session_state.last_audio=ap
                                    st.session_state.view="chat"; st.rerun()
                                except Exception as e: st.error(f"❌ {e}")
                    else:
                        st.session_state.pending=pt; st.session_state.view="chat"; st.rerun()

    if st.session_state.last_audio and os.path.exists(st.session_state.last_audio):
        st.divider()
        st.markdown('<div style="font-size:.7rem;color:rgba(255,255,255,.3);text-transform:uppercase;'
                    'letter-spacing:.1em;margin-bottom:6px;">🎧 Latest Audio</div>', unsafe_allow_html=True)
        st.audio(st.session_state.last_audio, format="audio/mp3")
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  SETTINGS VIEW
# ════════════════════════════════════════════════════════════
elif st.session_state.view == "settings":
    st.markdown('<div class="panel-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="panel-hdr"><span class="panel-ttl">⚙️ Settings</span><span class="panel-bdg">CONFIG</span></div>', unsafe_allow_html=True)

    ll=list(LANGS.keys()); ci=ll.index(st.session_state.language) if st.session_state.language in ll else 2
    ch=st.selectbox("🌍 Reply Language", ll, index=ci, key="lang_s")
    if ch!=st.session_state.language: st.session_state.language=ch

    st.session_state.tts=st.checkbox("🔊 Auto text-to-speech", value=st.session_state.tts)

    st.divider()
    if st.button("🧹 Clear Chat History", key="clr_ch"):
        st.session_state.messages.clear(); st.session_state.view="home"; st.rerun()

    if llm is None:
        st.markdown(f'<div class="warn-b">⚠️ Ollama not running — pull '
                    f'<code>llama3.2:3b</code> + <code>nomic-embed-text</code>'
                    f'{"<br><small>"+llm_err+"</small>" if llm_err else ""}</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="ok-b">✅ Ollama connected and ready</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
