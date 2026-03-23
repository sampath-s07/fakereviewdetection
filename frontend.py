"""
frontend.py – FakeShield ULTRA UI
====================================
Run:  streamlit run frontend.py
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import plotly.graph_objects as go

from backend import train_model, predict

st.set_page_config(
    page_title="FakeShield · Review Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  MEGA CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ── Reset ── */
*, html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif !important; margin:0; padding:0; box-sizing:border-box; }

/* ── Base ── */
.stApp { background: #020008; min-height: 100vh; overflow-x: hidden; }

/* ── Animated space background ── */
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: -3; pointer-events: none;
    background:
        radial-gradient(ellipse 100% 80% at 10%  5%,  rgba(111, 30,255,.28) 0%, transparent 50%),
        radial-gradient(ellipse  80% 65% at 90% 10%,  rgba(255, 20,100,.22) 0%, transparent 50%),
        radial-gradient(ellipse  70% 70% at 50% 95%,  rgba(  0,200,255,.18) 0%, transparent 50%),
        radial-gradient(ellipse  55% 50% at  5% 80%,  rgba(255,100,  0,.14) 0%, transparent 50%),
        radial-gradient(ellipse  45% 45% at 95% 85%,  rgba( 50,255,150,.12) 0%, transparent 50%),
        #020008;
    animation: bgShift 18s ease-in-out infinite alternate;
}
@keyframes bgShift {
    0%   { filter: hue-rotate(0deg)   brightness(1)    saturate(1.2); }
    50%  { filter: hue-rotate(20deg)  brightness(1.12) saturate(1.4); }
    100% { filter: hue-rotate(-10deg) brightness(1.05) saturate(1.3); }
}

/* ── Cyber grid overlay ── */
.stApp::after {
    content: '';
    position: fixed; inset: 0; z-index: -2; pointer-events: none;
    background-image:
        linear-gradient(rgba(111,30,255,.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(111,30,255,.06) 1px, transparent 1px);
    background-size: 50px 50px;
    animation: gridPulse 8s ease-in-out infinite alternate;
}
@keyframes gridPulse { 0% { opacity:.5; } 100% { opacity:1; } }

/* ── Floating particles ── */
.particles { position:fixed; inset:0; z-index:-1; pointer-events:none; overflow:hidden; }
.particle {
    position: absolute; border-radius: 50%;
    animation: floatParticle linear infinite;
    opacity: 0;
}
@keyframes floatParticle {
    0%   { transform: translateY(100vh) scale(0);   opacity: 0; }
    10%  { opacity: .7; }
    90%  { opacity: .4; }
    100% { transform: translateY(-20vh) scale(1.5); opacity: 0; }
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(10,0,30,.7) !important;
    border-right: 1px solid rgba(111,30,255,.25) !important;
    backdrop-filter: blur(30px) saturate(180%);
    box-shadow: 4px 0 30px rgba(111,30,255,.1);
}
section[data-testid="stSidebar"] * { color: #d4c6ff !important; }

/* ── Sidebar logo ── */
.logo-wrap {
    position: relative; text-align: center;
    padding: 34px 18px 26px; margin-bottom: 24px;
    border-radius: 22px; overflow: hidden;
}
.logo-wrap::before {
    content: ''; position: absolute; inset: -2px; border-radius: 24px; z-index: 0;
    background: linear-gradient(45deg, #6c1fff, #ff1464, #00c8ff, #6c1fff);
    background-size: 300% 300%;
    animation: borderSpin 4s linear infinite;
}
.logo-wrap::after {
    content: ''; position: absolute; inset: 2px; border-radius: 21px; z-index: 1;
    background: linear-gradient(145deg, rgba(20,0,60,.95), rgba(10,0,30,.98));
}
@keyframes borderSpin { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
.logo-inner { position: relative; z-index: 2; }
.logo-shield {
    font-size: 3.8rem; display: block; position: relative; z-index:2;
    filter: drop-shadow(0 0 25px rgba(111,30,255,1)) drop-shadow(0 0 50px rgba(255,20,100,.6));
    animation: shieldFloat 3.5s ease-in-out infinite, shieldGlow 2s ease-in-out infinite alternate;
}
@keyframes shieldFloat  { 0%,100%{transform:translateY(0) rotate(-2deg)} 50%{transform:translateY(-8px) rotate(2deg)} }
@keyframes shieldGlow   { 0%{filter:drop-shadow(0 0 20px rgba(111,30,255,.9)) drop-shadow(0 0 40px rgba(255,20,100,.5))}
                          100%{filter:drop-shadow(0 0 35px rgba(111,30,255,1)) drop-shadow(0 0 70px rgba(0,200,255,.6))} }
.logo-name {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.4rem; font-weight: 900; letter-spacing: 2px;
    background: linear-gradient(90deg, #b084ff, #ff6eb4, #67e8f9, #b084ff);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
    text-transform: uppercase;
}
@keyframes shimmer { to { background-position: 200% center; } }
.logo-tag {
    font-size: .65rem; letter-spacing: 3px; text-transform: uppercase;
    color: rgba(180,150,255,.6) !important; margin-top: 5px;
}

/* ── Sidebar stat chips ── */
.stat-chip {
    display: flex; align-items: center; justify-content: space-between;
    padding: 9px 14px; border-radius: 12px; margin-bottom: 7px;
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(111,30,255,.2);
    font-size: .78rem; font-weight: 600;
    transition: all .25s;
}
.stat-chip:hover { background: rgba(111,30,255,.1); border-color: rgba(111,30,255,.4); transform: translateX(3px); }
.stat-val { font-family: 'JetBrains Mono', monospace !important; color: #a78bfa !important; font-size: .85rem; font-weight: 700; }

/* ── Signal items ── */
.signal {
    display: flex; align-items: center; gap: 10px;
    padding: 7px 10px; border-radius: 10px;
    font-size: .76rem; color: rgba(200,180,255,.6) !important;
    border: 1px solid transparent;
    transition: all .2s;
    cursor: default;
}
.signal:hover {
    background: rgba(111,30,255,.08); border-color: rgba(111,30,255,.2);
    color: rgba(220,210,255,.9) !important; padding-left: 14px;
}
.sig-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }

/* ── Hero ── */
.hero {
    position: relative; overflow: hidden; text-align: center;
    padding: 60px 40px 50px;
    border-radius: 30px; margin-bottom: 40px;
    background: linear-gradient(135deg,
        rgba(111,30,255,.15) 0%,
        rgba(255,20,100,.10) 40%,
        rgba(0,200,255,.08) 100%);
    border: 1px solid rgba(111,30,255,.2);
    box-shadow: 0 0 80px rgba(111,30,255,.1), inset 0 1px 0 rgba(255,255,255,.06);
}
/* Scan-line effect */
.hero::before {
    content: ''; position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(111,30,255,.015) 2px, rgba(111,30,255,.015) 4px
    );
    animation: scanMove 8s linear infinite;
}
@keyframes scanMove { 0% { background-position: 0 0; } 100% { background-position: 0 400px; } }
/* Glow blob */
.hero::after {
    content: ''; position: absolute; top: -30%; left: 50%; transform: translateX(-50%);
    width: 700px; height: 500px; z-index: 0;
    background: radial-gradient(ellipse, rgba(111,30,255,.2) 0%, rgba(255,20,100,.08) 40%, transparent 65%);
    animation: blobPulse 6s ease-in-out infinite alternate;
    pointer-events: none;
}
@keyframes blobPulse { 0%{opacity:.5;transform:translateX(-50%) scale(1)} 100%{opacity:1;transform:translateX(-50%) scale(1.15)} }

.hero > * { position: relative; z-index: 1; }
.hero-icon {
    font-size: 5rem; display: inline-block;
    filter: drop-shadow(0 0 30px rgba(111,30,255,.9)) drop-shadow(0 0 60px rgba(255,20,100,.5));
    animation: heroFloat 4s ease-in-out infinite;
}
@keyframes heroFloat { 0%,100%{transform:translateY(0) scale(1)} 50%{transform:translateY(-12px) scale(1.05)} }
.hero-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 3.2rem; font-weight: 900; letter-spacing: -1px; line-height: 1.1;
    margin-top: 14px;
    background: linear-gradient(90deg, #c084fc 0%, #f472b6 25%, #38bdf8 50%, #4ade80 75%, #c084fc 100%);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shimmer 4s linear infinite;
    text-shadow: none;
}
.hero-sub { color: rgba(255,255,255,.65); font-size: 1.05rem; margin-top: 10px; letter-spacing: .3px; }

/* ── Neon stat bar ── */
.stat-bar {
    display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;
    margin-top: 28px;
}
.stat-item {
    display: flex; flex-direction: column; align-items: center;
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 18px; padding: 14px 22px;
    backdrop-filter: blur(12px);
    min-width: 100px;
    transition: transform .2s, box-shadow .2s;
}
.stat-item:hover { transform: translateY(-4px); box-shadow: 0 10px 30px rgba(111,30,255,.3); }
.stat-num {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.6rem; font-weight: 800; line-height: 1;
}
.stat-lbl { font-size: .65rem; color: rgba(255,255,255,.45); text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,.02);
    border: 1px solid rgba(111,30,255,.15);
    border-radius: 24px; padding: 28px 24px;
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 40px rgba(0,0,0,.3), inset 0 1px 0 rgba(255,255,255,.04);
    margin-bottom: 24px;
}

/* ── Section header ── */
.sec-hdr {
    font-size: .85rem; font-weight: 700; margin-bottom: 12px;
    text-transform: uppercase; letter-spacing: 1.5px;
    color: rgba(180,150,255,.7);
    display: flex; align-items: center; gap: 10px;
}
.sec-hdr::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(111,30,255,.4), transparent);
}

/* ── Textarea ── */
.stTextArea textarea {
    background: rgba(255,255,255,.95) !important;
    border: 2px solid rgba(111,30,255,.35) !important;
    border-radius: 18px !important; color: #0d0020 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: .95rem !important;
    transition: border .25s, box-shadow .25s !important;
    box-shadow: 0 4px 24px rgba(0,0,0,.25), 0 0 0 0 rgba(111,30,255,0) !important;
}
.stTextArea textarea:focus {
    border-color: rgba(111,30,255,.8) !important;
    box-shadow: 0 0 0 4px rgba(111,30,255,.18), 0 0 30px rgba(111,30,255,.15) !important;
}

/* ── Options mini-card ── */
.opt-mini {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(111,30,255,.15);
    border-radius: 20px; padding: 20px 16px;
    backdrop-filter: blur(16px);
}

/* ── Selectbox ── */
.stSelectbox > div {
    background: rgba(255,255,255,.95) !important;
    border-radius: 12px !important;
    border: 1.5px solid rgba(111,30,255,.3) !important;
}
.stSelectbox div[data-baseweb] *, [data-testid="stSelectbox"] * { color: #1a0040 !important; }
[data-baseweb="menu"] *, [data-baseweb="popover"] * { background: #fff !important; color: #1a0040 !important; }
[data-testid="stWidgetLabel"] p, .stTextArea label p, .stSelectbox label p {
    color: rgba(200,180,255,.85) !important; font-weight: 600 !important; font-size: .82rem !important;
    text-transform: uppercase !important; letter-spacing: 1px !important;
}

/* ── Analyse button ── */
.stButton > button {
    font-family: 'Orbitron', monospace !important;
    background: linear-gradient(90deg, #5b21b6, #9d1b6e, #0e7490, #5b21b6) !important;
    background-size: 300% auto !important;
    color: white !important; border: none !important;
    border-radius: 18px !important; font-weight: 800 !important;
    font-size: 1rem !important; padding: .9rem 2.4rem !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
    transition: all .3s ease !important;
    box-shadow:
        0 0 0 1px rgba(111,30,255,.5),
        0 8px 32px rgba(111,30,255,.5),
        0 0 60px rgba(111,30,255,.2) !important;
    animation: btnPulse 3s ease-in-out infinite !important;
    position: relative !important;
}
@keyframes btnPulse {
    0%,100% { box-shadow: 0 0 0 1px rgba(111,30,255,.5), 0 8px 32px rgba(111,30,255,.5), 0 0 60px rgba(111,30,255,.15); }
    50%      { box-shadow: 0 0 0 2px rgba(255,20,100,.6), 0 8px 40px rgba(255,20,100,.5), 0 0 80px rgba(255,20,100,.2);  }
}
.stButton > button:hover {
    background-position: right center !important;
    transform: translateY(-5px) scale(1.03) !important;
    box-shadow: 0 0 0 2px rgba(111,30,255,.8), 0 14px 50px rgba(111,30,255,.7), 0 0 100px rgba(111,30,255,.3) !important;
}

/* ── Divider ── */
.neon-divider {
    display: flex; align-items: center; gap: 16px; margin: 32px 0 26px;
}
.neon-divider .line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(111,30,255,.6), rgba(255,20,100,.4), transparent);
}
.neon-divider .label {
    font-family: 'Orbitron', monospace !important;
    font-size: .65rem; font-weight: 700; letter-spacing: 3px;
    color: rgba(180,150,255,.7); text-transform: uppercase;
    background: rgba(111,30,255,.12); padding: 5px 14px; border-radius: 9999px;
    border: 1px solid rgba(111,30,255,.25);
}

/* ── Verdict card ── */
.verdict {
    border-radius: 26px; padding: 36px 28px; text-align: center;
    position: relative; overflow: hidden;
    transition: transform .3s, box-shadow .3s;
}
.verdict:hover { transform: translateY(-6px); }
.verdict-fake {
    background: linear-gradient(145deg, rgba(220,38,38,.18) 0%, rgba(239,68,68,.06) 100%);
    border: 1.5px solid rgba(239,68,68,.4);
    box-shadow: 0 12px 50px rgba(239,68,68,.2), 0 0 0 1px rgba(239,68,68,.1), inset 0 1px 0 rgba(255,255,255,.05);
}
.verdict-genuine {
    background: linear-gradient(145deg, rgba(21,128,61,.18) 0%, rgba(34,197,94,.06) 100%);
    border: 1.5px solid rgba(34,197,94,.4);
    box-shadow: 0 12px 50px rgba(34,197,94,.2), 0 0 0 1px rgba(34,197,94,.1), inset 0 1px 0 rgba(255,255,255,.05);
}
/* Animated corner accents */
.verdict::before, .verdict::after {
    content: ''; position: absolute; width: 24px; height: 24px; border-style: solid;
}
.verdict-fake::before  { top:12px;  left:12px;  border-color: rgba(239,68,68,.5) transparent transparent rgba(239,68,68,.5); border-width: 2px 0 0 2px; }
.verdict-fake::after   { bottom:12px; right:12px; border-color: transparent rgba(239,68,68,.5) rgba(239,68,68,.5) transparent; border-width: 0 2px 2px 0; }
.verdict-genuine::before { top:12px; left:12px; border-color: rgba(34,197,94,.5) transparent transparent rgba(34,197,94,.5); border-width: 2px 0 0 2px; }
.verdict-genuine::after  { bottom:12px; right:12px; border-color: transparent rgba(34,197,94,.5) rgba(34,197,94,.5) transparent; border-width: 0 2px 2px 0; }

.verdict-icon  { font-size: 4rem; display: block; position: relative; z-index:1;
                 animation: iconPop .5s cubic-bezier(.34,1.56,.64,1) both; }
@keyframes iconPop { from{transform:scale(0) rotate(-20deg)} to{transform:scale(1) rotate(0)} }
.verdict-label {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.7rem; font-weight: 900; letter-spacing: 1px; margin-top: 10px;
    position: relative; z-index:1;
}
.verdict-fake    .verdict-label { color: #f87171; text-shadow: 0 0 20px rgba(248,113,113,.6), 0 0 40px rgba(248,113,113,.3); }
.verdict-genuine .verdict-label { color: #4ade80; text-shadow: 0 0 20px rgba(74,222,128,.6),  0 0 40px rgba(74,222,128,.3);  }
.verdict-prob   { font-size: .9rem; color: rgba(255,255,255,.7); margin-top: 8px; position: relative; z-index:1; }
.verdict-conf   {
    display: inline-block; margin-top: 14px; padding: 5px 18px;
    border-radius: 9999px; font-size: .72rem; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; position: relative; z-index:1;
}
.verdict-fake    .verdict-conf { background:rgba(239,68,68,.18); color:#fca5a5; border:1px solid rgba(239,68,68,.4); }
.verdict-genuine .verdict-conf { background:rgba(34,197,94,.18);  color:#86efac; border:1px solid rgba(34,197,94,.4);  }

/* ── Risk card ── */
.risk-card {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(111,30,255,.15);
    border-radius: 22px; padding: 20px 18px;
    backdrop-filter: blur(16px);
    box-shadow: 0 4px 30px rgba(0,0,0,.25);
}
.risk-bar-wrap   { margin-bottom: 13px; }
.risk-bar-header { display:flex; justify-content:space-between; margin-bottom:5px; font-size:.78rem; color:rgba(220,210,255,.8); font-weight:500; }
.risk-bar-bg     { height: 9px; border-radius: 9999px; background:rgba(255,255,255,.07); overflow:hidden; position:relative; }
.risk-bar-fill   { height: 100%; border-radius: 9999px; transition: width 1s cubic-bezier(.4,0,.2,1); position:relative; }
.risk-bar-fill::after { content:''; position:absolute; right:0; top:0; bottom:0; width:4px; filter:blur(3px); background:inherit; }

/* ── Misc ── */
hr { border-color: rgba(111,30,255,.15) !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(111,30,255,.4); border-radius: 9999px; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Floating particles HTML ────────────────────────────────────────────────────
COLORS = ["#a78bfa","#f472b6","#38bdf8","#4ade80","#fb923c","#c084fc"]
particles_html = '<div class="particles">'
import random
random.seed(7)
for i in range(25):
    size   = random.randint(3, 9)
    left   = random.randint(0, 100)
    dur    = random.randint(12, 28)
    delay  = random.randint(0, 18)
    color  = COLORS[i % len(COLORS)]
    glow   = f"0 0 {size*3}px {color}"
    particles_html += (
        f'<div class="particle" style="'
        f'width:{size}px;height:{size}px;left:{left}%;'
        f'background:{color};box-shadow:{glow};'
        f'animation-duration:{dur}s;animation-delay:-{delay}s;'
        f'"></div>'
    )
particles_html += "</div>"
st.markdown(particles_html, unsafe_allow_html=True)


# ─────────────────────────────────────── Load model ──────────────────────────
@st.cache_resource(show_spinner=False)
def get_model():
    return train_model()

with st.spinner("⚡ Initialising AI…"):
    clf, acc = get_model()


# ─────────────────────────────────────── Sidebar ─────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="logo-wrap">
      <div class="logo-inner">
        <span class="logo-shield">🛡️</span>
        <div class="logo-name">FakeShield</div>
        <div class="logo-tag">Review Authenticity AI</div>
      </div>
    </div>

    <div style="margin-bottom:18px;">
      <div class="stat-chip">
        <span>🤖 Model</span>
        <span class="stat-val">RandomForest</span>
      </div>
      <div class="stat-chip">
        <span>🎯 Accuracy</span>
        <span class="stat-val" style="color:#4ade80!important;">{acc}%</span>
      </div>
      <div class="stat-chip">
        <span>⚡ Features</span>
        <span class="stat-val">11</span>
      </div>
      <div class="stat-chip">
        <span>🔥 Status</span>
        <span class="stat-val" style="color:#4ade80!important;">ONLINE</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="font-size:.65rem;font-weight:700;color:rgba(180,150,255,.5)!important;
                letter-spacing:2.5px;text-transform:uppercase;margin-bottom:10px;">
        Detection Signals
    </div>
    """, unsafe_allow_html=True)

    SIGNALS = [
        ("#f472b6","🔠","ALL-CAPS overuse"),
        ("#fb923c","❗","Excessive exclamations"),
        ("#a78bfa","🔁","Low vocabulary variety"),
        ("#38bdf8","🎭","Extreme subjectivity"),
        ("#f87171","🛒","Unverified purchase"),
        ("#fbbf24","⭐","Extreme ratings (1 or 5★)"),
        ("#86efac","😀","Emoji overuse"),
        ("#c084fc","📏","Suspicious text length"),
    ]
    sig_html = ""
    for color, icon, label in SIGNALS:
        sig_html += f"""
        <div class="signal">
          <div class="sig-dot" style="background:{color};box-shadow:0 0 6px {color};"></div>
          <span style="margin-right:4px;">{icon}</span>
          <span>{label}</span>
        </div>"""
    st.markdown(sig_html, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:.6rem;color:rgba(255,255,255,.12);text-align:center;margin-top:24px;line-height:2.2;font-family:'JetBrains Mono',monospace!important;">
    v2.0 · Python · scikit-learn<br>Streamlit · Plotly · TextBlob
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  Hero
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
  <div class="hero-icon">🛡️</div>
  <div class="hero-title">FAKESHIELD</div>
  <div class="hero-sub">AI-Powered Review Authenticity Detector · Real-time · 11 Signals</div>
  <div class="stat-bar">
    <div class="stat-item">
      <div class="stat-num" style="color:#c084fc;">{acc}%</div>
      <div class="stat-lbl">Accuracy</div>
    </div>
    <div class="stat-item">
      <div class="stat-num" style="color:#f472b6;">200</div>
      <div class="stat-lbl">Trees</div>
    </div>
    <div class="stat-item">
      <div class="stat-num" style="color:#38bdf8;">11</div>
      <div class="stat-lbl">Signals</div>
    </div>
    <div class="stat-item">
      <div class="stat-num" style="color:#4ade80;">1K</div>
      <div class="stat-lbl">Trained On</div>
    </div>
    <div class="stat-item">
      <div class="stat-num" style="color:#fb923c;">⚡</div>
      <div class="stat-lbl">Real-time</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  Input zone
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-hdr">📝 Review Text</div>', unsafe_allow_html=True)
review_text = st.text_area(
    "Review Text",
    placeholder="Paste or type your e-commerce review here…",
    height=180,
    label_visibility="collapsed",
)

col_a, col_b = st.columns(2, gap="medium")
with col_a:
    rating = st.selectbox("⭐ Star Rating", [5, 4, 3, 2, 1])
with col_b:
    verified = st.selectbox("🛒 Purchase Type", ["Unverified", "Verified"])
verified_int = 1 if verified == "Verified" else 0

st.markdown("<br>", unsafe_allow_html=True)
_, bc, _ = st.columns([1.8, 1, 1.8])
with bc:
    go_btn = st.button("⚡  ANALYSE", use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  Results
# ══════════════════════════════════════════════════════════════════════════════
if go_btn and review_text.strip():


    result = predict(clf, review_text, rating=rating, verified=verified_int)
    fp     = result["fake_prob"]
    lbl    = result["label"]
    feats  = result["features"]

    # Divider
    st.markdown("""
    <div class="neon-divider">
      <div class="line"></div>
      <div class="label">⚡ AI Analysis Results</div>
      <div class="line" style="background:linear-gradient(90deg,rgba(255,20,100,.4),rgba(111,30,255,.6),transparent);"></div>
    </div>
    """, unsafe_allow_html=True)

    col_v, col_g, col_r2 = st.columns([1, 1.15, 1], gap="medium")

    # ── Verdict ───────────────────────────────────────────────────────────────
    with col_v:
        cls      = "verdict-fake" if lbl else "verdict-genuine"
        icon_v   = "🚨" if lbl else "✅"
        label_v  = "FAKE" if lbl else "GENUINE"
        conf_lbl = "HIGH" if fp > 0.75 or fp < 0.25 else "MEDIUM" if fp > 0.60 or fp < 0.40 else "LOW"
        st.markdown(f"""
        <div class="verdict {cls}">
            <span class="verdict-icon">{icon_v}</span>
            <div class="verdict-label">{label_v}</div>
            <div class="verdict-prob">Fake probability: <b>{fp*100:.1f}%</b></div>
            <span class="verdict-conf">{conf_lbl} CONFIDENCE</span>
        </div>""", unsafe_allow_html=True)

    # ── Gauge ─────────────────────────────────────────────────────────────────
    with col_g:
        bar_color = "#f87171" if lbl else "#4ade80"
        fig = go.Figure(go.Indicator(
            mode  = "gauge+number",
            value = round(fp * 100, 1),
            number= {"suffix": "%", "font": {"size": 52, "color": "white", "family": "Orbitron"}},
            title = {"text": "FAKE SCORE", "font": {"size": 11, "color": "rgba(180,150,255,.6)", "family": "Orbitron"}},
            gauge = {
                "axis": {
                    "range": [0, 100],
                    "tickcolor": "rgba(180,150,255,.2)",
                    "tickfont" : {"color": "rgba(180,150,255,.3)", "size": 10},
                    "dtick": 25,
                },
                "bar": {"color": bar_color, "thickness": .3},
                "bgcolor": "rgba(255,255,255,.02)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0,  33], "color": "rgba(74,222,128,.08)"},
                    {"range": [33, 66], "color": "rgba(234,179,8,.07)"},
                    {"range": [66,100], "color": "rgba(248,113,113,.08)"},
                ],
            },
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="white", height=280,
            margin=dict(l=24, r=24, t=70, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Risk bars ─────────────────────────────────────────────────────────────
    with col_r2:
        st.markdown('<div class="sec-hdr">⚡ Risk Signals</div>', unsafe_allow_html=True)
        st.markdown('<div class="risk-card">', unsafe_allow_html=True)
        RISKS = [
            ("🔠 CAPS Usage",    min(feats["capital_ratio"] * 3, 1),         "#f472b6"),
            ("❗ Exclamations",  min(feats["exclamation_count"] / 8, 1),      "#fb923c"),
            ("🔁 Word Repeat",   max(0, 1 - feats["unique_word_ratio"]),      "#a78bfa"),
            ("🎭 Subjectivity",  feats["sentiment_subjectivity"],             "#38bdf8"),
            ("🛒 Unverified",    1 - feats["verified_purchase"],              "#f87171"),
            ("⭐ Extreme Rating",float(feats["extreme_rating"]),              "#fbbf24"),
            ("😀 Emoji Overuse", min(feats["emoji_count"] / 5, 1),           "#86efac"),
        ]
        bars = ""
        for lbl_r, score, color in RISKS:
            pct = int(score * 100)
            bars += f"""
            <div class="risk-bar-wrap">
              <div class="risk-bar-header">
                <span>{lbl_r}</span>
                <span style="color:{color};font-weight:700;font-family:'JetBrains Mono',monospace;">{pct}%</span>
              </div>
              <div class="risk-bar-bg">
                <div class="risk-bar-fill"
                     style="width:{pct}%;
                            background:linear-gradient(90deg,{color}55,{color});
                            box-shadow: 0 0 12px {color}80, 0 0 4px {color};">
                </div>
              </div>
            </div>"""
        st.markdown(bars + "</div>", unsafe_allow_html=True)

elif go_btn:
    st.warning("⚠️ Please enter a review to analyse.")
