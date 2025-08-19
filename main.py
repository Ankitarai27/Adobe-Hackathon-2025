from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import json

app = FastAPI()

# Allow CORS for frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key="95094bfe86d74dfc91a6b0af1327e2ce")

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    pdf_bytes = await file.read()

    # ---- MOCK Adobe JSON ---- (replace with real Adobe Extract later)
    adobe_json = {
        "title": "Sample PDF",
        "outline": [
            {"level": "H1", "text": "Introduction", "page": 1},
            {"level": "H1", "text": "Methodology", "page": 2}
        ]
    }

    # Enriched JSON for Gemini
    enriched_json = {
        "persona": "College Student",
        "task": "Summarize and extract insights",
        "pdf_metadata": {
            "name": file.filename,
            "size_kb": len(pdf_bytes) // 1024,
        },
        "content": adobe_json
    }

    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"""
    You are given structured JSON from a PDF.

    Persona: {enriched_json['persona']}
    Task: {enriched_json['task']}
    PDF Metadata: {json.dumps(enriched_json['pdf_metadata'])}
    Content: {json.dumps(adobe_json)}

    Return a JSON object with:
    - "highlights": list of {{"title": str, "page": int, "snippet": str}}
    - "insights": {{
        "insights": list of strings,
        "contradictions": list of strings,
        "inspirations": list of strings
      }}
    """

    gemini_response = model.generate_content(prompt)

    # Try to parse JSON safely
    try:
        result = json.loads(gemini_response.text)
    except:
        # fallback if Gemini gave plain text
        result = {
            "highlights": [
                {"title": "Intro", "page": 1, "snippet": "Overview of document"}
            ],
            "insights": {
                "insights": ["Document covers compliance issues."],
                "contradictions": ["Section 2 conflicts with Section 5."],
                "inspirations": ["Consider restructuring methodology section."]
            }
        }

    return result
