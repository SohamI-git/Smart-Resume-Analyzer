SKILLS = [
    'python','java','sql','machine learning','deep learning',
    'tensorflow','keras','pandas','numpy','cnn','nlp','data science'
]

def extract_skills(text):
    skills_found = []
    for skill in SKILLS:
        if skill in text:
            skills_found.append(skill)
    return list(set(skills_found))
