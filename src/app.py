import streamlit as st
from job_fit_agent import JobFitAgent
from resume_reader import extract_text_from_file

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(page_title="Job-Fit Agent", layout="wide", page_icon="🎯")

# ── Theme Setup ──────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "results" not in st.session_state:
    st.session_state.results = None

THEMES = {
    "Dark": {
        "bg": "#0B132B", "sidebar": "#1C2541", "card": "#3A506B",
        "text": "#F5F5F5", "muted": "#B8C1D1", "accent": "#5BC0BE", "accent2": "#6FFFE9",
        "input_bg": "#22304A", "border": "rgba(255,255,255,0.12)"
    },
    "Light": {
        "bg": "#F7F9FC", "sidebar": "#FFFFFF", "card": "#FFFFFF",
        "text": "#0B132B", "muted": "#5A6472", "accent": "#0F8B8D", "accent2": "#0B6E70",
        "input_bg": "#F0F3F8", "border": "rgba(0,0,0,0.1)"
    }
}

def inject_css(t):
    st.markdown(f"""
    <style>
        /* ---- Base ---- */
        .stApp {{ background-color: {t['bg']}; }}
        section[data-testid="stSidebar"] {{
            background-color: {t['sidebar']};
            border-right: 1px solid {t['border']};
        }}

        /* ---- Universal text fix (covers headers, labels, radio, everything) ---- */
        section[data-testid="stSidebar"] * ,
        .main * {{
            color: {t['text']};
        }}
        h1, h2, h3, h4, h5, h6 {{ color: {t['text']} !important; }}

        /* ---- Header ---- */
        .main-header {{
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(90deg, {t['accent']}, {t['accent2']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }}
        .sub-header {{ color: {t['muted']} !important; font-size: 1rem; }}

        /* ---- Inputs (text, select, slider) ---- */
        div[data-baseweb="input"], div[data-baseweb="select"] > div {{
            background-color: {t['input_bg']} !important;
            color: {t['text']} !important;
            border-radius: 8px !important;
        }}
        input, textarea {{ color: {t['text']} !important; }}

        /* ---- File uploader ---- */
        div[data-testid="stFileUploaderDropzone"] {{
            background-color: {t['input_bg']} !important;
            border: 1.5px dashed {t['accent']} !important;
            border-radius: 10px !important;
        }}
        div[data-testid="stFileUploaderDropzone"] * {{ color: {t['text']} !important; }}
        div[data-testid="stFileUploaderDropzoneInstructions"] span,
        div[data-testid="stFileUploaderDropzoneInstructions"] small {{
            color: {t['muted']} !important;
        }}

        /* ---- Buttons ---- */
        .stButton > button, .stDownloadButton > button {{
            background: linear-gradient(90deg, {t['accent']}, {t['accent2']});
            color: #0B132B !important;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1rem;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(0,0,0,0.25);
        }}
        .stButton > button p {{ color: #0B132B !important; }}

        /* ---- Job Cards ---- */
        .job-card {{
            background: {t['card']};
            padding: 22px 24px;
            border-radius: 14px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            margin-bottom: 4px;
            border-left: 5px solid {t['accent']};
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .job-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }}
        .job-title {{ font-size: 1.15rem; font-weight: 700; color: {t['text']}; margin: 0; }}

        /* ---- Badges ---- */
        .badge {{
            display: inline-block; padding: 4px 12px; border-radius: 20px;
            font-size: 0.75rem; font-weight: 700; margin-left: 8px;
        }}
        .badge-govt {{ background: {t['accent']}; color: #0B132B; }}
        .badge-private {{ background: #F0C808; color: #1A1A1A; }}
        .badge-good {{ background: #2ECC71; color: #08321A; }}
        .badge-average {{ background: #F0C808; color: #1A1A1A; }}
        .badge-bad {{ background: #E74C3C; color: #FFFFFF; }}

        /* ---- Metrics ---- */
        div[data-testid="stMetricValue"] {{ color: {t['accent2']} !important; font-weight: 800; }}
        div[data-testid="stMetricLabel"] {{ color: {t['muted']} !important; }}

        /* ---- Expander ---- */
        div[data-testid="stExpander"] {{
            background-color: {t['card']} !important;
            border-radius: 10px !important;
            border: 1px solid {t['border']} !important;
        }}
        div[data-testid="stExpander"] * {{ color: {t['text']} !important; }}

        /* ---- Divider spacing ---- */
        hr {{ border-color: {t['border']}; }}
    </style>
    """, unsafe_allow_html=True)

t = THEMES[st.session_state.theme]
inject_css(t)

# ── Cached Agent Loader (senior touch: don't reload the model every run) ──
@st.cache_resource
def load_agent():
    return JobFitAgent('../data/resume_ds.txt', '../data/resume_sde.txt')

# ── Header ───────────────────────────────────────────────────
header_col, theme_col = st.columns([5, 1])
with header_col:
    st.markdown('<p class="main-header">🎯 Autonomous Job-Fit Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real jobs fetch karta hai, resume se score karta hai, aur best matches rank karta hai.</p>', unsafe_allow_html=True)
with theme_col:
    new_theme = st.selectbox("Theme", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1, label_visibility="collapsed")
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

st.divider()

# ── Sidebar: Settings ────────────────────────────────────────
st.sidebar.header("⚙️ Search Settings")
keyword = st.sidebar.text_input("Job keyword", value="data scientist")
num_results = st.sidebar.slider("Number of jobs to fetch", 5, 20, 10)
branch = st.sidebar.selectbox("Your branch", ["IT/Computer Science", "Mechanical", "Civil", "Electrical"])

st.sidebar.header("📄 Resume")
resume_mode = st.sidebar.radio("Resume source", ["Upload my own resume", "Use built-in demo resumes (DS/SDE)"])

uploaded_resume_text = None
if resume_mode == "Upload my own resume":
    uploaded_file = st.sidebar.file_uploader("Upload resume", type=["txt", "pdf", "docx"])
    if uploaded_file is not None:
        try:
            uploaded_resume_text = extract_text_from_file(uploaded_file)
            st.sidebar.success("✅ Resume loaded!")
        except Exception as e:
            st.sidebar.error(f"Could not read file: {e}")

run_clicked = st.sidebar.button("🚀 Run Agent", use_container_width=True)

# ── Run Logic ────────────────────────────────────────────────
if run_clicked:
    if resume_mode == "Upload my own resume" and uploaded_resume_text is None:
        st.error("Pehle resume upload karo, phir Run Agent dabao.")
    else:
        progress_text = st.empty()
        progress_bar = st.progress(0)

        progress_text.text("🔍 Fetching live jobs...")
        progress_bar.progress(30)

        agent = load_agent()

        progress_text.text("🧠 Scoring jobs against your resume...")
        progress_bar.progress(65)

        if resume_mode == "Upload my own resume":
            results = agent.run_with_resume(uploaded_resume_text, keyword=keyword, num_results=num_results, branch=branch)
        else:
            results = agent.run(keyword=keyword, num_results=num_results, branch=branch)

        progress_bar.progress(100)
        progress_bar.empty()
        progress_text.empty()

        st.session_state.results = results

# ── Results Display (persists across reruns via session_state) ──
if st.session_state.results:
    results = st.session_state.results
    st.success(f"🎉 Found and ranked {len(results)} jobs!")

    for i, r in enumerate(results, start=1):
        sector_badge = "badge-govt" if r['sector'] == "Government" else "badge-private"
        fit_label = r.get('fit') or ("Good Fit" if r['chance'] >= 0.40 else "Average Fit" if r['chance'] >= 0.28 else "Bad Fit")
        fit_badge = "badge-good" if "Good" in fit_label else "badge-average" if "Average" in fit_label else "badge-bad"

        st.markdown(f"""
        <div class="job-card">
            <p class="job-title">{i}. {r['title']} at {r['company']}
                <span class="badge {sector_badge}">{r['sector']}</span>
                <span class="badge {fit_badge}">{fit_label}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Realistic Chance", f"{r['chance']:.3f}")
        if "resume_choice" in r:
            col2.metric("Resume Used", r['resume_choice'])
            col3.metric("Confidence", r['confidence'])

        st.progress(float(min(r['chance'], 1.0)))

        with st.expander("See skill details"):
            st.write(f"✓ **Matched:** {', '.join(r['matched']) if r['matched'] else 'None'}")
            st.write(f"✗ **Missing:** {', '.join(r['missing']) if r['missing'] else 'None'}")
            st.markdown(f"🔗 [Apply Here]({r['apply_link']})")

        st.write("")
else:
    st.info("👈 Settings set karo aur 'Run Agent' dabao results dekhne ke liye.")