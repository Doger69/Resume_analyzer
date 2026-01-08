import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt

from utils import (
    calculate_similarity,
    keyword_gap_analysis,
    ats_score,
    resume_suggestions
)
from pdf_report import generate_pdf


# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Resume–Job Match Analyzer",
    page_icon="📄",
    layout="wide"
)


# ================== GLOBAL STYLES ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top, #020617, #020617);
}

.card {
    background: linear-gradient(145deg, #020617, #020617);
    border-radius: 20px;
    padding: 28px;
    border: 1px solid #1e293b;
    box-shadow: 0 25px 60px rgba(0,0,0,0.55);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 54px;
    font-weight: 800;
    text-align: center;
}

.hero-subtitle {
    font-size: 18px;
    color: #94a3b8;
    text-align: center;
    margin-bottom: 60px;
}

.score {
    font-size: 52px;
    font-weight: 800;
}

.progress-bg {
    background: #020617;
    height: 20px;
    border-radius: 12px;
    margin-top: 6px;
}

.progress-fill {
    height: 20px;
    border-radius: 12px;
    background: linear-gradient(90deg, #ef4444, #f59e0b, #22c55e);
}
</style>
""", unsafe_allow_html=True)


# ================== HEADER ==================
st.markdown('<div class="hero-title">Resume–Job Match Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Professional ATS-style resume evaluation powered by NLP</div>',
    unsafe_allow_html=True
)


# ================== FUNCTIONS ==================
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t
    return text


def progress_bar(label, value):
    st.markdown(f"""
    <div style="margin-bottom:18px;">
        <strong>{label}</strong>
        <div class="progress-bg">
            <div class="progress-fill" style="width:{value}%"></div>
        </div>
        <div style="margin-top:6px; font-weight:600;">{value}%</div>
    </div>
    """, unsafe_allow_html=True)


# ================== INPUT SECTION ==================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📄 Upload Resume")
    resume = st.file_uploader("", type=["pdf"])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Job Description")
    job_desc = st.text_area("", height=240)
    st.markdown('</div>', unsafe_allow_html=True)


# ================== ANALYZE BUTTON ==================
st.markdown('<div class="card">', unsafe_allow_html=True)
analyze = st.button("🔍 Analyze Match", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# ================== RESULTS ==================
if analyze:
    if not resume or not job_desc:
        st.warning("Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing resume..."):
            resume_text = extract_text_from_pdf(resume)

            score = calculate_similarity(resume_text, job_desc)
            missing = keyword_gap_analysis(resume_text, job_desc)
            ats = ats_score(score, missing)
            suggestions = resume_suggestions(score, missing)

        # ================== SCORES ==================
        colA, colB = st.columns(2, gap="large")

        with colA:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 Match Scores")
            progress_bar("Similarity Score", score)
            progress_bar("ATS Compatibility", ats)
            st.markdown('</div>', unsafe_allow_html=True)

        with colB:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📈 ATS Overview")

            fig, ax = plt.subplots()
            ax.pie(
                [ats, 100 - ats],
                startangle=90,
                wedgeprops=dict(width=0.35)
            )
            ax.set_aspect("equal")
            st.pyplot(fig)

            st.markdown('</div>', unsafe_allow_html=True)

        # ================== KEYWORD GAP ==================
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🧩 Missing Keywords")

        if missing:
            for kw in missing[:15]:
                st.markdown(
                    f"""
                    <div style="margin-bottom:8px;">
                        <span style="font-weight:600;">{kw}</span>
                        <div class="progress-bg">
                            <div class="progress-fill" style="width:35%"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.success("No major keyword gaps found.")

        st.markdown('</div>', unsafe_allow_html=True)

        # ================== SUGGESTIONS ==================
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💡 Resume Improvement Suggestions")

        for s in suggestions:
            st.markdown(f"- {s}")

        st.markdown('</div>', unsafe_allow_html=True)

        # ================== PDF EXPORT ==================
        pdf_file = generate_pdf(score, ats, missing, suggestions)

        with open(pdf_file, "rb") as f:
            st.download_button(
                "📄 Download Professional PDF Report",
                f,
                file_name="resume_match_report.pdf",
                use_container_width=True
            )
