import { useState, useEffect } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import './App.css';
import UploadSection from './components/UploadSection';
import ResultsSection from './components/ResultsSection';
import LoadingSpinner from './components/LoadingSpinner';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HeroSection from './components/HeroSection';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeSection, setActiveSection] = useState('upload');

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [activeSection, loading]);

  const handleSubmit = async (file, jobDescription) => {
    setLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('job_description', jobDescription);
      
      // Show toast for better UX
      toast.loading('Analyzing your resume...', { id: 'analyzeToast' });
      
      const response = await fetch('https://ai-based-resume-analyzer.onrender.com/analyze/', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      setResults(data);
      setActiveSection('results');
      
      toast.success('Analysis complete!', { id: 'analyzeToast' });
    } catch (err) {
      console.error('Error:', err);
      toast.error(`Failed to analyze resume: ${err.message}`, { id: 'analyzeToast' });
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setResults(null);
    setActiveSection('upload');
  };

  return (
    <div className="app-container">
      <Toaster position="top-center" />
      <Navbar />
      
      <main>
        {activeSection === 'upload' && !loading && (
          <>
            <HeroSection />
            <section className="content-section">
              <UploadSection onSubmit={handleSubmit} />
            </section>
          </>
        )}
        
        {loading && (
          <section className="content-section">
            <LoadingSpinner />
          </section>
        )}
        
        {activeSection === 'results' && results && !loading && (
          <section className="content-section results-page">
            <div className="results-header">
              <h2>Resume Analysis Results</h2>
              <button 
                className="reset-button" 
                onClick={resetAnalysis}
              >
                Analyze Another Resume
              </button>
            </div>
            <ResultsSection results={results} />
          </section>
        )}
      </main>
      
      <Footer />
    </div>
  );
}

export default App;
