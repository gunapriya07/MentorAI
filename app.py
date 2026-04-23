import streamlit as st
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MentorAI · Smart Study Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:           #080b11;
    --surface:      #0f1319;
    --surface-2:    #161b25;
    --surface-3:    #1c2230;
    --border:       #1f2738;
    --border-light: #2a3347;
    --accent:       #c8a96e;
    --accent-dim:   #7a5f35;
    --accent-glow:  rgba(200,169,110,.12);
    --teal:         #4ecdc4;
    --text:         #eae6de;
    --text-muted:   #6e7a96;
    --text-faint:   #333d55;
    --danger:       #e05c5c;
    --r:            10px;
    --r-lg:         16px;
    --display:      'Cormorant Garamond', Georgia, serif;
    --body:         'DM Sans', sans-serif;
    --mono:         'DM Mono', monospace;
}

/* ── Shell reset ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--body) !important;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="collapsedControl"],
footer { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 99px; }

/* ── Radio pills ── */
[data-testid="stRadio"] > div {
    display: flex !important;
    gap: .55rem !important;
    flex-wrap: wrap;
}
[data-testid="stRadio"] label {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 99px !important;
    padding: .45rem 1.2rem !important;
    font-family: var(--mono) !important;
    font-size: .72rem !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    cursor: pointer !important;
    transition: all .2s !important;
}
[data-testid="stRadio"] label:has(input:checked) {
    background: var(--accent-glow) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}
[data-testid="stRadio"] label > div:first-child { display: none !important; }
[data-testid="stRadio"] > label { display: none !important; }

/* ── Textarea ── */
[data-testid="stTextArea"] textarea {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: var(--body) !important;
    font-size: .93rem !important;
    line-height: 1.7 !important;
    border-radius: var(--r) !important;
    transition: border-color .2s, box-shadow .2s !important;
    resize: vertical !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
    outline: none !important;
}
[data-testid="stTextArea"] label { display: none !important; }

/* ── All buttons base ── */
[data-testid="stButton"] > button {
    border-radius: var(--r) !important;
    font-family: var(--body) !important;
    font-weight: 600 !important;
    font-size: .82rem !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
    transition: all .2s !important;
    cursor: pointer !important;
    border: none !important;
}
/* Primary */
button[data-testid="baseButton-primary"],
[data-testid="stButton"]:has(button[kind="primary"]) > button {
    background: var(--accent) !important;
    color: #080b11 !important;
    padding: .7rem 2.2rem !important;
}
[data-testid="stButton"]:has(button[kind="primary"]) > button:hover {
    opacity: .88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(200,169,110,.28) !important;
}
/* Secondary */
button[data-testid="baseButton-secondary"],
[data-testid="stButton"]:has(button[kind="secondary"]) > button {
    background: var(--surface-2) !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border) !important;
    padding: .7rem 1.4rem !important;
}
[data-testid="stButton"]:has(button[kind="secondary"]) > button:hover {
    border-color: var(--accent-dim) !important;
    color: var(--text) !important;
}
/* Spinner */
[data-testid="stSpinner"] p {
    color: var(--text-muted) !important;
    font-family: var(--mono) !important;
    font-size: .8rem !important;
}
/* Warning */
[data-testid="stAlert"] {
    background: rgba(224,92,92,.07) !important;
    border: 1px solid rgba(224,92,92,.4) !important;
    border-radius: var(--r) !important;
    color: var(--danger) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
for k, v in {
    "page": "landing",
    "history": [],
    "current_topic": "",
    "last_response": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────
# STUB IMPORTS
# ─────────────────────────────────────────────────────────────
try:
    from utils.llm import generate_response
    from prompts.templates import get_prompt
except ImportError:
    def get_prompt(mode, text): return text
    def generate_response(prompt):
        return (
            "Placeholder response — connect your LLM backend by "
            "implementing utils.llm.generate_response and "
            "prompts.templates.get_prompt."
        )


# ═══════════════════════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════════════════════
def render_landing():

    # ── Styles (landing-only) ─────────────────────────────────
    st.markdown("""
    <style>
    .l-nav {
        display:flex; align-items:center; justify-content:space-between;
        padding:1.5rem 3.5rem;
        border-bottom:1px solid var(--border);
        background:rgba(8,11,17,.92);
        backdrop-filter:blur(14px);
        position:sticky; top:0; z-index:200;
    }
    .l-logo { font-family:var(--display); font-size:1.45rem; font-weight:400; color:var(--text); }
    .l-logo b { color:var(--accent); font-weight:600; }
    .l-nav-links { display:flex; gap:2.2rem; }
    .l-nav-links span {
        font-family:var(--mono); font-size:.7rem; letter-spacing:.18em;
        text-transform:uppercase; color:var(--text-muted);
    }

    .l-hero {
        position:relative; overflow:hidden;
        display:flex; flex-direction:column; align-items:center;
        text-align:center;
        padding:6.5rem 2rem 3rem;
    }
    .l-hero::before {
        content:''; position:absolute; inset:0; pointer-events:none;
        background:
            radial-gradient(ellipse 70% 55% at 50% -5%,  rgba(200,169,110,.1)  0%, transparent 65%),
            radial-gradient(ellipse 40% 32% at 88% 88%,  rgba(78,205,196,.06)  0%, transparent 60%),
            radial-gradient(ellipse 28% 22% at 8%  72%,  rgba(200,169,110,.04) 0%, transparent 60%);
    }
    .l-orb {
        position:absolute; border-radius:50%;
        filter:blur(70px); pointer-events:none; opacity:.3;
    }
    .l-orb-1 { width:360px; height:360px; top:-100px; left:calc(50% - 180px); background:radial-gradient(circle,rgba(200,169,110,.3),transparent 70%); }
    .l-orb-2 { width:220px; height:220px; bottom:40px; right:6%; background:radial-gradient(circle,rgba(78,205,196,.22),transparent 70%); }

    .l-eyebrow {
        font-family:var(--mono); font-size:.7rem; letter-spacing:.28em;
        text-transform:uppercase; color:var(--accent);
        background:var(--accent-glow); border:1px solid var(--accent-dim);
        border-radius:99px; padding:.35rem 1.1rem;
        margin-bottom:2rem; display:inline-block;
        animation:fu .6s ease both;
    }
    .l-h1 {
        font-family:var(--display); font-size:clamp(3.2rem,6.5vw,6.8rem);
        font-weight:300; line-height:1.04; color:var(--text);
        max-width:880px; margin:0 auto 1.4rem;
        animation:fu .7s .08s ease both;
    }
    .l-h1 em { font-style:italic; color:var(--accent); }
    .l-sub {
        font-size:1.05rem; font-weight:300; color:var(--text-muted);
        max-width:490px; line-height:1.78; margin:0 auto 2.6rem;
        animation:fu .7s .16s ease both;
    }
    /* cta wrapper — makes button appear below subtitle */
    .cta-anchor { animation:fu .7s .24s ease both; }

    .l-badges {
        display:flex; gap:.7rem; justify-content:center; flex-wrap:wrap;
        margin-top:2.4rem; padding-bottom:5.5rem;
        animation:fu .7s .38s ease both;
    }
    .l-badge {
        font-family:var(--mono); font-size:.64rem; letter-spacing:.14em;
        text-transform:uppercase; color:var(--text-faint);
        border:1px solid var(--border-light); border-radius:99px; padding:.3rem .9rem;
    }

    /* Features */
    .l-sec { padding:5.5rem 5rem; }
    .l-sec-alt { background:var(--surface); border-top:1px solid var(--border); border-bottom:1px solid var(--border); }
    .l-tag  { font-family:var(--mono); font-size:.68rem; letter-spacing:.22em; text-transform:uppercase; color:var(--accent); margin-bottom:.7rem; }
    .l-h2   { font-family:var(--display); font-size:clamp(2rem,3vw,3rem); font-weight:300; color:var(--text); margin-bottom:3rem; }

    .feat-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:1.2rem; max-width:1100px; }
    .feat-card {
        background:var(--surface-2); border:1px solid var(--border);
        border-radius:var(--r-lg); padding:1.8rem 1.6rem;
        transition:border-color .25s, transform .25s, box-shadow .25s;
    }
    .feat-card:hover { border-color:var(--accent-dim); transform:translateY(-5px); box-shadow:0 16px 40px rgba(0,0,0,.4); }
    .feat-num  { font-family:var(--mono); font-size:.65rem; color:var(--accent); letter-spacing:.15em; margin-bottom:1rem; }
    .feat-name { font-family:var(--display); font-size:1.4rem; font-weight:400; color:var(--text); margin-bottom:.5rem; }
    .feat-desc { font-size:.84rem; color:var(--text-muted); line-height:1.7; }

    .how-inner { max-width:820px; }
    .step { display:flex; gap:2.2rem; align-items:flex-start; padding:1.6rem 0; border-top:1px solid var(--border); }
    .step-n { font-family:var(--display); font-size:2.8rem; font-weight:300; color:var(--text-faint); min-width:2.8rem; line-height:1; }
    .step-h { font-family:var(--display); font-size:1.3rem; font-weight:400; color:var(--text); margin-bottom:.3rem; }
    .step-p { font-size:.84rem; color:var(--text-muted); line-height:1.65; }

    .l-footer {
        padding:2rem 3.5rem;
        border-top:1px solid var(--border);
        display:flex; align-items:center; justify-content:space-between;
    }
    .l-footer-brand { font-family:var(--display); font-size:1.1rem; color:var(--text-muted); }
    .l-footer-brand b { color:var(--accent); }
    .l-footer-copy { font-family:var(--mono); font-size:.65rem; letter-spacing:.08em; color:var(--text-faint); }

    @keyframes fu { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
    </style>

    <!-- NAV -->
    <nav class="l-nav">
        <div class="l-logo">Mentor<b>AI</b></div>
        <div class="l-nav-links">
            <span>Features</span>
            <span>How it works</span>
            <span>About</span>
        </div>
    </nav>

    <!-- HERO top (eyebrow + headline + subtitle) -->
    <section class="l-hero">
        <div class="l-orb l-orb-1"></div>
        <div class="l-orb l-orb-2"></div>
        <div class="l-eyebrow">AI-Powered Study Assistant</div>
        <h1 class="l-h1">
            Learn anything.<br><em>Master everything.</em>
        </h1>
        <p class="l-sub">
            Explain complex concepts, compress your notes, and quiz yourself —
            all powered by AI that remembers your session context.
        </p>
    </section>
    """, unsafe_allow_html=True)

    # ══ TRY NOW BUTTON — rendered HERE so it lands in the hero ══
    st.markdown('<div class="cta-anchor" style="display:flex;justify-content:center;margin-top:-3.2rem;position:relative;z-index:10;">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([3.2, 1, 3.2])
    with c2:
        if st.button("Try Now", key="hero_cta", use_container_width=True, type="primary"):
            st.session_state.page = "dashboard"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Badges + rest of page ─────────────────────────────────
    st.markdown("""
    <div class="l-badges">
        <span class="l-badge">Explain Mode</span>
        <span class="l-badge">Summarize Mode</span>
        <span class="l-badge">Quiz Mode</span>
        <span class="l-badge">Session Memory</span>
    </div>

    <!-- FEATURES -->
    <div class="l-sec l-sec-alt">
        <div class="l-tag">Core Capabilities</div>
        <div class="l-h2">Everything you need to master any subject</div>
        <div class="feat-grid">
            <div class="feat-card">
                <div class="feat-num">01</div>
                <div class="feat-name">Deep Explanation</div>
                <div class="feat-desc">Break intricate concepts into clear, layered explanations with examples tailored to your level.</div>
            </div>
            <div class="feat-card">
                <div class="feat-num">02</div>
                <div class="feat-name">Smart Summarization</div>
                <div class="feat-desc">Compress lengthy documents, lecture notes, or chapters into precise, actionable summaries.</div>
            </div>
            <div class="feat-card">
                <div class="feat-num">03</div>
                <div class="feat-name">Adaptive Quizzing</div>
                <div class="feat-desc">Reinforce retention with context-aware questions generated directly from your study material.</div>
            </div>
            <div class="feat-card">
                <div class="feat-num">04</div>
                <div class="feat-name">Session Memory</div>
                <div class="feat-desc">Every response is logged. Review your full history and pick up exactly where you left off.</div>
            </div>
        </div>
    </div>

    <!-- HOW IT WORKS -->
    <div class="l-sec">
        <div class="how-inner">
            <div class="l-tag">Process</div>
            <div class="l-h2">Three steps to mastery</div>
            <div class="step">
                <div class="step-n">01</div>
                <div>
                    <div class="step-h">Choose your mode</div>
                    <div class="step-p">Select Explain, Summarize, or Quiz depending on where you are in your study cycle.</div>
                </div>
            </div>
            <div class="step">
                <div class="step-n">02</div>
                <div>
                    <div class="step-h">Enter your content</div>
                    <div class="step-p">Paste a topic, paragraph, or question. The assistant retains context across your entire session.</div>
                </div>
            </div>
            <div class="step">
                <div class="step-n">03</div>
                <div>
                    <div class="step-h">Review and iterate</div>
                    <div class="step-p">Read the AI response, follow up with deeper questions, and revisit everything in your history log.</div>
                </div>
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <div class="l-footer">
        <div class="l-footer-brand">Mentor<b>AI</b></div>
        <div class="l-footer-copy">Built for learners who take their craft seriously.</div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════
def render_dashboard():
    st.markdown("""
    <style>
    /* ── Top bar ── */
    .db-bar {
        display:flex; align-items:center; justify-content:space-between;
        padding:.95rem 2.4rem;
        border-bottom:1px solid var(--border);
        background:rgba(8,11,17,.96);
        backdrop-filter:blur(14px);
        position:sticky; top:0; z-index:200;
    }
    .db-logo { font-family:var(--display); font-size:1.35rem; font-weight:400; color:var(--text); }
    .db-logo b { color:var(--accent); }
    .db-bar-right { display:flex; gap:1rem; align-items:center; }
    .db-pill {
        font-family:var(--mono); font-size:.62rem; letter-spacing:.12em;
        text-transform:uppercase; color:var(--text-muted);
        background:var(--surface-2); border:1px solid var(--border);
        border-radius:99px; padding:.28rem .85rem;
    }
    .db-pill b { color:var(--accent); }

    /* ── Left panel ── */
    .lp-head { padding:1.8rem 1.8rem 0; }
    .lp-eyebrow { font-family:var(--mono); font-size:.62rem; letter-spacing:.2em; text-transform:uppercase; color:var(--text-muted); margin-bottom:.4rem; }
    .lp-title { font-family:var(--display); font-size:2.1rem; font-weight:300; color:var(--text); margin-bottom:1.5rem; }

    .lp-body { padding:0 1.8rem 1.8rem; }

    /* mode selector label */
    .field-label { font-family:var(--mono); font-size:.62rem; letter-spacing:.18em; text-transform:uppercase; color:var(--text-muted); margin-bottom:.55rem; }

    /* ── Response card ── */
    .resp-wrap { padding:0 1.8rem 2rem; }
    .resp-card {
        background:var(--surface); border:1px solid var(--border);
        border-radius:var(--r-lg); overflow:hidden;
        animation:dbFu .4s ease both;
    }
    .resp-card-header {
        display:flex; align-items:center; justify-content:space-between;
        padding:1rem 1.4rem; border-bottom:1px solid var(--border);
        background:var(--surface-2);
    }
    .resp-tag {
        font-family:var(--mono); font-size:.6rem; letter-spacing:.14em;
        text-transform:uppercase; color:var(--accent);
        background:var(--accent-glow); border:1px solid var(--accent-dim);
        border-radius:99px; padding:.2rem .72rem;
    }
    .resp-ts { font-family:var(--mono); font-size:.6rem; color:var(--text-faint); }
    .resp-body { padding:1.5rem 1.4rem; }
    .resp-text { font-size:.93rem; color:var(--text); line-height:1.84; white-space:pre-wrap; }

    /* empty placeholder */
    .empty-box {
        border:1px dashed var(--border-light); border-radius:var(--r-lg);
        padding:3.5rem 2rem; text-align:center;
        font-family:var(--display); font-style:italic;
        color:var(--text-faint); font-size:.95rem;
    }

    /* ── Right panel ── */
    .rp-wrap { padding:1.8rem 1.4rem 1rem; }
    .rp-title { font-family:var(--display); font-size:1.6rem; font-weight:300; color:var(--text); }
    .rp-sub   { font-family:var(--mono); font-size:.62rem; letter-spacing:.1em; text-transform:uppercase; color:var(--text-muted); margin-top:.15rem; margin-bottom:1.2rem; }
    .rp-divider { border:none; border-top:1px solid var(--border); margin:0 0 1.1rem; }

    /* stats */
    .stats-row { display:grid; grid-template-columns:repeat(3,1fr); gap:.65rem; margin-bottom:1.1rem; }
    .stat-box  { background:var(--surface-2); border:1px solid var(--border); border-radius:var(--r); padding:.85rem .8rem; }
    .stat-val  { font-family:var(--display); font-size:1.75rem; font-weight:300; color:var(--accent); line-height:1; }
    .stat-key  { font-family:var(--mono); font-size:.58rem; letter-spacing:.12em; text-transform:uppercase; color:var(--text-muted); margin-top:.22rem; }

    /* history */
    .hist-scroll { max-height:55vh; overflow-y:auto; padding-right:4px; }
    .hi {
        border:1px solid var(--border); border-radius:var(--r);
        padding:.95rem 1rem; margin-bottom:.65rem;
        background:var(--surface-2);
        transition:border-color .2s, transform .15s;
    }
    .hi:hover { border-color:var(--accent-dim); transform:translateX(3px); }
    .hi-top  { display:flex; justify-content:space-between; align-items:center; margin-bottom:.4rem; }
    .hi-pill { font-family:var(--mono); font-size:.58rem; letter-spacing:.12em; text-transform:uppercase; color:var(--accent); border:1px solid var(--accent-dim); border-radius:99px; padding:.14rem .55rem; }
    .hi-num  { font-family:var(--mono); font-size:.58rem; color:var(--text-faint); }
    .hi-q    { font-size:.81rem; color:var(--text); font-weight:500; margin-bottom:.32rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .hi-a    { font-size:.76rem; color:var(--text-muted); line-height:1.55; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }

    .empty-hist {
        text-align:center; padding:3rem 1rem;
        font-family:var(--display); font-style:italic;
        color:var(--text-faint); font-size:.9rem;
        border:1px dashed var(--border); border-radius:var(--r-lg);
    }

    @keyframes dbFu { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
    </style>
    """, unsafe_allow_html=True)

    total  = len(st.session_state.history)
    exp_c  = sum(1 for h in st.session_state.history if h["mode"] == "Explain")
    quiz_c = sum(1 for h in st.session_state.history if h["mode"] == "Quiz")

    # ── Top bar ──
    st.markdown(
f"""<div class="db-bar">
<div class="db-logo">Mentor<b>AI</b></div>
<div class="db-bar-right">
<span class="db-pill">Session &middot; <b>{total}</b> generations</span>
</div>
</div>""", unsafe_allow_html=True)

    # ── Two columns ──
    left, right = st.columns([1.62, 1], gap="medium")

    # ═══════════════ LEFT ═══════════════
    with left:
        st.markdown("""
        <div class="lp-head">
            <div class="lp-eyebrow">Input Panel</div>
            <div class="lp-title">What are we studying today?</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="lp-body">', unsafe_allow_html=True)

        st.markdown('<div class="field-label">Study Mode</div>', unsafe_allow_html=True)
        mode = st.radio("mode", ["Explain", "Summarize", "Quiz"],
                        horizontal=True, label_visibility="collapsed",
                        key="mode_radio")

        st.markdown('<div style="height:.9rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="field-label">Topic or Content</div>', unsafe_allow_html=True)
        user_input = st.text_area(
            "input",
            placeholder="Paste a paragraph, enter a topic, or type your question...",
            height=195,
            label_visibility="collapsed",
            key="user_input",
        )

        st.markdown('<div style="height:.75rem;"></div>', unsafe_allow_html=True)

        bc1, bc2, bc3 = st.columns([1.5, 1, 2.2])
        with bc1:
            generate = st.button("Generate", key="gen_btn",
                                 use_container_width=True, type="primary")
        with bc2:
            if st.button("Clear All", key="clear_btn",
                         use_container_width=True, type="secondary"):
                st.session_state.history = []
                st.session_state.current_topic = ""
                st.session_state.last_response = ""
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<hr style="border:none;border-top:1px solid var(--border);margin:0 1.8rem;">', unsafe_allow_html=True)

        # ── Generate logic ──
        if generate:
            if not user_input.strip():
                st.markdown('<div style="padding:.8rem 1.8rem 0;">', unsafe_allow_html=True)
                st.warning("Please enter a topic or content before generating.")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                with st.spinner("Generating response..."):
                    st.session_state.current_topic = user_input
                    base_prompt = get_prompt(mode, user_input)
                    full_prompt = f"""You are a helpful AI study assistant.

Current Mode: {mode}
Current Topic: {st.session_state.current_topic}

Last Response:
{st.session_state.last_response}

Now respond based on the above context.

User Input:
{base_prompt}

If the question refers to previous content, use the last response. If unsure, say you don't know."""
                    result = generate_response(full_prompt)
                    st.session_state.last_response = result
                    st.session_state.history.append({
                        "mode": mode,
                        "input": user_input,
                        "output": result,
                        "time": datetime.now().strftime("%H:%M"),
                    })

        # ── Response area ──
        if st.session_state.last_response:
            last = st.session_state.history[-1]
            t = last.get("time", "")
            st.markdown(
f"""<div class="resp-wrap">
<div class="field-label" style="margin:1.4rem 0 .7rem;">Latest Response</div>
<div class="resp-card">
<div class="resp-card-header">
<span class="resp-tag">{last['mode']}</span>
<span class="resp-ts">{t}</span>
</div>
<div class="resp-body">
<div class="resp-text">{last['output']}</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding:1.5rem 1.8rem 2rem;">
                <div class="empty-box">
                    Your AI response will appear here after you generate.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ═══════════════ RIGHT ═══════════════
    with right:
        st.markdown(
f"""<div class="rp-wrap">
<div class="rp-title">Study History</div>
<div class="rp-sub">Session Activity Log</div>
<hr class="rp-divider">
<div class="stats-row">
<div class="stat-box"><div class="stat-val">{total}</div><div class="stat-key">Total</div></div>
<div class="stat-box"><div class="stat-val">{exp_c}</div><div class="stat-key">Explained</div></div>
<div class="stat-box"><div class="stat-val">{quiz_c}</div><div class="stat-key">Quizzed</div></div>
</div>
</div>""",
            unsafe_allow_html=True,
        )

        history = st.session_state.history
        if not history:
            st.markdown("""
            <div style="padding:0 1.4rem;">
                <div class="empty-hist">No activity yet.<br>Generate something to begin.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="padding:0 1.4rem;"><div class="hist-scroll">', unsafe_allow_html=True)
            for i, item in enumerate(reversed(history)):
                idx = len(history) - i
                q   = item['input'][:74] + "..." if len(item['input']) > 74 else item['input']
                a   = item['output'][:145] + "..." if len(item['output']) > 145 else item['output']
                t   = item.get("time", "")
                st.markdown(
f"""<div class="hi">
<div class="hi-top">
<span class="hi-pill">{item['mode']}</span>
<span class="hi-num">#{idx} &middot; {t}</span>
</div>
<div class="hi-q">{q}</div>
<div class="hi-a">{a}</div>
</div>""", unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown('<div style="padding:.6rem 1.4rem 1.5rem;">', unsafe_allow_html=True)
        if st.button("Back to Home", key="back_home",
                     use_container_width=True, type="secondary"):
            st.session_state.page = "landing"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────
if st.session_state.page == "landing":
    render_landing()
else:
    render_dashboard()