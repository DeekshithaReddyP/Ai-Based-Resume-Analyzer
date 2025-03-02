import React from 'react';
import './ScoreCircle.css';

function ScoreCircle({ score, size = 150, strokeWidth = 10 }) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  // Assuming score is between 0 and 100
  const percent = score;
  const offset = circumference - (percent / 100) * circumference;
  const center = size / 2;

  return (
    <svg className="score-circle" width={size} height={size}>
      {/* Background circle */}
      <circle
        className="score-circle-bg"
        stroke="#e5e7eb"
        strokeWidth={strokeWidth}
        fill="transparent"
        r={radius}
        cx={center}
        cy={center}
      />
      {/* Progress circle */}
      <circle
        className="score-circle-progress"
        stroke="var(--primary)"
        strokeWidth={strokeWidth}
        fill="transparent"
        r={radius}
        cx={center}
        cy={center}
        strokeDasharray={circumference}
        strokeDashoffset={offset}
      />
      {/* Centered Score Text with counter-rotation */}
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        alignmentBaseline="middle"
        className="score-circle-text"
        transform={`rotate(90, ${center}, ${center})`}
      >
        {score}
      </text>
    </svg>
  );
}

export default ScoreCircle;
