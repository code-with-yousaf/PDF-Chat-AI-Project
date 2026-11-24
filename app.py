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
try:    import edge_tts, asyncio;  EDGE_TTS = True
except: EDGE_TTS = False
try:    from duckduckgo_search import DDGS; DDGS_OK = True
except: DDGS_OK = False
try:
    from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
    from llama_index.llms.ollama import Ollama
    from llama_index.embeddings.ollama import OllamaEmbedding
    LLAMA_OK = True
except: LLAMA_OK = False

os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"
DATA = "data"; os.makedirs(DATA, exist_ok=True)

@st.cache_resource(show_spinner=False)
def load_llm():
    if not LLAMA_OK: return None, "llama_index not installed"
    try:
        llm = Ollama(model="llama3.2:3b", request_timeout=300.0)
        emb = OllamaEmbedding(model_name="nomic-embed-text")
        Settings.llm = llm; Settings.embed_model = emb
        return llm, None
    except Exception as e: return None, str(e)

@st.cache_resource(show_spinner=False)
def get_rag(_h):
    if not LLAMA_OK: return None
    srcs = [f for f in os.listdir(DATA) if f.endswith((".pdf",".txt"))]
    if not srcs: return None
    try:
        docs = SimpleDirectoryReader(DATA, required_exts=[".pdf",".txt"]).load_data()
        return VectorStoreIndex.from_documents(docs).as_query_engine(streaming=True)
    except: return None

def fhash():
    return str(sorted((f, os.path.getsize(os.path.join(DATA,f)))
               for f in os.listdir(DATA) if f.endswith((".pdf",".txt"))))

def gen_audio(text):
    if not EDGE_TTS: return None
    fname = f"sp_{''.join(random.choices(string.ascii_lowercase,k=5))}.mp3"
    errs=[]
    def _r():
        try:
            loop=asyncio.new_event_loop(); asyncio.set_event_loop(loop)
            loop.run_until_complete(edge_tts.Communicate(text,"en-US-ChristopherNeural").save(fname))
            loop.close()
        except Exception as e: errs.append(e)
    t=threading.Thread(target=_r,daemon=True); t.start(); t.join(timeout=30)
    return fname if not errs and os.path.exists(fname) else None

def web_search(q):
    if not DDGS_OK: return "DuckDuckGo not installed."
    try:
        with DDGS() as d: return "\n\n".join(r["body"] for r in d.text(q,max_results=4))
    except Exception as e: return f"Search failed: {e}"

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

llm, llm_err = load_llm()

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
#  SIDEBAR — slim icon rail (exact match)
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sb-logo">✦</div>', unsafe_allow_html=True)

    NAV = [
        ("home",    "＋",  "New Chat"),
        ("sources", "⊡",   "Sources"),
        ("studio",  "⠿",   "Studio"),
        ("settings","⚙",   "Settings"),
    ]
    for vk, ic, lb in NAV:
        if st.button(ic, key=f"nav_{vk}", help=lb, use_container_width=True):
            st.session_state.view = vk
            st.rerun()

    # dots at bottom like image
    st.markdown("""
<div style="position:absolute;bottom:24px;left:50%;transform:translateX(-50%);
display:flex;flex-direction:column;align-items:center;gap:5px;">
  <div style="width:4px;height:4px;border-radius:50%;background:rgba(255,255,255,.2);"></div>
  <div style="width:4px;height:4px;border-radius:50%;background:rgba(255,255,255,.2);"></div>
  <div style="width:4px;height:4px;border-radius:50%;background:rgba(255,255,255,.2);"></div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  HOME VIEW  — hero + glass input + chips
# ════════════════════════════════════════════════════════════
if st.session_state.view == "home":

    # ── Hero ──────────────────────────────────────────────
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
  <h1 class="hero-title">How can i help you today?</h1>
</div>
""", unsafe_allow_html=True)

    # ── Glass input card ───────────────────────────────────
    st.markdown('<div class="input-wrap"><div class="input-card">', unsafe_allow_html=True)

    home_prompt = st.chat_input("What do you want to know ?", key="home_chat")

    # Card bottom bar
    cb1, cb2, cb3 = st.columns([3, 5, 3])
    with cb1:
        lang_list = list(LANGS.keys())
        cur_i = lang_list.index(st.session_state.language) if st.session_state.language in lang_list else 2
        picked = st.selectbox("", lang_list, index=cur_i, key="lang_home",
                              label_visibility="collapsed")
        if picked != st.session_state.language:
            st.session_state.language = picked
    with cb2:
        mode_pick = st.radio("", ["📄 Docs", "🌐 Web", "🧠 Chat"],
                             horizontal=True, key="mode_home",
                             label_visibility="collapsed")
        st.session_state.mode = mode_pick
    with cb3:
        pass   # icons placeholder

    st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Action chips ───────────────────────────────────────
    st.markdown("""
<div class="chips-row">
  <div class="a-chip"><span class="a-chip-ic">✉️</span>Generate ideas</div>
  <div class="a-chip"><span class="a-chip-ic">⚡</span>Motion concept</div>
  <div class="a-chip"><span class="a-chip-ic">📈</span>Market analysis</div>
  <div class="a-chip"><span class="a-chip-ic">❓</span>Ask AI anything</div>
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
                err="⚠️ Ollama not running. Start Ollama & pull `llama3.2:3b` + `nomic-embed-text`."
            elif "Docs" in mv:
                eng=get_rag(fhash())
                if eng:
                    r=eng.query(build_prompt(prompt2)); slot.empty()
                    with chat_area.chat_message("assistant"):
                        ph=st.empty()
                        for chunk in r.response_gen: full+=chunk; ph.markdown(full+"▌")
                        ph.markdown(full)
                else: err="📭 No docs. Upload PDFs in Sources first."
            elif "Web" in mv:
                slot.markdown('<div class="spin-c"><div class="spin-i"></div><div><div class="spin-t">Searching…</div></div></div>', unsafe_allow_html=True)
                ctx=web_search(prompt2)
                slot.markdown('<div class="spin-c"><div class="spin-i"></div><div><div class="spin-t">Generating…</div></div></div>', unsafe_allow_html=True)
                full=Settings.llm.complete(build_prompt(prompt2,ctx)).text; slot.empty()
                with chat_area.chat_message("assistant"): st.markdown(full)
            else:
                full=Settings.llm.complete(build_prompt(prompt2)).text; slot.empty()
                with chat_area.chat_message("assistant"): st.markdown(full)
        except Exception as e: err=f"❌ `{e}`"

        slot.empty()
        if err:
            full=err
            with chat_area.chat_message("assistant"): st.markdown(err)

        st.session_state.messages.append({"role":"assistant","content":full})
        if st.session_state.tts and EDGE_TTS and len(full)>10:
            ap=gen_audio(full[:400])
            if ap: st.session_state.last_audio=ap
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
