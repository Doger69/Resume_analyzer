import streamlit as st
from utils import extract_text_from_pdf, calculate_similarity

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Resume–Job Match Analyzer",
    page_icon="📄",
    layout="wide"
)

# ================== CUSTOM CSS ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top, #111827, #020617);
}

.main {
    padding: 3rem 6rem;
}

/* Header */
.hero-title {
    font-size: 52px;
    font-weight: 800;
    text-align: center;
    color: #f8fafc;
}
.hero-subtitle {
    font-size: 18px;
    color: #9ca3af;
    text-align: center;
    margin-bottom: 60px;
}

/* Cards */
.card {
    background: linear-gradient(145deg, #0f172a, #020617);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.5);
}

/* Buttons */
.stButton button {
    width: 100%;
    padding: 16px;
    font-size: 18px;
    font-weight: 600;
    border-radius: 16px;
    border: none;
    background: linear-gradient(90deg, #2563eb, #22c55e);
}

/* Score */
.score {
    font-size: 48px;
    font-weight: 800;
}

/* Progress bar */
.progress-bg {
    width: 100%;
    height: 22px;
    background: #020617;
    border-radius: 14px;
    margin-top: 12px;
}
.progress-fill {
    height: 100%;
    border-radius: 14px;
    background: linear-gradient(90deg, #ef4444, #f59e0b, #22c55e);
}

/* Status colors */
.low { color: #ef4444; }
.mid { color: #f59e0b; }
.high { color: #22c55e; }

</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown('<div class="hero-title">Resume–Job Match Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Upload your resume and instantly evaluate how well it matches a job description</div>',
    unsafe_allow_html=True
)

# ================== INPUT SECTION ==================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📄 Upload Resume")
    resume_file = st.file_uploader(
        "Upload your resume in PDF format",
        type=["pdf"],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=220,
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ================== ANALYZE BUTTON ==================
st.markdown('<div class="card">', unsafe_allow_html=True)
analyze = st.button("🔍 Analyze Match")
st.markdown('</div>', unsafe_allow_html=True)

# ================== RESULTS ==================
if analyze:
    if not resume_file or not job_description:
        st.warning("Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing resume..."):
            resume_text = extract_text_from_pdf(resume_file)
            score = calculate_similarity(resume_text, job_description)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Match Result")

        if score < 40:
            status_class = "low"
            message = "Low match. Consider improving your resume keywords."
        elif score < 70:
            status_class = "mid"
            message = "Moderate match. Some improvements recommended."
        else:
            status_class = "high"
            message = "Excellent match. Your resume aligns well."

        st.markdown(f'<div class="score {status_class}">{score}%</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="progress-bg">
            <div class="progress-fill" style="width:{score}%"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<p class='{status_class}' style='margin-top:15px;font-size:16px;'>{message}</p>",
                    unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
