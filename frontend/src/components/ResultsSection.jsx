import AccordionSection from './AccordionSection';
import ScoreCircle from './ScoreCircle';
import './ResultsSection.css';

function ResultsSection({ results }) {
  const {
    name = [],
    organizations = [],
    education = [],
    experience = {},
    skills = [],
    categorized_skills = {},
    score = {},
    matched_skills = [],
    missing_skills = [],
    analysis = {}
  } = results;

  const displayName = name && name.length > 0 ? name[0] : "Unknown";

  return (
    <div className="results-section">
      <h2>Resume Analysis Results</h2>

      <AccordionSection title="Personal Information" defaultExpanded={true}>
        <div className="info-item">
          <div className="info-label">Name:</div>
          <div className="info-value">{displayName}</div>
        </div>
        {education.length > 0 && (
          <div className="info-item">
            <div className="info-label">Education:</div>
            <div className="info-value">
              {education.map((edu, idx) => (
                <div key={idx}>{edu}</div>
              ))}
            </div>
          </div>
        )}
        {experience.job_titles && (
          <div className="info-item">
            <div className="info-label">Experience:</div>
            <div className="info-value">
              {experience.job_titles.join(', ')}
              {experience.years_of_experience ? ` (${experience.years_of_experience} years)` : ''}
            </div>
          </div>
        )}
      </AccordionSection>

      <AccordionSection title="Skills Identified">
        {skills.length > 0 ? (
          <div className="skills-grid">
            {skills.map((skill, index) => (
              <div key={index} className="skill-tag">{skill}</div>
            ))}
          </div>
        ) : (
          <p className="no-data">No skills identified</p>
        )}
      </AccordionSection>

      <AccordionSection title="Organizations Mentioned">
        {organizations.length > 0 ? (
          <ul className="org-list">
            {organizations.map((org, index) => (
              <li key={index}>{org}</li>
            ))}
          </ul>
        ) : (
          <p className="no-data">No organizations identified</p>
        )}
      </AccordionSection>

      {score.TotalScore !== undefined && (
        <AccordionSection title="Resume Score">
          <div className="score-section">
            <ScoreCircle score={score.TotalScore} />
            <div className="score-details">
              {score.Breakdown && (
                <div className="score-breakdown">
                  {Object.entries(score.Breakdown).map(([key, value], index) => (
                    <div key={index} className="score-item">
                      <span className="score-label">{key}:</span>
                      <span className="score-value">{value}</span>
                    </div>
                  ))}
                </div>
              )}
              {score.Interpretation && (
                <p className="score-interpretation">{score.Interpretation}</p>
              )}
            </div>
          </div>
        </AccordionSection>
      )}

      {(matched_skills.length > 0 || missing_skills.length > 0) && (
        <AccordionSection title="Job Match Analysis">
          <div className="match-container">
            <div className="matched-skills">
              <h4>Skills You Have</h4>
              {matched_skills.length > 0 ? (
                <div className="skills-grid">
                  {matched_skills.map((skill, index) => (
                    <div key={index} className="skill-tag matched">
                      <span className="check-icon">✓</span> {skill}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="no-data">No matched skills</p>
              )}
            </div>
            <div className="missing-skills">
              <h4>Skills to Develop</h4>
              {missing_skills.length > 0 ? (
                <div className="skills-grid">
                  {missing_skills.map((skill, index) => (
                    <div key={index} className="skill-tag missing">{skill}</div>
                  ))}
                </div>
              ) : (
                <p className="no-data">Your resume covers all required skills!</p>
              )}
            </div>
          </div>
        </AccordionSection>
      )}

      {analysis && Object.keys(analysis).length > 0 && (
        <AccordionSection title="Additional Analysis">
          {analysis.Summary && (
            <p className="analysis-summary">{analysis.Summary}</p>
          )}
          {analysis.MatchPercentage !== undefined && (
            <p className="analysis-match">Match Percentage: {analysis.MatchPercentage}%</p>
          )}
          {analysis.Suggestions && analysis.Suggestions.length > 0 && (
            <div className="analysis-suggestions">
              <h4>Suggestions:</h4>
              <ul>
                {analysis.Suggestions.map((suggestion, index) => (
                  <li key={index}>{suggestion.suggestion}</li>
                ))}
              </ul>
            </div>
          )}
        </AccordionSection>
      )}
    </div>
  );
}

export default ResultsSection;
