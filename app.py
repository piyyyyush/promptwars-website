import time
import streamlit as st

from utils.pdf_reader import extract_text
from utils.profile_builder import build_profile
from agents.technical_agent import analyze as technical_analyze
from agents.hr_agent import analyze as hr_analyze
from agents.hiring_manager import analyze as manager_analyze
from agents.skeptic_agent import analyze as skeptic_analyze
from utils.debate_engine import run_debate
from utils.decision_engine import final_decision

st.set_page_config(
    page_title="AI Interview Panel",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    .stApp {
        background: #0b1020;
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background: #10172a;
    }
    .hero {
        padding: 2.2rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #172554, #312e81, #0f172a);
        border: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        font-size: 3rem;
        margin-bottom: 0.4rem;
    }
    .muted {
        color: #a5b4fc;
    }
    .glass-card {
        background: rgba(20, 28, 50, 0.85);
        border: 1px solid rgba(148,163,184,0.22);
        border-radius: 18px;
        padding: 1.2rem;
        min-height: 220px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.18);
    }
    .agent-title {
        font-size: 1.1rem;
        font-weight: 800;
    }
    .verdict {
        font-size: 1.5rem;
        font-weight: 900;
        color: #c4b5fd;
    }
    .evidence {
        background: #0f172a;
        border-left: 4px solid #8b5cf6;
        padding: 0.8rem;
        border-radius: 8px;
        color: #cbd5e1;
        margin-top: 0.8rem;
    }
    .debate {
        background: #121a2e;
        border: 1px solid rgba(148,163,184,0.2);
        border-radius: 16px;
        padding: 1.2rem;
        margin: 0.8rem 0;
    }
    .change-card {
        background: linear-gradient(135deg, #3f1d5b, #1e293b);
        border: 1px solid #a78bfa;
        border-radius: 16px;
        padding: 1.3rem;
    }
    .final-card {
        text-align: center;
        padding: 2rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #064e3b, #14532d);
        border: 1px solid #34d399;
    }
    .final-verdict {
        font-size: 3.5rem;
        font-weight: 1000;
        color: #86efac;
    }
    .metric-box {
        padding: 1rem;
        background: #121a2e;
        border-radius: 14px;
        border: 1px solid rgba(148,163,184,0.2);
        text-align: center;
    }
    .skill {
        display: inline-block;
        padding: 0.45rem 0.8rem;
        margin: 0.25rem;
        border-radius: 999px;
        background: #312e81;
        color: #e0e7ff;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if "results" not in st.session_state:
    st.session_state.results = None

with st.sidebar:
    st.markdown("## 🤖 AI Interview Panel")
    st.caption("Multi-Agent Hiring Intelligence")
    st.divider()
    st.markdown("### Panel Agents")
    st.markdown("💻 Technical Expert")
    st.markdown("👥 HR / Culture Expert")
    st.markdown("💼 Hiring Manager")
    st.markdown("🕵️ Skeptic Agent")

st.markdown("""
<div class="hero">
    <h1>🤖 AI Interview Panel</h1>
    <p class="muted">Multi-Agent Hiring Intelligence System</p>
    <p>Upload the job description, candidate resume and interview transcript. Four independent AI personas will analyze the evidence before debating and reaching a final recommendation.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📤 Upload & Analyze",
    "👤 Candidate Dashboard",
    "💬 Agent Debate",
    "⚖️ Final Decision"
])

with tab1:
    st.subheader("1️⃣ Upload Candidate Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        job_file = st.file_uploader("📄 Job Description", type=["pdf", "txt"], key="job")
    with col2:
        resume_file = st.file_uploader("📄 Candidate Resume", type=["pdf", "txt"], key="resume")
    with col3:
        transcript_file = st.file_uploader("💬 Interview Transcript", type=["pdf", "txt"], key="transcript")

    st.write("")
    start = st.button("🚀 START AI INTERVIEW ANALYSIS", use_container_width=True, type="primary")

    if start:
        if not all([job_file, resume_file, transcript_file]):
            st.warning("Please upload all three files before starting the analysis.")
        else:
            status_box = st.empty()
            steps = [
                "✓ Reading Resume",
                "✓ Extracting Candidate Profile",
                "🤖 Technical Agent analyzing...",
                "👥 HR Agent analyzing...",
                "💼 Hiring Manager analyzing...",
                "🕵️ Skeptic Agent analyzing...",
                "💬 Preparing Agent Debate...",
                "⚖️ Generating Final Decision..."
            ]

            progress = st.progress(0)
            for i, step in enumerate(steps):
                status_box.markdown(
                    f"""
                    <div class="glass-card">
                        <h3>{step}</h3>
                        <p class="muted">Multi-agent system is processing evidence...</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                progress.progress((i + 1) / len(steps))
                time.sleep(0.7)

            job_text = extract_text(job_file)
            resume_text = extract_text(resume_file)
            transcript_text = extract_text(transcript_file)

            profile = build_profile(resume_text, transcript_text)

            # Separate calls/functions preserve independent agent analysis.
            agent_results = {
                "Technical Agent": technical_analyze(resume_text, transcript_text, job_text),
                "HR / Culture Agent": hr_analyze(resume_text, transcript_text, job_text),
                "Hiring Manager Agent": manager_analyze(resume_text, transcript_text, job_text),
                "Skeptic Agent": skeptic_analyze(resume_text, transcript_text, job_text),
            }

            debate = run_debate(agent_results)
            decision = final_decision(agent_results)

            st.session_state.results = {
                "profile": profile,
                "agents": agent_results,
                "debate": debate,
                "decision": decision
            }
            st.session_state.analysis_complete = True

            status_box.success("Analysis complete! Open the other tabs to explore the panel results.")
            st.balloons()

with tab2:
    if not st.session_state.analysis_complete:
        st.info("Complete an analysis from the Upload & Analyze tab first.")
    else:
        results = st.session_state.results
        profile = results["profile"]

        st.subheader("👤 Candidate Profile")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="metric-box"><h4>Candidate</h4><h2>Candidate</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-box"><h4>Experience</h4><h2>{profile["experience"]}</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="metric-box"><h4>Panel Status</h4><h2>Analysis Complete</h2></div>', unsafe_allow_html=True)

        st.markdown("### 🧠 Skills")
        st.markdown("".join([f'<span class="skill">{skill}</span>' for skill in profile["skills"]]), unsafe_allow_html=True)

        st.markdown("### 🤖 Independent Agent Opinions")
        cols = st.columns(4)

        for column, (_, agent) in zip(cols, results["agents"].items()):
            with column:
                st.markdown(f"""
                <div class="glass-card">
                    <div class="agent-title">{agent["icon"]} {agent["name"]}</div>
                    <p class="verdict">{agent["verdict"]}</p>
                    <p>Confidence: <b>{agent["confidence"]}%</b></p>
                    <hr>
                    <b>Evidence</b>
                    <div class="evidence">{agent["evidence"]}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("### 📌 Detailed Agent Evidence")
        for _, agent in results["agents"].items():
            with st.expander(f'{agent["icon"]} {agent["name"]} — View Evidence'):
                st.write("**Strengths**")
                for item in agent["strengths"]:
                    st.write("•", item)

                st.write("**Concerns**")
                for item in agent["concerns"]:
                    st.write("•", item)

                st.write("**Supporting Evidence**")
                st.info(agent["evidence"])

with tab3:
    if not st.session_state.analysis_complete:
        st.info("Complete an analysis from the Upload & Analyze tab first.")
    else:
        st.subheader("💬 Multi-Agent Debate")
        st.caption("Agents first analyzed independently. The following stage allows them to respond to evidence from other agents.")

        for item in st.session_state.results["debate"]:
            if item["type"] == "opinion_change":
                st.markdown(f"""
                <div class="change-card">
                    <h3>{item["icon"]} {item["agent"]} — Opinion Changed</h3>
                    <p><b>Before Debate:</b> {item["before"]}</p>
                    <h2>⬇</h2>
                    <p><b>After Debate:</b> {item["after"]}</p>
                    <p>{item["text"]}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                label = {
                    "statement": "INITIAL ARGUMENT",
                    "response": "DIRECT RESPONSE / DISAGREEMENT",
                    "agreement": "AGREEMENT WITH LIMITATION"
                }.get(item["type"], "DEBATE")

                evidence_html = f'<div class="evidence">📌 Evidence: {item.get("evidence", "")}</div>'
                st.markdown(f"""
                <div class="debate">
                    <div class="agent-title">{item["icon"]} {item["agent"]}</div>
                    <p class="muted">{label}</p>
                    <p>{item["text"]}</p>
                    {evidence_html}
                </div>
                """, unsafe_allow_html=True)

with tab4:
    if not st.session_state.analysis_complete:
        st.info("Complete an analysis from the Upload & Analyze tab first.")
    else:
        decision = st.session_state.results["decision"]

        st.markdown(f"""
        <div class="final-card">
            <h2>⚖️ FINAL PANEL DECISION</h2>
            <div class="final-verdict">{decision["recommendation"]}</div>
            <h3>Confidence: {decision["confidence"]}</h3>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        left, right = st.columns(2)

        with left:
            st.markdown("### 💪 Strengths")
            for strength in decision["strengths"]:
                st.success(strength)

        with right:
            st.markdown("### ⚠️ Concerns")
            for concern in decision["concerns"]:
                st.warning(concern)

        st.markdown("### 🧠 How the Panel Reached This Decision")
        st.info(decision["reasoning"])

        st.markdown("### 🤝 Unresolved Agent Disagreement")
        st.error(decision["unresolved"])

        st.caption("Important: this final decision is evidence-weighted and is not calculated by simply averaging the four agent scores.")
