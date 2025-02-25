from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import uvicorn
import os
from models.resume_extractor import extract_text_from_file
from models.skills_analyzer import extract_entities, extract_skills
from models.job_matcher import match_resume_with_job

app = FastAPI()

@app.post("/analyze/")
async def analyze_resume(
    file: UploadFile = File(...), 
    job_description: str = Form("")
):
    """API to analyze a resume, extract insights, and suggest missing skills."""
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)  # Ensure the 'temp' directory exists

    file_path = os.path.join(temp_dir, file.filename)
    
    # Save the uploaded file temporarily
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text from the resume
    resume_text = extract_text_from_file(file_path)

    # Extract basic insights
    entities = extract_entities(resume_text)
    skills = extract_skills(resume_text)

    response = {
        "Extracted Name": entities.get("Names", []),
        "Extracted Organizations": entities.get("Organizations", []),
        "Extracted Skills": skills
    }

    # If a job description is provided, compute matched/missing skills
    if job_description.strip():
        skill_match = match_resume_with_job(resume_text, job_description)
        response["Matched Skills"] = skill_match.get("Matched Skills", [])
        response["Missing Skills (Suggested Improvements)"] = skill_match.get("Missing Skills (Suggested Improvements)", [])
    else:
        response["Matched Skills"] = []
        response["Missing Skills (Suggested Improvements)"] = []
        response["Message"] = "Job description not provided. Please provide one for skill matching suggestions."

    # Clean up the temporary file
    os.remove(file_path)

    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  
    uvicorn.run(app, host="0.0.0.0", port=port)
