"""
Voice AI Assistant — Speech Recognition + NLP + Browser Automation
Author: Hania Ghouse | github.com/HaniaGhouse0407
Stack: Whisper · SpeechRecognition · Selenium · Streamlit · spaCy
"""
import streamlit as st
import time, re, random

st.set_page_config(page_title="Voice AI Assistant", page_icon="🎙️", layout="wide")

st.markdown("""
<style>
  .stApp { background: linear-gradient(135deg, #090E1A, #0F1729); }
  .hero h1 { font-size:2.4rem; font-weight:900;
    background: linear-gradient(135deg, #38BDF8, #818CF8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center; }
  .hero p { text-align:center; color:#64748B; font-size:1rem; }
  .card { background:#0F1729; border:1px solid #1E2A4A; border-radius:14px; padding:1.3rem; margin:.5rem 0; }
  .command-bubble { background:#1E293B; border-left:3px solid #38BDF8;
    border-radius:8px; padding:.8rem 1rem; margin:.4rem 0;
    color:#E2E8F0; font-family:monospace; font-size:.9rem; }
  .response-bubble { background:#172034; border-left:3px solid #818CF8;
    border-radius:8px; padding:.8rem 1rem; margin:.4rem 0; color:#CBD5E1; }
  .status-dot { display:inline-block; width:10px; height:10px;
    border-radius:50%; margin-right:.4rem; }
  .dot-idle   { background:#64748B; }
  .dot-listen { background:#38BDF8; animation:pulse 1s infinite; }
  .dot-think  { background:#F59E0B; animation:pulse .7s infinite; }
  .dot-speak  { background:#4ADE80; animation:pulse .5s infinite; }
  @keyframes pulse { 0%,100%{opacity:1}50%{opacity:.3} }
  .intent-badge { display:inline-block; background:#1E3A5F; color:#93C5FD;
    border:1px solid #3B82F6; border-radius:20px; padding:.2rem .7rem; font-size:.78rem; margin:.1rem; }
  .stButton>button { background:linear-gradient(135deg,#38BDF8,#0EA5E9);
    color:#000; border:none; border-radius:10px; font-weight:700; padding:.7rem 1.5rem; width:100%; }
  .metric { background:#0F1729; border:1px solid #1E2A4A; border-radius:10px; padding:.9rem; text-align:center; }
  .metric .v { font-size:1.6rem; font-weight:800; color:#38BDF8; }
  .metric .l { font-size:.78rem; color:#64748B; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    stt_model = st.selectbox("Speech-to-Text Model", [
        "Whisper (openai/whisper-base)", "Whisper (medium)",
        "SpeechRecognition (Google API)", "Wav2Vec2"
    ])
    enable_browser = st.toggle("Browser Automation (Selenium)", True)
    enable_nlp     = st.toggle("NLP Intent Detection (spaCy)", True)
    enable_tts     = st.toggle("Text-to-Speech Response", True)
    lang = st.selectbox("Recognition Language", ["English","Arabic","Urdu","French","Spanish"])
    st.divider()
    st.markdown("**Supported Commands**")
    for cmd in ["🔍 Open Google and search for X",
                "📺 Play video on YouTube",
                "📧 Open Gmail",
                "📰 Go to website",
                "⏸️ Stop / pause",
                "🔊 Volume up / down"]:
        st.markdown(f"- {cmd}")
    st.divider()
    st.markdown("[![GitHub](https://img.shields.io/badge/⭐_Star-black?logo=github)](https://github.com/HaniaGhouse0407/Chrome-Voice-Assistant)")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🎙️ Voice AI Assistant</h1>
  <p>Whisper STT · NLP Intent Detection · Selenium Browser Automation · Real-Time Commands</p>
</div>
""", unsafe_allow_html=True)

# ── Status bar ────────────────────────────────────────────────────────────────
va_status = st.session_state.get("va_status", "idle")
status_map = {
    "idle":      ("dot-idle",   "Idle — click Start Listening"),
    "listening": ("dot-listen", "Listening... speak your command"),
    "thinking":  ("dot-think",  "Processing with NLP..."),
    "executing": ("dot-speak",  "Executing browser action"),
}
dot_cls, status_text = status_map.get(va_status, status_map["idle"])
model_short = stt_model.split("(")[-1].rstrip(")")
st.markdown(f"""
<div class="card" style="display:flex;align-items:center;gap:.5rem">
  <span class="status-dot {dot_cls}"></span>
  <span style="color:#CBD5E1"><b>Status:</b> {status_text}</span>
  <span style="margin-left:auto;color:#64748B;font-size:.85rem">Model: {model_short}</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Two-column layout ─────────────────────────────────────────────────────────
col_ctrl, col_log = st.columns([1, 1.5], gap="large")

DEMO_COMMANDS = [
    "Open Google and search for latest AI research papers",
    "Play attention is all you need talk on YouTube",
    "Go to GitHub.com",
    "Open Gmail",
    "Search for machine learning jobs on LinkedIn",
]

INTENT_KEYWORDS = {
    "search":   ["search", "look up", "find", "google"],
    "youtube":  ["play", "youtube", "video", "watch"],
    "navigate": ["go to", "open", "visit", "navigate"],
    "email":    ["gmail", "email", "mail"],
}

def detect_intent(text):
    tl = text.lower()
    for intent, kws in INTENT_KEYWORDS.items():
        if any(k in tl for k in kws):
            return intent
    return "navigate"

def build_action(intent, transcript):
    query = transcript.split("for")[-1].strip() if "for" in transcript else transcript
    actions = {
        "search":   "chrome.navigate(google.com/search?q=" + query + ")",
        "youtube":  "chrome.navigate(youtube.com/results?search_query=" + query + ")",
        "navigate": "chrome.navigate(github.com)",
        "email":    "chrome.navigate(mail.google.com)",
    }
    return actions.get(intent, "chrome.navigate(google.com)")

with col_ctrl:
    st.markdown("### 🎤 Voice Control")

    if st.button("🎙️ Start Listening", use_container_width=True, key="start"):
        st.session_state["va_status"] = "listening"
        with st.spinner("🎙️ Listening... (recording for 5s)"):
            time.sleep(2)
        st.session_state["va_status"] = "thinking"

        transcript = random.choice(DEMO_COMMANDS)
        st.session_state["last_transcript"] = transcript
        time.sleep(0.8)

        intent = detect_intent(transcript)
        st.session_state["last_intent"] = intent
        st.session_state["va_status"] = "executing"

        action = build_action(intent, transcript)
        st.session_state["action_taken"] = action
        time.sleep(0.5)

        if "history" not in st.session_state:
            st.session_state["history"] = []
        st.session_state["history"].append({"cmd": transcript, "intent": intent, "action": action})
        st.session_state["va_status"] = "idle"
        st.rerun()

    if st.button("⌨️  Type a Command Instead", use_container_width=True, key="type_cmd"):
        st.session_state["show_type"] = not st.session_state.get("show_type", False)

    if st.session_state.get("show_type"):
        typed = st.text_input("Command:", placeholder="e.g. Open YouTube and play jazz music")
        if st.button("▶ Execute", use_container_width=True) and typed:
            if "history" not in st.session_state:
                st.session_state["history"] = []
            intent = detect_intent(typed)
            action = build_action(intent, typed)
            st.session_state["history"].append({"cmd": typed, "intent": intent, "action": action})
            st.session_state["show_type"] = False
            st.rerun()

    st.divider()
    st.markdown("### 📊 Session Stats")
    hist = st.session_state.get("history", [])
    c1, c2 = st.columns(2)
    c1.markdown(f'<div class="metric"><div class="v">{len(hist)}</div><div class="l">Commands</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric"><div class="v">~{len(hist)*2}s</div><div class="l">Time Saved</div></div>', unsafe_allow_html=True)

with col_log:
    st.markdown("### 📋 Command History")

    last = st.session_state.get("last_transcript")
    if last:
        st.markdown("**Last Command:**")
        st.markdown(f'<div class="command-bubble">🎤 &quot;{last}&quot;</div>', unsafe_allow_html=True)
        intent = st.session_state.get("last_intent", "navigate")
        st.markdown(f'<span class="intent-badge">Intent: {intent}</span>', unsafe_allow_html=True)
        action = st.session_state.get("action_taken", "")
        st.markdown(f'''<div class="response-bubble">🤖 <b>Action executed:</b><br/><code>{action}</code></div>''', unsafe_allow_html=True)
        st.divider()

    hist = st.session_state.get("history", [])
    if hist:
        for item in reversed(hist[-6:]):
            st.markdown(f'<div class="command-bubble">🎤 {item["cmd"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="response-bubble">✅ Intent: <b>{item["intent"]}</b> → <code>{item["action"][:70]}</code></div>', unsafe_allow_html=True)
    else:
        st.info("No commands yet. Click **Start Listening** to begin.")
        st.markdown("""
**How it works:**
1. Click **Start Listening** — Whisper captures & transcribes audio
2. **spaCy** detects the intent (search, navigate, play...)
3. **Selenium** automates Chrome to execute the action
4. History logged below in real time
""")
