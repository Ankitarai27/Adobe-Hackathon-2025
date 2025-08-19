from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os, shutil, sqlite3, datetime
import fitz  # PyMuPDF

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve uploaded PDFs
app.mount("/pdfs", StaticFiles(directory=UPLOAD_DIR), name="pdfs")

# ✅ SQLite
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

@app.get("/uploads/{role}")
async def list_uploads_by_role(role: str):
    cursor.execute("SELECT id, filename, role, jobdesc, uploaded_at FROM uploads WHERE role=? ORDER BY uploaded_at DESC", (role,))
    rows = cursor.fetchall()
    return [
        {"id": r[0], "filename": r[1], "role": r[2], "jobdesc": r[3], "uploaded_at": r[4]}
        for r in rows
    ]

@app.get("/snippets/{filename}")
async def extract_snippets(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    doc = fitz.open(file_path)
    snippets = []
    section_title = "Untitled Section"

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]  # structured text
        for b in blocks:
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text:
                        continue

                    # --- Heading detection logic (Round 1A style) ---
                    is_heading = (
                        text.isupper() or
                        len(text.split()) <= 8 and text.endswith(":") or
                        span["size"] > 12  # heuristic: large font = heading
                    )

                    if is_heading:
                        section_title = text
                    else:
                        # Extract snippet (first ~3 sentences)
                        sentences = text.split(". ")
                        snippet_text = ". ".join(sentences[:3]) + "..."
                        snippets.append({
                            "section": section_title or "Untitled Section",
                            "snippet": snippet_text,
                            "page": page_num
                        })

                    if len(snippets) >= 5:  # max 5 snippets
                        break
                if len(snippets) >= 5:
                    break
            if len(snippets) >= 5:
                break
        if len(snippets) >= 5:
            break

    return {"file": filename, "snippets": snippets}
