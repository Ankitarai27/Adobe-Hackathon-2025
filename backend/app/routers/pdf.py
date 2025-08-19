# backend/app/routers/pdf.py
from fastapi import APIRouter, UploadFile, File
import os, shutil

router = APIRouter()
UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "path": file_path}

@router.get("/list")
async def list_pdfs():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}
