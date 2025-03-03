# Ai-Based-Resume-Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**AI-Based Resume Analyzer** is a full-stack application that analyzes resumes, extracts key information, computes a resume score, and provides job matching insights. The backend is built with FastAPI and NLTK, while the frontend is built with React (using Vite).

**Live Demo :**  
[https://ai-based-resume-analyzer.vercel.app/](https://ai-based-resume-analyzer.vercel.app/)

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **Resume Parsing:** Upload your resume (PDF or DOCX) for analysis.
- **Entity Extraction:** Automatically extracts personal details, education, experience, and organizations.
- **Skill Analysis:** Identifies and categorizes key skills from resumes.
- **Resume Scoring:** Calculates a resume score based on various criteria, visually displayed as a circular progress indicator.
- **Job Matching:** Compares your resume against a provided job description, highlighting matched and missing skills.
- **User-Friendly Interface:** A responsive frontend with intuitive interactions and clear visual feedback.

## Project Structure

```
Ai-Based-Resume-Analyzer/
├── ai-service/        # Backend application (FastAPI, NLTK)
├── frontend/          # Frontend application (React with Vite)
├── .gitignore         # Git ignore file
└── README.md          # Project documentation (this file)
```

## Getting Started

### Backend Setup

1. **Navigate to the backend folder:**
   ```bash
   cd ai-service
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the development server:**
   ```bash
   uvicorn app:app --reload
   ```
   The backend should now be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Frontend Setup

1. **Navigate to the frontend folder:**
   ```bash
   cd frontend
   ```
2. **Install dependencies:**
   ```bash
   npm install
   # or, if using yarn:
   yarn install
   ```
3. **Test the production build locally:**
   ```bash
   npm run build
   npm run preview
   ```
   The frontend will typically run at [http://localhost:5173](http://localhost:5173) (or another port as specified).


## Usage

1. Open the frontend application in your browser.
2. Upload your resume (PDF or DOCX) using the provided interface.
3. Optionally, paste a job description for a personalized analysis.
4. Click **Analyze Resume**.
5. View your analysis results, which include:
   - Personal Information (Name, Education, Experience)
   - Identified Skills
   - Organizations Mentioned
   - A visually appealing Resume Score displayed with a circular progress indicator
   - Job Match Analysis (matched and missing skills)
   - Additional recommendations and insights

## Contributing

Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Open a pull request describing your changes.
For major changes, please open an issue first to discuss what you would like to modify.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **[FastAPI](https://fastapi.tiangolo.com/):** For providing a robust backend framework.
- **[NLTK](https://www.nltk.org/):** For powerful natural language processing.
- **[React](https://reactjs.org/) & [Vite](https://vitejs.dev/):** For building a fast and interactive frontend.
- Thanks to all open-source contributors and the community for inspiration and support.

Feel free to adjust any sections to match your exact project setup or add any additional details you feel are important. This README should serve as a solid starting point for users and contributors alike.
