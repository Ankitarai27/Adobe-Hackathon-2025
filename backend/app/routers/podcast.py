from fastapi import APIRouter, Body
from app.services.tts_service import text_to_speech

router = APIRouter()

@router.post("/")
def generate_audio(text: str = Body(..., embed=True)):
    file_path = text_to_speech(text)
    return {"audio_file": file_path}
