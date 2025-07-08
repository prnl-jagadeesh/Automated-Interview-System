import React, { useState } from 'react';

const QuestionDisplay = ({ questions, onSubmitAnswer }) => {
  const [answers, setAnswers] = useState({});

  const handleChange = (index, value) => {
    setAnswers({ ...answers, [index]: value });
  };

  const handleSubmit = () => {
    const finalAnswers = questions.map((q, i) => ({
      question: q,
      answer: answers[i] || '',
    }));
    onSubmitAnswer(finalAnswers);
  };

  return (
    <div>
      <h4>Answer the following questions:</h4>
      {questions.map((q, index) => (
        <div key={index} style={{ marginBottom: '1rem' }}>
          <p><strong>Q{index + 1}:</strong> {q}</p>
          <textarea
            rows="4"
            cols="60"
            value={answers[index] || ''}
            onChange={(e) => handleChange(index, e.target.value)}
            placeholder="Type your answer here"
          />
        </div>
      ))}
      <button onClick={handleSubmit}>Submit Answers</button>
    </div>
  );
};

export default QuestionDisplay;
