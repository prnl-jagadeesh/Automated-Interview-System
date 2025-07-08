import React from 'react';

const Scorecard = ({ evaluations }) => {
  if (!evaluations || evaluations.length === 0) return null;

  const totalScore = evaluations.reduce((sum, item) => sum + (item.score || 0), 0);
  const averageScore = (totalScore / evaluations.length).toFixed(1);

  let verdict = 'Rejected';
  if (averageScore >= 8) verdict = 'Ideal Candidate';
  else if (averageScore >= 5) verdict = 'Borderline';

  return (
    <div>
      <h3>Evaluation Results</h3>
      {evaluations.map((item, index) => (
        <div key={index} style={{ borderBottom: '1px solid #ccc', marginBottom: '1rem' }}>
          <p><strong>Q{index + 1}:</strong> {item.question}</p>
          <p><strong>Your Answer:</strong> {item.answer}</p>
          <p><strong>Score:</strong> {item.score}/10</p>
          <p><strong>Feedback:</strong> {item.feedback}</p>
        </div>
      ))}
      <hr />
      <h4>Total Score: {totalScore} / {evaluations.length * 10}</h4>
      <h4>Verdict: <span style={{ color: verdict === 'Ideal Candidate' ? 'green' : verdict === 'Borderline' ? 'orange' : 'red' }}>{verdict}</span></h4>
    </div>
  );
};

export default Scorecard;
