// Navbar.jsx
import { useState, useEffect } from 'react';
import './Navbar.css';

function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 10;
      if (isScrolled !== scrolled) {
        setScrolled(isScrolled);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [scrolled]);

  const handleNavClick = (e, targetId) => {
    e.preventDefault();
    const element = document.getElementById(targetId);
    if (element) {
      const yOffset = -80; 
      const yPosition = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({ top: yPosition, behavior: 'smooth' });
    }
    setMenuOpen(false);
  };

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="navbar-container">
        <div className="logo">
          <span className="logo-icon">📄</span>
          <span className="logo-text">
            <span className="logo-primary">Resume</span>
            <span className="logo-secondary">Analyzer</span>
          </span>
        </div>

        <div className="nav-right">
          <div className={`nav-links ${menuOpen ? 'active' : ''}`}>
            <a
              href="#home"
              className="nav-link active"
              onClick={(e) => handleNavClick(e, 'home')}
            >
              Home
            </a>
            <a
              href="#features"
              className="nav-link"
              onClick={(e) => handleNavClick(e, 'features')}
            >
              Features
            </a>
            <a
              href="#how-it-works"
              className="nav-link"
              onClick={(e) => handleNavClick(e, 'how-it-works')}
            >
              How It Works
            </a>
            <a
              href="#contact"
              className="nav-link contact-link"
              onClick={(e) => handleNavClick(e, 'contact')}
            >
              Contact Us
            </a>
          </div>
          <button
            className={`menu-toggle ${menuOpen ? 'active' : ''}`}
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Toggle menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
