from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os, shutil, sqlite3, datetime, uuid
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text

from collections import Counter
import re
from app.generate_audio import generate_audio

# ✅ Initialize App
app = FastAPI()

# ✅ Directories
UPLOAD_DIR = "uploads"
AUDIO_DIR = "audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# ✅ CORS
frontend_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "").split(",")
    if origin.strip()
]
frontend_origins.extend(["http://localhost:3000", "http://127.0.0.1:3000"])
allow_origins = list(dict.fromkeys(frontend_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve Static Files
app.mount("/pdfs", StaticFiles(directory=UPLOAD_DIR), name="pdfs")
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

# ✅ SQLite Setup
conn = sqlite3.connect("uploads.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    role TEXT,
    jobdesc TEXT,
    uploaded_at TEXT
)
""")
conn.commit()


STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "from", "your", "have", "are", "was",
    "were", "will", "shall", "into", "than", "then", "their", "there", "about", "also",
    "only", "through", "using", "between", "within", "across", "while", "where", "when",
    "what", "which", "who", "whom", "why", "how", "a", "an", "in", "on", "of", "to", "is",
    "it", "as", "or", "by", "be", "at", "we", "you", "our", "they", "can"
}


def build_snippets_from_pdf(file_path: str, max_snippets: int = 8, query_text: str = ""):
    """
    Extract section/snippet candidates from a PDF.
    Strategy:
    1) Try structured text extraction with PyMuPDF (best for born-digital PDFs).
    2) If nothing meaningful is found, fall back to pdfminer full-text extraction.
    """
    doc = fitz.open(file_path)
    snippets = []

    candidates = []
    section_title = "Untitled Section"
    query_terms = {
        term.lower()
        for term in re.findall(r"[A-Za-z]{3,}", query_text or "")
        if term.lower() not in STOPWORDS
    }

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text:
                        continue
                    is_heading = (
                        text.isupper() or
                        (len(text.split()) <= 8 and text.endswith(":")) or
                        span["size"] > 12
                    )
                    if is_heading:
                        section_title = text
                    else:
                        sentences = text.split(". ")
                        snippet_text = ". ".join(sentences[:3]) + ("..." if len(sentences) > 3 else "")
                        if snippet_text.strip():
                            candidates.append({
                                "section": section_title or "Untitled Section",
                                "snippet": snippet_text,
                                "page": page_num
                            })


    # Rank candidates by relevance + content richness and pick diverse pages
    if candidates:
        def score(item):
            words = re.findall(r"[A-Za-z]{3,}", item["snippet"].lower())
            overlap = sum(1 for w in words if w in query_terms) if query_terms else 0
            richness = min(len(words), 60) / 60
            return (overlap * 2) + richness

        ranked = sorted(candidates, key=score, reverse=True)
        used_pages = set()
        for item in ranked:
            if len(snippets) >= max_snippets:
                break
            # keep at most 2 snippets per page to avoid page-1 domination
            page_count = sum(1 for s in snippets if s["page"] == item["page"])
            if page_count >= 2 and len(used_pages) < 3:
                continue
            snippets.append(item)
            used_pages.add(item["page"])

    # Fallback for scanned/odd-layout files where block parsing misses useful text
    extraction_mode = "pymupdf"
    if len(snippets) == 0:
        raw_text = extract_text(file_path) or ""
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        for idx, line in enumerate(lines[:max_snippets], start=1):
            snippets.append({
                "section": "Extracted Text",
                "snippet": line[:320],
                "page": idx
            })
        if snippets:
            extraction_mode = "pdfminer_fallback"

    return snippets, extraction_mode

# ✅ Upload PDF
@app.post("/upload")
async def upload_file(file: UploadFile, role: str = Form(...), jobdesc: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    cursor.execute(
        "INSERT INTO uploads (filename, role, jobdesc, uploaded_at) VALUES (?, ?, ?, ?)",
        (file.filename, role, jobdesc, datetime.datetime.now().isoformat())
    )
    conn.commit()

    return {"message": "File uploaded", "filename": file.filename}

# ✅ List Uploads
@app.get("/uploads/{role}")
async def list_uploads_by_role(role: str):
    cursor.execute("SELECT id, filename, role, jobdesc, uploaded_at FROM uploads WHERE role=? ORDER BY uploaded_at DESC", (role,))
    rows = cursor.fetchall()
    return [
        {"id": r[0], "filename": r[1], "role": r[2], "jobdesc": r[3], "uploaded_at": r[4]}
        for r in rows
    ]

# ✅ Snippet Extractor
@app.get("/snippets/{filename}")
async def extract_snippets(filename: str, role: str = "", job: str = ""):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}


    snippets, extraction_mode = build_snippets_from_pdf(
        file_path,
        max_snippets=10,
        query_text=f"{role} {job}".strip()
    )

    if not snippets:
        return {
            "file": filename,
            "snippets": [],
            "extraction_mode": extraction_mode,
            "warning": "No extractable text found. This PDF may be scanned/image-only and needs OCR."
        }

    return {"file": filename, "snippets": snippets, "extraction_mode": extraction_mode}


@app.get("/insights/{filename}")
async def generate_insights(filename: str, role: str = "", job: str = ""):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    snippets, extraction_mode = build_snippets_from_pdf(
        file_path, max_snippets=16, query_text=f"{role} {job}".strip()
    )
    combined = " ".join(item["snippet"] for item in snippets)
    words = [
        w.lower() for w in re.findall(r"[A-Za-z]{4,}", combined)
        if w.lower() not in STOPWORDS
    ]
    top_keywords = [k for k, _ in Counter(words).most_common(8)]
    highlights = [item["snippet"] for item in snippets[:5]]

    return {
        "file": filename,
        "extraction_mode": extraction_mode,
        "highlights": highlights,
        "top_keywords": top_keywords,
        "total_snippets_considered": len(snippets)
    }

# ✅ Snippet to Audio
@app.get("/snippets/audio/{filename}")
async def snippets_audio(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    snippet_objects, extraction_mode = build_snippets_from_pdf(file_path, max_snippets=12)
    snippets = [item.get("snippet", "").strip() for item in snippet_objects if item.get("snippet", "").strip()]
    combined_text = "\n".join(snippets[:10])

    if not combined_text:
        return {
            "error": "No extractable text found for audio generation. PDF may require OCR.",
            "extraction_mode": extraction_mode
        }

    audio_filename = f"snippet_audio_{uuid.uuid4().hex[:6]}.mp3"
    output_path = os.path.join(AUDIO_DIR, audio_filename)

    try:
        generate_audio(combined_text, output_path)
        return {
            "audio_url": f"/audio/{audio_filename}",
            "message": "Audio generated from snippets"
        }
    except Exception as e:
        return {"error": str(e)}
