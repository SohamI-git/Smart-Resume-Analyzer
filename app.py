import streamlit as st
from utils.resume_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.skill_extractor import extract_skills
from utils.matcher import calculate_match, calculate_ats_score
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# ---------------- CUSTOM THEME FEEL ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>📄 Smart Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>AI-powered resume analysis using NLP & Machine Learning</p>", unsafe_allow_html=True)

st.divider()

# ---------------- INPUT SECTION ----------------
st.subheader("📤 Upload Resume")
uploaded_file = st.file_uploader("Upload resume (PDF only)", type=["pdf"])

st.subheader("📝 Job Description")
jd_text = st.text_area("Paste the job description here", height=200)

# ---------------- ANALYZE BUTTON ----------------
if st.button("🔍 Analyze Resume"):

    if uploaded_file is None or jd_text.strip() == "":
        st.error("Please upload a resume and paste job description.")
    else:
        # -------- PROCESSING --------
        resume_text = extract_text_from_pdf(uploaded_file)
        resume_clean = clean_text(resume_text)
        jd_clean = clean_text(jd_text)

        resume_skills = extract_skills(resume_clean)
        jd_skills = extract_skills(jd_clean)

        match_score = calculate_match(resume_clean, jd_clean)

        # -------- ATS SCORE LOGIC --------
        skill_match_ratio = len(set(resume_skills) & set(jd_skills)) / max(len(jd_skills), 1)
        ats_score = int((0.6 * match_score) + (0.4 * skill_match_ratio * 100))
        ats_score = min(ats_score, 100)

        missing_skills = list(set(jd_skills) - set(resume_skills))

        # ---------------- RESULTS ----------------
        st.divider()
        st.subheader("📊 Analysis Results")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Job Match %", f"{match_score}%")
        with col2:
            st.metric("ATS Score", f"{ats_score}/100")

        st.subheader("📈 ATS Compatibility")
        st.progress(ats_score / 100)

        st.subheader("✅ Extracted Skills")
        if resume_skills:
            for skill in resume_skills:
                st.success(skill)
        else:
            st.warning("No skills detected.")

        st.subheader("❌ Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.warning(skill)
        else:
            st.success("Great! No major skills missing 🎉")

        # ---------------- PDF REPORT ----------------
        st.divider()
        st.subheader("📄 Download Report")

        def generate_pdf():
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            c = canvas.Canvas(temp_file.name, pagesize=A4)
            width, height = A4

            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Smart Resume Analyzer Report")

            c.setFont("Helvetica", 12)
            c.drawString(50, height - 90, f"Job Match Score: {match_score}%")
            c.drawString(50, height - 110, f"ATS Score: {ats_score}/100")

            c.drawString(50, height - 150, "Extracted Skills:")
            y = height - 170
            for skill in resume_skills:
                c.drawString(70, y, f"- {skill}")
                y -= 15

            y -= 10
            c.drawString(50, y, "Missing Skills:")
            y -= 20
            for skill in missing_skills:
                c.drawString(70, y, f"- {skill}")
                y -= 15

            c.save()
            return temp_file.name

        pdf_path = generate_pdf()

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF Report",
                data=f,
                file_name="Resume_Analysis_Report.pdf",
                mime="application/pdf"
            )

# ---------------- SIDEBAR ----------------
st.sidebar.title("ℹ️ About")
st.sidebar.info(
    "This application analyzes resumes against job descriptions "
    "using Natural Language Processing and Machine Learning."
)
st.sidebar.write("👨‍💻 Built by Soham Ingale")
