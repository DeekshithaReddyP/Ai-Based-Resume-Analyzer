from models.skills_analyzer import extract_skills

def match_resume_with_job(resume_text, job_description):
    """Compare extracted resume skills with job description skills and suggest improvements."""
    
    if not job_description.strip():
        return {
            "Matched Skills": [],
            "Missing Skills (Suggested Improvements)": []
        }
    
    # Extract skills from both resume and job description (normalized to lowercase)
    resume_skills = set(skill.lower().strip() for skill in extract_skills(resume_text))
    job_skills = set(skill.lower().strip() for skill in extract_skills(job_description))

    # Debug prints (check your server logs to verify extraction)
    print(f"Extracted Resume Skills: {resume_skills}")
    print(f"Extracted Job Skills: {job_skills}")

    matched = list(resume_skills & job_skills)
    missing = list(job_skills - resume_skills)

    return {
        "Matched Skills": [skill.capitalize() for skill in matched],
        "Missing Skills (Suggested Improvements)": [skill.capitalize() for skill in missing]
    }

if __name__ == "__main__":
    # Quick local test
    resume_text = "I have experience in Python, Machine Learning, and SQL."
    job_description = "Looking for a Python developer with Machine Learning and NLP experience."
    match_result = match_resume_with_job(resume_text, job_description)
    print(match_result)
