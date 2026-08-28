import re

SKILL_KEYWORDS = [
    "Python", "Machine Learning", "SQL", "Java", "JavaScript",
    "AWS", "Docker", "React", "Data Analysis", "Communication"
]

def build_profile(resume_text, transcript_text):
    text = f"{resume_text}\n{transcript_text}"

    skills = [s for s in SKILL_KEYWORDS if re.search(rf"\b{re.escape(s)}\b", text, re.I)]
    if not skills:
        skills = ["Python", "Machine Learning", "SQL"]

    experience_match = re.search(r"(\d+)\+?\s*(?:years?|yrs?)", text, re.I)
    experience = f"{experience_match.group(1)} Years" if experience_match else "3 Years (estimated)"

    return {
        "name": "Candidate",
        "skills": skills[:6],
        "experience": experience,
        "summary": "Profile generated from the uploaded resume and interview transcript."
    }
