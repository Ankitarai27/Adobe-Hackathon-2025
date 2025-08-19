from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os, shutil, sqlite3, datetime, uuid
import fitz  # PyMuPDF
from app.generate_audio import generate_audio

# ✅ Initialize App
app = FastAPI()

# ✅ Directories
UPLOAD_DIR = "uploads"
AUDIO_DIR = "audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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
async def extract_snippets(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    doc = fitz.open(file_path)
    snippets = []
    section_title = "Untitled Section"

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
                        len(text.split()) <= 8 and text.endswith(":") or
                        span["size"] > 12
                    )
                    if is_heading:
                        section_title = text
                    else:
                        sentences = text.split(". ")
                        snippet_text = ". ".join(sentences[:3]) + ("..." if len(sentences) > 3 else "")
                        snippets.append({
                            "section": section_title or "Untitled Section",
                            "snippet": snippet_text,
                            "page": page_num
                        })
                    if len(snippets) >= 5:
                        break
                if len(snippets) >= 5:
                    break
            if len(snippets) >= 5:
                break
        if len(snippets) >= 5:
            break

    return {"file": filename, "snippets": snippets}

# ✅ Snippet to Audio
@app.get("/snippets/audio/{filename}")
async def snippets_audio(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    doc = fitz.open(file_path)
    snippets = []
    section_title = "Untitled Section"

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
                        snippets.append(snippet_text)
    combined_text = "\n".join(snippets[:10])

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
