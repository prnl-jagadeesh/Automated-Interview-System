from transformers import pipeline

# Load Gemma 7B instruction-tuned model from Hugging Face
gemma = pipeline("text-generation", model="google/gemma-7b-it", device_map="auto")

def parse_cv(cv_text):
    """
    Parse CV text using a prompt and return structured output.
    """
    prompt = open("models/prompts/cv_parser_prompt.txt").read().strip()
    full_prompt = f"{prompt}{cv_text}"
    result = gemma(full_prompt, max_new_tokens=300)[0]["generated_text"]
    return result

def generate_questions(cv_json: dict, intro_text: str):
    """
    Generate 2 interview questions based on parsed CV and self-introduction.
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

    result = gemma(full_prompt, max_new_tokens=300)[0]["generated_text"]
    return result

def evaluate_answer(question: str, answer: str):
    """
    Evaluate a candidate's answer to a question and assign score and feedback.

    Args:
        question (str): The interview question
        answer (str): The candidate's response

    Returns:
        dict: Contains numeric score and feedback string
    """
    prompt = open("backend/models/prompts/evaluation_prompt.txt").read().strip()

    full_prompt = f"""{prompt}

Question: {question}
Answer: {answer}"""

    result = gemma(full_prompt, max_new_tokens=300)[0]["generated_text"]

    lines = result.strip().split("")
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