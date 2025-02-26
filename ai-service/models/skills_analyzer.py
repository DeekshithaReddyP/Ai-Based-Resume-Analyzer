import spacy
import re

# Load spaCy model (make sure you have downloaded en_core_web_lg)
nlp = spacy.load("en_core_web_sm")

# Define a common set of skills (all in lowercase for matching)
COMMON_SKILLS = {
    "python", "java", "c", "c++", "sql", "javascript", "react", "html", "css",
    "git", "excel", "tableau", "machine learning", "deep learning", "nlp",
    "data analysis", "r", "flask", "django", "github", "aws"
}

# Headers/keywords to exclude when extracting organizations
EXCLUDE_ORG = {
    "education", "skills", "experience", "projects", "certifications",
    "summary", "objective", "positions", "responsibility"
}

def extract_name(text):
    """
    Heuristically extract the candidate's name from the first few non-empty lines.
    Looks for a line with at least two words that are capitalized.
    """
    lines = text.splitlines()
    for line in lines[:5]:
        line = line.strip()
        if line:
            words = line.split()
            # Check if at least two words start with an uppercase letter
            if len(words) >= 2 and sum(1 for word in words if word[0].isupper()) >= 2:
                return " ".join(words)
    return "Name Not Found"

def extract_entities(text):
    """
    Extracts the candidate's name and organizations from the resume text.
    Uses a dedicated function for the name and spaCy's NER for organizations.
    """
    name = extract_name(text)
    doc = nlp(text)
    orgs = set()
    for ent in doc.ents:
        if ent.label_ == "ORG":
            # Exclude common section headers and short tokens
            if ent.text.lower() not in EXCLUDE_ORG and len(ent.text) > 2:
                orgs.add(ent.text.strip())
    return {"Names": [name], "Organizations": list(orgs)}

def extract_skills(text):
    """
    Extracts skills by matching words in the resume text against a predefined skills set.
    The text is lowered for matching, and found skills are capitalized in the output.
    """
    text_lower = text.lower()
    skills_found = {skill.capitalize() for skill in COMMON_SKILLS if skill in text_lower}
    return list(skills_found)
