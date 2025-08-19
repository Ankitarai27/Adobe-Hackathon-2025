# backend/app/routers/insights.py
from fastapi import APIRouter, Body
from app.services.insights_generator import get_insights
import os
import fitz  # PyMuPDF

router = APIRouter()

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

@router.get("/")
def default_insights():
    return {"message": "Send a POST with context or use persona/pdf first."}

@router.post("/")
def generate_insights(context: str = Body(None, embed=True), filename: str = Body(None)):
    # If user directly sends context
    if context:
        return get_insights(context)

    # If a filename is provided (from /pdf/upload)
    if filename:
        file_path = os.path.join("storage/uploads", filename)
        if os.path.exists(file_path):
            text = extract_text_from_pdf(file_path)
            return get_insights(text)

    return {"error": "No context or valid file provided"}
