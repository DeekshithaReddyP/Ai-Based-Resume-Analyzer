import { useEffect, useState } from 'react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev < 100) {
          return prev + 10;
        }
        clearInterval(interval);
        return 100;
      });
    }, 500);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="loading-container">
      <div className="spinner-wrapper">
        <div className="spinner">
          <div className="spinner-inner"></div>
        </div>
      </div>
      <h3 className="loading-text">Analyzing your resume...</h3>
      <p className="loading-subtext">Our AI is extracting skills and matching to job requirements</p>
      
      <div className="progress-bar-container">
        <div className="progress-bar" style={{ width: `${progress}%` }}></div>
      </div>
      
      <div className="loading-steps">
        <div className="loading-step active">
          <div className="step-indicator">
            <div className="step-icon-container">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
          </div>
          <div className="step-content">
            <p className="step-title">Parsing resume</p>
          </div>
        </div>
        
        <div className="loading-step active">
          <div className="step-indicator">
            <div className="step-icon-container">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
          </div>
          <div className="step-content">
            <p className="step-title">Extracting skills</p>
          </div>
        </div>
        
        <div className="loading-step current">
          <div className="step-indicator">
            <div className="step-spinner"></div>
          </div>
          <div className="step-content">
            <p className="step-title">Analyzing content</p>
          </div>
        </div>
        
        <div className="loading-step">
          <div className="step-indicator">
            <div className="step-number">4</div>
          </div>
          <div className="step-content">
            <p className="step-title">Preparing recommendations</p>
          </div>
        </div>
        
        <div className="loading-step">
          <div className="step-indicator">
            <div className="step-number">5</div>
          </div>
          <div className="step-content">
            <p className="step-title">Finalizing results</p>
          </div>
        </div>
      </div>
      
      <div className="loading-tips">
        <h4>Resume Tips</h4>
        <p>Did you know? Including quantifiable achievements can increase your interview chances by 40%</p>
      </div>
    </div>
  );
}

export default LoadingSpinner;