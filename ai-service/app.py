from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from models.resume_extractor import extract_text_from_file
from models.skills_analyzer import extract_entities, extract_skills, extract_experience, calculate_resume_score
from models.job_matcher import match_resume_with_job
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import nltk
nltk.download('punkt')

app = FastAPI(
    title="Advanced Resume Analyzer AI",
    description="An API for analyzing resumes, extracting insights, and providing job matching analysis",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ResumeUploadResponse(BaseModel):
    name: List[str]
    organizations: List[str]
    education: List[str]
    experience: Dict[str, Any]
    skills: List[str]
    categorized_skills: Dict[str, List[Dict[str, Any]]]
    score: Dict[str, Any]
    matched_skills: Optional[List[str]] = []
    missing_skills: Optional[List[str]] = []
    analysis: Optional[Dict[str, Any]] = {}

@app.get("/")
def home():
    return {
        "message": "Advanced Resume Analyzer AI is running!",
        "version": "2.0.0",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Home endpoint"},
            {"path": "/analyze/", "method": "POST", "description": "Analyze a resume"},
            {"path": "/health", "method": "GET", "description": "Health check endpoint"}
        ]
    }

@app.get("/health")
def health_check():
    """Health check endpoint to verify service is running."""
    return {"status": "healthy"}

@app.post("/analyze/", response_model=ResumeUploadResponse)
async def analyze_resume(
    file: UploadFile = File(...), 
    job_description: str = Form("")
):
    """
    API to analyze a resume, extract insights, calculate score, and suggest improvements.
    
    - **file**: Resume file (PDF or DOCX)
    - **job_description**: Optional job description text for matching analysis
    """
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)  # Ensure the 'temp' directory exists

    file_path = os.path.join(temp_dir, file.filename)
    
    # Save the uploaded file temporarily
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text from the resume
    resume_text = extract_text_from_file(file_path)
    
    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not extract text from the provided file")

    # Extract basic insights
    entities = extract_entities(resume_text)
    experience_info = extract_experience(resume_text)
    flat_skills, categorized_skills = extract_skills(resume_text)
    
    # Calculate base resume score
    score = calculate_resume_score(resume_text)
    
    response = {
        "name": entities.get("Names", []),
        "organizations": entities.get("Organizations", []),
        "education": entities.get("Education", []),
        "experience": experience_info,
        "skills": flat_skills,
        "categorized_skills": categorized_skills,
        "score": score,
        "matched_skills": [],
        "missing_skills": [],
        "analysis": {}
    }

    # If a job description is provided, compute matched/missing skills and job-specific score
    if job_description.strip():
        match_results = match_resume_with_job(resume_text, job_description)
        response["matched_skills"] = match_results.get("Matched Skills", [])
        response["missing_skills"] = match_results.get("Missing Skills", [])
        response["score"] = match_results.get("Score")
        response["analysis"] = match_results.get("Analysis")
    else:
        response["analysis"] = {
            "Summary": "Job description not provided. For personalized analysis, please provide a job description."
        }

    # Clean up the temporary file
    os.remove(file_path)

    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  
    uvicorn.run(app, host="0.0.0.0", port=port)