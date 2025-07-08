from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from whisper_utils import transcribe_audio
from gemma_llm import parse_cv, generate_questions, evaluate_answer
from utils.file_utils import extract_text_from_pdf, extract_text_from_docx
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)

    elif filename.endswith(".docx"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        text = extract_text_from_docx(tmp_path)

    else:
        # Fallback to plain text decode
        text = content.decode("utf-8", errors="ignore")

    result = parse_cv(text)
    return {"parsed_cv": result}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_data = await file.read()
    result = transcribe_audio(audio_data)
    return {"transcript": result}

@app.post("/generate-questions")
async def generate(cv: str = Form(...), intro: str = Form(...)):
    import json
    parsed_cv = json.loads(cv)
    questions = generate_questions(parsed_cv, intro)
    return {"questions": questions}

@app.post("/evaluate-answer")
async def evaluate(question: str = Form(...), answer: str = Form(...)):
    result = evaluate_answer(question, answer)
    return result