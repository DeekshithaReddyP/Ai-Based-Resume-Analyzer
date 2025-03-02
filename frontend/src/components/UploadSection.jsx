import { useState } from 'react';
import './UploadSection.css';

function UploadSection({ onSubmit }) {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [dragging, setDragging] = useState(false);
  const [fileName, setFileName] = useState('');
  const [error, setError] = useState('');

  const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB in bytes

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    handleFile(selectedFile);
  };

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;
    
    // Check file type
    const validTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];
    if (!validTypes.includes(selectedFile.type)) {
      setError('Please upload a PDF or DOCX file');
      setFile(null);
      setFileName('');
      return;
    }
    
    // Validate file size (max 5MB)
    if (selectedFile.size > MAX_FILE_SIZE) {
      setError('File size must be less than 5MB');
      setFile(null);
      setFileName('');
      return;
    }
    
    // If all checks pass, clear error and set file
    setError('');
    setFile(selectedFile);
    setFileName(selectedFile.name);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    handleFile(droppedFile);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please upload a resume file');
      return;
    }
    
    onSubmit(file, jobDescription);
  };

  return (
    <div className="upload-section">
      <div className="upload-container">
        <form onSubmit={handleSubmit}>
          <label 
            className={`file-upload-area ${dragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            aria-label="Resume file upload area. Click or drag and drop your resume."
            tabIndex="0"
          >
            <input 
              type="file" 
              onChange={handleFileChange}
              accept=".pdf,.docx"
              className="file-input"
              id="resume-upload"
              aria-label="Choose a resume file"
            />
            
            {!file ? (
              <div className="upload-prompt">
                <div className="upload-icon">
                  {/* SVG icon */}
                </div>
                <p className="upload-text">
                  <span className="primary-text">Click to upload</span> or drag and drop
                </p>
                <p className="upload-format">PDF or DOCX (max. 5MB)</p>
              </div>
            ) : (
              <div className="file-info">
                <div className="file-icon">
                  {/* SVG icon */}
                </div>
                <span className="file-name">{fileName}</span>
                <button 
                  type="button" 
                  className="change-file"
                  onClick={(e) => {
                    e.stopPropagation();
                    setFile(null);
                    setFileName('');
                  }}
                  aria-label="Change file"
                >
                  Change
                </button>
              </div>
            )}
          </label>
          
          {error && <p className="error-message" role="alert">{error}</p>}
          
          <div className="job-description-area">
            <label htmlFor="job-description">Job Description (optional)</label>
            <textarea
              id="job-description"
              placeholder="Paste the job description here to get a personalized match analysis..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={6}
              aria-label="Job Description input"
            ></textarea>
          </div>
          
          <button 
            type="submit" 
            className="analyze-button"
            disabled={!file}
            aria-label="Analyze Resume"
          >
            <span className="button-icon">
              {/* SVG icon */}
            </span>
            Analyze Resume
          </button>
        </form>
      </div>
    </div>
  );
}

export default UploadSection;
