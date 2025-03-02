import './HeroSection.css';

function HeroSection() {
  return (
    <section className="hero-section">
      <div className="hero-content">
        <h1 className="hero-title">
          <span className="title-highlight">AI-Powered</span> Resume Analysis
        </h1>
        <p className="hero-subtitle">
          Upload your resume, get instant insights, and discover how to improve your job prospects with our AI resume analyzer
        </p>
        <div className="hero-cta">
          <a href="#upload-resume" className="cta-button primary">
            Analyze Your Resume
          </a>
          <a href="#features" className="cta-button secondary">
            Explore Features
          </a>
        </div>
      </div>
      
      <div className="hero-features" id="features">
        <div className="feature-card">
          <div className="feature-icon skill-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
            </svg>
          </div>
          <h3>Skill Extraction</h3>
          <p>AI identifies your key skills from your resume automatically</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon match-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="m22 2-7 20-4-9-9-4 20-7z"></path>
            </svg>
          </div>
          <h3>Job Matching</h3>
          <p>Compare your resume with job descriptions for perfect matches</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon gap-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle><path d="M12 8v8"></path><path d="M8 12h8"></path>
            </svg>
          </div>
          <h3>Skill Gaps</h3>
          <p>Discover missing skills to improve your chances of landing the job</p>
        </div>
      </div>
      
      <div className="how-it-works" id="how-it-works">
        <h2>How It Works</h2>
        <div className="steps-container">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Upload Resume</h3>
            <p>Upload your PDF or DOCX resume file using our simple interface</p>
          </div>
          
          <div className="step-separator"></div>
          
          <div className="step">
            <div className="step-number">2</div>
            <h3>Add Job Description</h3>
            <p>Optionally paste a job description to compare with your skills</p>
          </div>
          
          <div className="step-separator"></div>
          
          <div className="step">
            <div className="step-number">3</div>
            <h3>Get AI Analysis</h3>
            <p>Our AI analyzes your resume and provides detailed insights</p>
          </div>
          
          <div className="step-separator"></div>
          
          <div className="step">
            <div className="step-number">4</div>
            <h3>Improve Your Resume</h3>
            <p>Use our suggestions to enhance your resume and increase job prospects</p>
          </div>
        </div>
      </div>
      
      <div className="upload-section-wrapper" id="upload-resume">
        <h2>Ready to Analyze Your Resume?</h2>
        <p>Upload your resume below and let our AI extract insights to help you land your dream job</p>
      </div>
    </section>
  );
}

export default HeroSection;