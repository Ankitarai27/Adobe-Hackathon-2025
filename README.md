# Adobe Hackathon 2025 — Intelligent PDF Insight & Podcast Generator

An end-to-end full-stack project for **Adobe Hackathon 2025** that turns static PDFs into role-aware, quick-consumption knowledge.

---

## 1) Heading Summary

This project helps users upload PDFs, organize them by persona/job context, read extracted snippet highlights, and optionally generate audio narration (“podcast mode”) from those snippets.

If you want a one-line summary:

> **Upload documents → extract smart snippets → listen to insights as audio.**

---

## 2) Project Summary

### What problem this solves
Long PDFs are slow to consume. This app reduces reading time by extracting meaningful snippet-level content and presenting it in a lightweight analysis interface.

### What the app delivers
- Fast PDF upload and storage.
- Role-based document listing (`/uploads/{role}`).
- Snippet extraction from document pages.
- Audio generation from extracted text for hands-free review.
- Frontend UX for upload + analysis + podcast playback.

---

## 3) What is unique in this project

This project is not just a PDF uploader. Its unique combination is:

1. **Persona-aware flow**
   - Uploads are tied to role/job context so analysis can be grouped by use-case.

2. **Hybrid reading + listening experience**
   - Users can inspect snippets visually and generate audio from the same source.

3. **Practical architecture for hackathon speed**
   - Local filesystem + SQLite for quick iteration.
   - Docker + Supervisor support for running frontend and backend together.

4. **Clear path to production**
   - Current prototype architecture can be upgraded to managed DB/object storage without redesigning user flow.

---

## 4) Core Flow (End-to-End)

1. User opens frontend and selects persona/job parameters.
2. User uploads one or more PDFs.
3. Backend stores file in `uploads/` and metadata in `uploads.db`.
4. Analysis page fetches role-based file list.
5. User selects a file.
6. Backend extracts section/snippet text using PyMuPDF.
7. Frontend displays extracted snippet cards.
8. User clicks podcast mode.
9. Backend generates MP3 in `audio/` and returns a URL.
10. Frontend plays generated audio in browser.

---

## 5) Tech Stack

### Frontend
- **Next.js 15** (App Router)
- **React 19**
- **TailwindCSS**
- **react-icons**

### Backend
- **FastAPI**
- **Uvicorn**
- **PyMuPDF (`fitz`)** for PDF text extraction
- **SQLite** for upload metadata

### Runtime / Deployment
- **Docker** (single-image full-stack build)
- **Supervisor** to run both backend + frontend in one container

---

## 6) Project Structure

```text
Adobe-Hackathon-2025/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── generate_audio.py
│   │   ├── routers/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   ├── uploads/                  # runtime PDF storage
│   ├── audio/                    # runtime MP3 storage
│   └── uploads.db                # SQLite metadata DB
├── frontend/
│   ├── app/
│   ├── services/
│   │   └── api.js
│   ├── package.json
│   └── ...
├── Dockerfile
├── supervisord.conf
└── README.md
```

---

## 7) Project Structure Explanation

### `backend/app/main.py`
Main FastAPI entrypoint. Defines upload/list/snippet/audio endpoints, static file mounts, and DB table setup.

### `backend/app/generate_audio.py`
Audio generation helper used by snippet-audio route.

### `backend/uploads/`
Stores uploaded PDF files at runtime.

### `backend/audio/`
Stores generated audio files at runtime.

### `backend/uploads.db`
SQLite database containing upload metadata (`filename`, `role`, `jobdesc`, `uploaded_at`).

### `frontend/app/`
Next.js app pages, including upload and analysis flows.

### `frontend/services/api.js`
Client-side API utility functions and base URL handling.

### `Dockerfile` + `supervisord.conf`
Single-container setup that builds frontend and runs frontend + backend simultaneously.

---

## 8) API Overview

Base URL (local): `http://127.0.0.1:8000`

### `POST /upload`
Uploads PDF + metadata.

- **Content-Type:** `multipart/form-data`
- **Fields:**
  - `file` (pdf)
  - `role` (string)
  - `jobdesc` (string)

**Success response (example):**
```json
{
  "message": "File uploaded",
  "filename": "my-doc.pdf"
}
```

### `GET /uploads/{role}`
Returns files uploaded for a specific role (latest first).

### `GET /snippets/{filename}`
Extracts up to snippet entries from the PDF with section context and page number.

### `GET /snippets/audio/{filename}`
Generates an MP3 from extracted snippet text and returns the audio URL.

### Static file routes
- `/pdfs/<filename>`
- `/audio/<filename>`

---

## 9) Backend Details

### Backend responsibilities
- Accept and persist uploads.
- Maintain upload metadata in SQLite.
- Parse PDF text blocks and detect probable headings.
- Generate short snippet chunks for quick preview.
- Convert snippet text to audio file.
- Expose static paths for PDFs and MP3 playback.

### Important design notes
- CORS currently allows localhost frontend origins.
- Data persistence is local (good for prototype/hackathon, limited for scale).
- Snippet extraction is heuristic-based (heading/size/text-shape rules).

---

## 10) Frontend Details

### Frontend responsibilities
- Collect role/job context and file uploads.
- Call backend upload endpoint.
- Fetch role-filtered uploaded docs.
- Fetch and render snippet list.
- Trigger podcast generation endpoint.
- Render audio player for generated MP3.

### UX pages
- **Upload page:** drag/drop + multi-file upload + current/history context.
- **Analysis page:** selectable documents, snippet cards, podcast mode button.

---

## 11) Key Features (Everything in one list)

- Persona/job-aware uploads.
- PDF upload pipeline with metadata tracking.
- Role-based document retrieval.
- Snippet extraction from PDF pages.
- Podcast mode: text-to-audio generation.
- Static serving for PDFs/audio.
- FastAPI + Next.js full-stack architecture.
- Single-container deployment support.

---

## 12) Setup (Local Development)

## Prerequisites
- Python 3.11+
- Node.js 18+
- npm
- ffmpeg (recommended for audio path)

## Step-by-step setup

### Step 1 — Clone
```bash
git clone <your-repo-url>
cd Adobe-Hackathon-2025
```

### Step 2 — Start backend (terminal A)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 3 — Configure frontend env
Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000
```

### Step 4 — Start frontend (terminal B)
```bash
cd frontend
npm install
npm run dev
```

### Step 5 — Access app
- Frontend: `http://localhost:3000`
- Backend docs: `http://127.0.0.1:8000/docs`

---

## 13) Deployment Logic (Step-by-Step)

## Option A: Single Docker deployment (quick start)

### Step 1 — Build image
```bash
docker build -t adobe-hackathon-2025:latest .
```

### Step 2 — Run container
```bash
docker run --name adobe-hackathon \
  -p 3000:3000 -p 8000:8000 \
  -d adobe-hackathon-2025:latest
```

### Step 3 — Verify
- `http://localhost:3000`
- `http://localhost:8000/docs`

### Step 4 — Persist data volumes (recommended)
```bash
docker run --name adobe-hackathon \
  -p 3000:3000 -p 8000:8000 \
  -v $(pwd)/backend/uploads:/app/backend/uploads \
  -v $(pwd)/backend/audio:/app/backend/audio \
  -v $(pwd)/backend/uploads.db:/app/backend/uploads.db \
  -d adobe-hackathon-2025:latest
```

## Option B: Split production deployment (recommended at scale)

### Backend deploy
- Deploy FastAPI service (Render/Railway/Fly/EC2).
- Set service to expose port 8000 (or platform port binding).
- Add CORS allowlist for your frontend domain.

### Frontend deploy
- Deploy Next.js app (Vercel/Netlify).
- Set env: `NEXT_PUBLIC_API_BASE=https://<backend-domain>`.
- Redeploy frontend with updated env.

### Why split is better
- Independent scaling.
- Better reliability and release control.
- Cleaner observability.

---

## 14) Differences in this project vs generic PDF apps

- Supports **persona + job metadata** as first-class context.
- Includes **audio generation** from extracted snippets.
- Built as a **full-stack workflow**, not a standalone parser script.
- Already includes **containerized all-in-one deployment path**.

---

## 15) Known Gaps / Current Limitations

- Local SQLite/file storage is not ideal for multi-instance production.
- Authentication/authorization not enforced for uploads.
- Validation limits (file size/type/deep sanitization) can be strengthened.
- Some frontend helper code and backend routes should be kept fully aligned as API evolves.

---

## 16) Suggested Next Improvements

1. Add API contract tests.
2. Add upload validations and content-security checks.
3. Move storage to object storage + managed DB.
4. Add authentication and per-user document isolation.
5. Add background jobs for large document processing.
6. Add richer insight generation (summary, theme clustering, action items).

---

## 17) Production Hardening Checklist

- [ ] Managed DB instead of SQLite.
- [ ] Object storage for files/audio.
- [ ] Strict CORS and auth.
- [ ] Rate limiting + input validation.
- [ ] Health checks + centralized logging.
- [ ] CI/CD with lint/test/build/security scan.

---

## 18) Troubleshooting

- **Cannot connect frontend to backend:** verify `NEXT_PUBLIC_API_BASE` and backend status.
- **CORS errors in browser:** include deployed frontend URL in FastAPI CORS allowlist.
- **No audio output:** verify ffmpeg and TTS dependencies in runtime.
- **Data disappears after container restart:** use Docker volumes or external persistent storage.

---

## 19) License

Add your preferred license (MIT / Apache-2.0 / proprietary) based on your team policy.
