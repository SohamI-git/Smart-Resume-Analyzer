import streamlit as st
from utils.resume_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.skill_extractor import extract_skills
from utils.matcher import calculate_match

st.title("Smart Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description")

if uploaded_file and jd_text:
    resume_text = extract_text_from_pdf(uploaded_file)
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    skills = extract_skills(resume_clean)
    match_score = calculate_match(resume_clean, jd_clean)

    st.subheader("Results")
    st.write("**Job Match Score:**", match_score, "%")
    st.write("**Extracted Skills:**", skills)
