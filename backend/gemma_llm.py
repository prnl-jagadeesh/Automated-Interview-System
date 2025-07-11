from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

# Load model and tokenizer once globally for performance
model_id = "google/gemma-7b-it"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.float16
)

def gemma_generate(prompt: str, max_tokens=300) -> str:
    """
    Utility function to generate text from prompt using Gemma model.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=max_tokens)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def parse_cv(cv_text):
    """
    Parses raw CV/resume text into structured JSON-like format.
    """
    prompt = open("models/prompts/cv_parser_prompt.txt").read().strip()
    full_prompt = f"{prompt}\n\n{cv_text}"
    result = gemma_generate(full_prompt)
    return result

def generate_questions(cv_json: dict, intro_text: str):
    """
    Generates interview questions based on parsed CV and self-introduction.
    """
    prompt_template = open("models/prompts/question_generator_prompt.txt").read().strip()

    cv_summary = f"""
Name: {cv_json.get('name')}
Skills: {', '.join(cv_json.get('skills', []))}
Experience: {cv_json.get('experience')}
Education: {cv_json.get('education')}
"""
    full_prompt = f"""{prompt_template}

Candidate Details:
{cv_summary}

Self-Introduction:
{intro_text}

Generate 2 questions:
"""

    result = gemma_generate(full_prompt)
    return result

def evaluate_answer(question: str, answer: str):
    """
    Evaluate a candidate's answer to a question and assign score and feedback.
    """
    prompt = open("models/prompts/evaluation_prompt.txt").read().strip()
    full_prompt = f"""{prompt}

Question: {question}
Answer: {answer}"""

    result = gemma_generate(full_prompt)
    
    lines = result.strip().split("\n")
    score_line = next((line for line in lines if "score" in line.lower()), "")
    feedback_line = next((line for line in lines if "feedback" in line.lower()), "")

    try:
        score = int(''.join(filter(str.isdigit, score_line)))
    except:
        score = None

    return {
        "question": question,
        "answer": answer,
        "score": score,
        "feedback": feedback_line.strip()
    }