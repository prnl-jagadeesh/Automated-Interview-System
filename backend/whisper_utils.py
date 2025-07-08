from transformers import pipeline
import tempfile
import os
from typing import Optional

# Load Whisper model via Hugging Face Transformers
# This will use the "openai/whisper-base" checkpoint
asr_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-base")

def save_audio_tempfile(audio_data: bytes, suffix: str = ".wav") -> str:
    """
    Save raw audio bytes to a temporary file for Whisper to process.

    Args:
        audio_data (bytes): Incoming audio byte stream
        suffix (str): File extension (e.g., '.wav')

    Returns:
        str: Path to the saved temporary audio file
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(audio_data)
        return tmp.name

def transcribe_audio(audio_data: bytes, cleanup: bool = True) -> Optional[str]:
    """
    Transcribe audio using Hugging Face Whisper model.

    Args:
        audio_data (bytes): Raw audio bytes
        cleanup (bool): Whether to delete the temp audio file after processing

    Returns:
        Optional[str]: Transcribed text if successful, else None
    """
    audio_path = save_audio_tempfile(audio_data)
    try:
        result = asr_pipeline(audio_path)
        return result.get("text")
    finally:
        if cleanup and os.path.exists(audio_path):
            os.remove(audio_path)