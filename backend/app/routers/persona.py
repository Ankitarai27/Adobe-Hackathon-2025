from fastapi import APIRouter, UploadFile, Form
from typing import List
from app.services import persona_engine
import tempfile

router = APIRouter()

@router.post("/analyze")
async def persona_analyze(
    files: List[UploadFile],
    persona: str = Form(...),
    job: str = Form(...)
):
    pdf_paths = []
    for f in files:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp.write(await f.read())
        tmp.close()
        pdf_paths.append({"filename": f.filename, "path": tmp.name})

    result = persona_engine.run_persona_analysis(pdf_paths, persona, job)
    return result
