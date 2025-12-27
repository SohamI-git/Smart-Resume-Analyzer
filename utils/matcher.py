from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(similarity * 100, 2)

def calculate_ats_score(match_score, resume_skills, jd_skills):
    skill_overlap = len(set(resume_skills) & set(jd_skills))
    skill_ratio = skill_overlap / max(len(jd_skills), 1)
    ats_score = (0.6 * match_score) + (0.4 * skill_ratio * 100)
    return min(round(ats_score, 2), 100)