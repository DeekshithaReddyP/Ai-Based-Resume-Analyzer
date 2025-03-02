from models.skills_analyzer import extract_skills, calculate_resume_score, get_improvement_suggestions

def match_resume_with_job(resume_text, job_description):
    """
    Enhanced job matching with detailed analysis, score, and improvement suggestions.
    """
    
    if not job_description.strip():
        return {
            "Matched Skills": [],
            "Missing Skills": [],
            "Score": 0,
            "Analysis": "Job description not provided"
        }
    
    # Extract skills from both resume and job description
    resume_flat_skills, resume_categorized = extract_skills(resume_text)
    job_flat_skills, job_categorized = extract_skills(job_description)
    
    # Convert to lowercase for comparison
    resume_skills_lower = set(skill.lower() for skill in resume_flat_skills)
    job_skills_lower = set(skill.lower() for skill in job_flat_skills)
    
    # Find matched and missing skills
    matched = list(resume_skills_lower & job_skills_lower)
    missing = list(job_skills_lower - resume_skills_lower)
    
    # Calculate resume score
    score = calculate_resume_score(resume_text, job_description)
    
    # Get detailed improvement suggestions
    suggestions = get_improvement_suggestions(resume_text, job_description)
    
    # Generate overall analysis text
    match_percentage = len(matched) / max(1, len(job_skills_lower)) * 100
    
    if match_percentage >= 80:
        analysis = "Strong match! Your resume aligns well with this job description."
    elif match_percentage >= 60:
        analysis = "Good match. With a few additions, your resume would be very well suited for this position."
    elif match_percentage >= 40:
        analysis = "Moderate match. Consider enhancing your resume with the missing skills to improve your chances."
    else:
        analysis = "Limited match. This role may require significant skill development or better highlighting of your relevant experience."
    
    # Add score interpretation
    total_score = score["total_score"]
    if total_score >= 85:
        score_analysis = "Excellent resume score. Your resume is very competitive for this position."
    elif total_score >= 70:
        score_analysis = "Good resume score. Your resume demonstrates solid qualifications for this role."
    elif total_score >= 50:
        score_analysis = "Average resume score. Consider implementing the suggestions to strengthen your application."
    else:
        score_analysis = "Below average resume score. Your resume may need significant improvements for this position."
    
    return {
        "Matched Skills": [skill.capitalize() for skill in matched],
        "Missing Skills": [skill.capitalize() for skill in missing],
        "Score": {
            "TotalScore": score["total_score"],
            "Breakdown": score["components"],
            "Interpretation": score_analysis
        },
        "Analysis": {
            "Summary": analysis,
            "MatchPercentage": round(match_percentage, 1),
            "Suggestions": suggestions
        }
    }