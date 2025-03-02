import { useState } from 'react';
import './ResultsSection.css'; 

function AccordionSection({ title, children, defaultExpanded = false }) {
  const [expanded, setExpanded] = useState(defaultExpanded);

  return (
    <div className="accordion-section">
      <div
        className="accordion-header"
        onClick={() => setExpanded(!expanded)}
        role="button"
        tabIndex="0"
        aria-expanded={expanded}
      >
        <h3>{title}</h3>
        <span className="accordion-icon">{expanded ? '−' : '+'}</span>
      </div>
      {expanded && <div className="accordion-content">{children}</div>}
    </div>
  );
}

export default AccordionSection;
