import spacy
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download NLTK resources (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Load spaCy model (make sure you have downloaded en_core_web_sm)
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

# Expanded skill list organized by categories
SKILL_CATEGORIES = {
    "Programming Languages": {
        "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin", 
        "go", "rust", "typescript", "scala", "perl", "r", "matlab", "dart"
    },
    "Web Development": {
        "html", "css", "react", "angular", "vue.js", "node.js", "express", "django", 
        "flask", "jquery", "bootstrap", "sass", "less", "webpack", "redux", "next.js", 
        "gatsby", "svelte", "graphql", "rest api", "soap"
    },
    "Database": {
        "sql", "mysql", "postgresql", "mongodb", "firebase", "oracle", "sqlite", 
        "redis", "cassandra", "dynamodb", "mariadb", "elasticsearch", "nosql"
    },
    "Cloud & DevOps": {
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", 
        "ansible", "circleci", "github actions", "travis ci", "devops", "ci/cd"
    },
    "Data Science & ML": {
        "machine learning", "deep learning", "nlp", "data analysis", "pandas", 
        "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "computer vision", 
        "data mining", "statistics", "big data", "hadoop", "spark", "tableau", 
        "power bi", "data visualization"
    },
    "Mobile Development": {
        "android", "ios", "react native", "flutter", "xamarin", "swift", "kotlin", "objective-c"
    },
    "Tools & Version Control": {
        "git", "github", "gitlab", "bitbucket", "subversion", "jira", "confluence", 
        "trello", "scrum", "agile", "kanban", "slack"
    },
    "Testing": {
        "selenium", "junit", "pytest", "jest", "mocha", "cypress", "testng", 
        "automated testing", "manual testing", "qa", "tdd", "bdd"
    },
    "Soft Skills": {
        "leadership", "teamwork", "communication", "problem solving", "critical thinking",
        "time management", "project management", "creative thinking", "adaptability",
        "conflict resolution", "negotiation", "presentation", "public speaking"
    }
}

# Create a flat list of all skills for matching
ALL_SKILLS = set()
for category, skills in SKILL_CATEGORIES.items():
    ALL_SKILLS.update(skills)

# Headers/keywords to exclude when extracting organizations
EXCLUDE_ORG = {
    "education", "skills", "experience", "projects", "certifications",
    "summary", "objective", "positions", "responsibility", "contact", 
    "references", "interests", "hobbies", "achievements"
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
            if len(words) >= 2 and sum(1 for word in words if word and word[0].isupper()) >= 2:
                # Exclude lines that are too long (likely a title or header)
                if len(words) <= 5:
                    return " ".join(words)
    
    # Fallback to spaCy NER for PERSON entities at the beginning
    doc = nlp(" ".join([line.strip() for line in lines[:10]]))
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
            
    return "Name Not Found"

def extract_organizations(text):
    """
    Improved organization extraction with context analysis and filtering.
    """
    doc = nlp(text)
    
    # Get all ORG entities
    org_candidates = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            # Exclude common section headers, short tokens, and lowercase orgs
            org_text = ent.text.strip()
            if (org_text.lower() not in EXCLUDE_ORG and 
                len(org_text) > 2 and 
                any(c.isupper() for c in org_text)):
                
                # Check for context - look for work experience indicators nearby
                context_window = text[max(0, ent.start_char-100):min(len(text), ent.end_char+100)]
                context_indicators = ["work", "experience", "employed", "position", "job", "company"]
                
                if any(indicator in context_window.lower() for indicator in context_indicators):
                    org_candidates.append((org_text, 2))  # Higher score for orgs with good context
                else:
                    org_candidates.append((org_text, 1))  # Lower score for orgs without clear context
    
    # Count frequencies and prioritize by context score
    org_counter = Counter()
    for org, score in org_candidates:
        org_counter[org] += score
    
    # Return organizations sorted by score (most relevant first)
    return [org for org, _ in org_counter.most_common(10)]

def extract_entities(text):
    """
    Extracts the candidate's name, organizations, education, and key dates from the resume text.
    """
    name = extract_name(text)
    organizations = extract_organizations(text)
    
    # Extract education entities
    education = []
    doc = nlp(text)
    
    # Look for education keywords and surrounding text
    education_keywords = ["bachelor", "master", "phd", "degree", "diploma", "university", 
                        "college", "school", "institute", "certification"]
    
    sentences = sent_tokenize(text)
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in education_keywords):
            # Look for institutions in that sentence
            sent_doc = nlp(sentence)
            for ent in sent_doc.ents:
                if ent.label_ == "ORG":
                    education.append(ent.text)
    
    # Extract key dates (like work experience duration)
    date_pattern = r"(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{4}\s+(-|to|–|—|\s+)\s+(Present|Current|Now|Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)(\s+\d{4})?"
    dates = re.findall(date_pattern, text)
    timeline = [" ".join(d[0:]).strip() for d in dates]
    
    return {
        "Names": [name], 
        "Organizations": organizations,
        "Education": list(set(education)),
        "Timeline": timeline
    }

def extract_skills(text):
    """
    Extracts skills by matching words in the resume text against a predefined skills set.
    Returns categorized skills with confidence scores.
    """
    text_lower = text.lower()
    
    # Initialize result dict
    categorized_skills = {category: [] for category in SKILL_CATEGORIES}
    
    # For each skill category, look for matching skills in the text
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            # Check if the skill appears as a whole word or phrase
            skill_pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(skill_pattern, text_lower):
                # Calculate confidence based on number of occurrences and position in text
                occurrences = len(re.findall(skill_pattern, text_lower))
                position_score = 1.0 if skill in text_lower[:len(text_lower)//3] else 0.7
                confidence = min(0.7 + (occurrences * 0.1), 1.0) * position_score
                
                categorized_skills[category].append({
                    "skill": skill.capitalize(),
                    "confidence": round(confidence, 2)
                })
    
    # Return flat list for backward compatibility
    flat_skills = [skill_info["skill"] for category in categorized_skills.values() 
                  for skill_info in category]
    
    return flat_skills, categorized_skills

def extract_experience(text):
    """
    Extract work experience details including job titles and duration.
    """
    # Common job title patterns
    job_title_patterns = [
        r'(Senior|Junior|Lead|Principal|Chief|Head|Staff|Software|Data|Product|Project|Program|Technical|Executive)\s+(Developer|Engineer|Scientist|Analyst|Manager|Director|Architect|Designer|Consultant|Officer)',
        r'(Frontend|Backend|Full Stack|Full-Stack|DevOps|Cloud|Machine Learning|AI|ML|QA|Test)\s+(Developer|Engineer|Specialist)',
        r'(Software|Application|System|Web|Mobile)\s+(Developer|Engineer)',
        r'(CEO|CTO|CFO|COO|CIO|CISO|VP|Director|Manager|Lead|Head|Supervisor)'
    ]
    
    job_titles = []
    for pattern in job_title_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                job_titles.append(" ".join(match))
            else:
                job_titles.append(match)
    
    # Extract experience duration
    experience_pattern = r'(\d+)\+?\s+(year|yr|month)s?\s+(of)?\s+(experience|exp)'
    experience_matches = re.findall(experience_pattern, text.lower())
    
    experience_years = 0
    for match in experience_matches:
        try:
            amount = int(match[0])
            unit = match[1]
            if 'year' in unit or 'yr' in unit:
                experience_years = max(experience_years, amount)
            elif 'month' in unit:
                experience_years = max(experience_years, amount / 12)
        except:
            pass
    
    return {
        "job_titles": list(set(job_titles)),
        "years_of_experience": experience_years
    }

def calculate_resume_score(resume_text, job_description=None):
    """
    Calculate a resume score based on various factors.
    Score range is 0-100 with breakdown by category.
    """
    # Extract all the information
    flat_skills, categorized_skills = extract_skills(resume_text)
    entities = extract_entities(resume_text)
    experience_info = extract_experience(resume_text)
    
    # Initialize score components
    score_components = {
        "skills_diversity": 0,
        "experience_quality": 0,
        "education": 0,
        "organization_prestige": 0,
        "job_relevance": 0
    }
    
    # 1. Skills diversity score (0-25)
    # Count non-empty skill categories
    non_empty_categories = sum(1 for category in categorized_skills.values() if category)
    total_skills = sum(len(skills) for skills in categorized_skills.values())
    
    score_components["skills_diversity"] = min(25, (non_empty_categories * 4) + (total_skills * 0.5))
    
    # 2. Experience quality score (0-25)
    # Based on years of experience and number of job titles
    years = experience_info["years_of_experience"]
    titles = len(experience_info["job_titles"])
    
    experience_score = min(15, years * 3) + min(10, titles * 2)
    score_components["experience_quality"] = experience_score
    
    # 3. Education score (0-15)
    education_count = len(entities.get("Education", []))
    score_components["education"] = min(15, education_count * 5)
    
    # 4. Organization prestige score (0-15)
    # Simply based on number of recognized organizations
    org_count = len(entities.get("Organizations", []))
    score_components["organization_prestige"] = min(15, org_count * 3)
    
    # 5. Job relevance score (0-20) - only if job description is provided
    if job_description:
        job_skills = extract_skills(job_description)[0]
        matched_skills = set(s.lower() for s in flat_skills) & set(s.lower() for s in job_skills)
        match_percentage = len(matched_skills) / max(1, len(job_skills))
        score_components["job_relevance"] = min(20, match_percentage * 25)
    else:
        # If no job description, distribute the 20 points to other categories
        score_components["skills_diversity"] += 5
        score_components["experience_quality"] += 5
        score_components["education"] += 5
        score_components["organization_prestige"] += 5
    
    # Calculate total score
    total_score = sum(score_components.values())
    
    # Ensure score is between 0 and 100
    total_score = max(0, min(100, total_score))
    
    return {
        "total_score": round(total_score),
        "components": {k: round(v) for k, v in score_components.items()}
    }

def get_improvement_suggestions(resume_text, job_description):
    """
    Generate detailed improvement suggestions based on the resume and job description.
    """
    # Extract information from both documents
    resume_flat_skills, resume_categorized_skills = extract_skills(resume_text)
    job_flat_skills, job_categorized_skills = extract_skills(job_description)
    
    # Calculate missing skills
    resume_skills_lower = set(skill.lower() for skill in resume_flat_skills)
    job_skills_lower = set(skill.lower() for skill in job_flat_skills)
    missing_skills = job_skills_lower - resume_skills_lower
    
    # Categorize missing skills
    categorized_missing = {category: [] for category in SKILL_CATEGORIES}
    for skill in missing_skills:
        for category, skills in SKILL_CATEGORIES.items():
            if skill in skills:
                categorized_missing[category].append(skill.capitalize())
    
    # Remove empty categories
    categorized_missing = {k: v for k, v in categorized_missing.items() if v}
    
    # Look for keyword patterns in job description that might not be in the skills list
    job_doc = nlp(job_description)
    
    # Extract key phrases from job description (excluding stopwords)
    job_key_phrases = []
    for sentence in sent_tokenize(job_description):
        words = word_tokenize(sentence)
        filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
        for i in range(len(filtered_words) - 1):
            phrase = filtered_words[i] + " " + filtered_words[i+1]
            job_key_phrases.append(phrase)
    
    # Count frequencies
    phrase_counter = Counter(job_key_phrases)
    common_phrases = [phrase for phrase, count in phrase_counter.most_common(10) if count > 1]
    
    # Generate suggestions
    suggestions = []
    
    # 1. Missing skills suggestions
    if categorized_missing:
        for category, skills in categorized_missing.items():
            if skills:
                suggestions.append({
                    "type": "missing_skills",
                    "category": category,
                    "skills": skills,
                    "suggestion": f"Add {category} skills: {', '.join(skills)}"
                })
    
    # 2. Experience clarity suggestions
    experience_info = extract_experience(resume_text)
    if len(experience_info["job_titles"]) < 2:
        suggestions.append({
            "type": "experience",
            "suggestion": "Clearly highlight your job titles and roles to make your experience stand out"
        })
    
    # 3. Education clarity suggestions
    entities = extract_entities(resume_text)
    if not entities.get("Education", []):
        suggestions.append({
            "type": "education",
            "suggestion": "Add your educational background with degree and institution names"
        })
    
    # 4. Key phrases from job description not found in resume
    resume_text_lower = resume_text.lower()
    missing_phrases = [phrase for phrase in common_phrases if phrase not in resume_text_lower]
    if missing_phrases:
        suggestions.append({
            "type": "key_phrases",
            "phrases": missing_phrases[:5],  # Limit to top 5
            "suggestion": f"Consider incorporating these key phrases from the job description: {', '.join(missing_phrases[:5])}"
        })
    
    # 5. Length and structure suggestions
    word_count = len(resume_text.split())
    if word_count < 300:
        suggestions.append({
            "type": "length",
            "suggestion": "Your resume seems short. Consider adding more details to your experiences and achievements"
        })
    
    return suggestions