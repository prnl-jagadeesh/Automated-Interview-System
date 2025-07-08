import fitz  # PyMuPDF
import docx

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a PDF byte stream using PyMuPDF.
    """
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])

def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts text from a DOCX file using python-docx.
    """
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])