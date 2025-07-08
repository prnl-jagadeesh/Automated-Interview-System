## This project is a full-stack AI-powered interview evaluation system that:
- Parses resumes (PDF/DOCX/TXT)
- Accepts self-introduction via voice
- Generates relevant questions using Gemma LLM
- Evaluates answers using LLM with score and feedback


## 🔧 Tech Stack
- **Backend:** FastAPI + HuggingFace (Whisper + Gemma)
- **Frontend:** ReactJS (CV upload, audio record, Q&A)
- **Model APIs:** HuggingFace `google/gemma-7b-it`, Whisper ASR

## 🚀 How to Run

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🧪 API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload-cv` | POST (file) | Upload and parse resume |
| `/transcribe` | POST (file) | Upload voice and return transcription |
| `/generate-questions` | POST (form) | Generate questions using CV and intro |
| `/evaluate-answer` | POST (form) | Evaluate answer and return score |


## 📂 Folder Structure
```

ai-interview-system/
├── backend/
│   ├── main.py (FastAPI)
│   ├── whisper_utils.py
│   └── gemma_llm.py
├── frontend/ (React)
│   └── App.js
├── models/
│   └── prompts/
│       ├── cv_parser_prompt.txt
│       └── question_generator_prompt.txt
├── uploads/
│   └── (CVs, audio)
└── README.md


backend/
├── main.py
├── whisper_utils.py
├── gemma_llm.py
├── models/prompts/*.txt
└── utils/file_utils.py

frontend/
├── src/components/
│   ├── UploadCV.js
│   ├── RecordIntro.js
│   ├── QuestionDisplay.js
│   └── Scorecard.js
└── App.js
```

## ✅ Example Flow
1. Upload resume
2. Record self-introduction
3. View AI-generated questions
4. Type or speak your answers
5. View feedback + total score