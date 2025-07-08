import React, { useState } from 'react';
import UploadCV from './components/UploadCV';
import RecordIntro from './components/RecordIntro';
import QuestionDisplay from './components/QuestionDisplay';
import Scorecard from './components/Scorecard';
import axios from 'axios';

function App() {
  const [parsedCV, setParsedCV] = useState(null);
  const [introText, setIntroText] = useState('');
  const [questions, setQuestions] = useState([]);
  const [evaluations, setEvaluations] = useState([]);

  const generateQuestions = async () => {
    const response = await axios.post('http://localhost:8000/generate-questions', {
      cv: JSON.stringify(parsedCV),
      intro: introText
    });
    setQuestions(response.data.questions || response.data); // in case it's a raw array
  };

  const evaluateAnswers = async (answers) => {
    const results = [];
    for (let item of answers) {
      const res = await axios.post('http://localhost:8000/evaluate-answer', {
        question: item.question,
        answer: item.answer
      });
      results.push(res.data);
    }
    setEvaluations(results);
  };

  return (
    <div>
      <h2>AI Interview System</h2>

      {!parsedCV && <UploadCV onParsed={setParsedCV} />}
      {parsedCV && !introText && <RecordIntro onTranscription={setIntroText} />}
      {parsedCV && introText && questions.length === 0 && (
        <button onClick={generateQuestions}>Generate Questions</button>
      )}
      {questions.length > 0 && evaluations.length === 0 && (
        <QuestionDisplay questions={questions} onSubmitAnswer={evaluateAnswers} />
      )}
      {evaluations.length > 0 && <Scorecard evaluations={evaluations} />}
    </div>
  );
}

export default App;
