# Adobe Hackathon 2025 — Document Intelligence Platform

A full-stack application built for **Adobe Hackathon 2025** that lets users:
- choose a persona/job context,
- upload PDF documents,
- extract section-based text snippets,
- generate audio narration (“podcast mode”) from document snippets.

The project uses a **FastAPI backend** and a **Next.js frontend**, and can run either locally (2 processes) or in one Docker container (via Supervisor).

---

## 1) What this project does

### Core user flow
1. User selects a role/persona and job context in the UI.
2. User uploads one or more PDFs.
3. Backend stores upload metadata in SQLite and serves files statically.
4. User opens analysis page and selects an uploaded file.
5. Backend extracts snippets from the PDF (using PyMuPDF).
6. Optional: backend generates MP3 audio narration from snippets.

### Features currently implemented
- PDF upload with `role` + `jobdesc` metadata.
- Fetch uploaded files by role.
- Extract section/snippet previews from a selected PDF.
- Generate and serve MP3 from extracted text.
- Frontend upload and analysis pages.

---

## 2) Tech stack

- **Frontend:** Next.js 15, React 19, TailwindCSS
- **Backend:** FastAPI, Uvicorn, PyMuPDF
- **Storage:** SQLite (`uploads.db`) + local filesystem (`uploads/`, `audio/`)
- **Process orchestration (Docker mode):** Supervisor

---

## 3) Project structure

```text
Adobe-Hackathon-2025/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app + API endpoints
│   │   ├── generate_audio.py       # Audio generation helper
│   │   ├── routers/                # Additional router modules
│   │   ├── services/               # Business/service layer modules
│   │   └── utils/                  # Utility helpers
│   ├── requirements.txt
│   ├── uploads/                    # Uploaded PDF files (runtime)
│   ├── audio/                      # Generated audio files (runtime)
│   └── uploads.db                  # SQLite DB (runtime)
├── frontend/
│   ├── app/                        # Next.js app router pages/layout
│   ├── services/
│   │   └── api.js                  # Frontend API helper
│   ├── package.json
│   └── ...
├── Dockerfile                      # Single-container full stack build
├── supervisord.conf                # Runs backend + frontend together
└── README.md
```

---

## 4) API overview (backend)

Base URL (local): `http://127.0.0.1:8000`

- `POST /upload`
  - multipart form-data: `file`, `role`, `jobdesc`
  - response: uploaded filename + status message

- `GET /uploads/{role}`
  - returns uploads filtered by role, newest first

- `GET /snippets/{filename}`
  - extracts and returns section/snippet previews from PDF

- `GET /snippets/audio/{filename}`
  - generates MP3 from extracted snippet text
  - returns `audio_url` under `/audio/...`

- static files
  - `/pdfs/<filename>`
  - `/audio/<filename>`

---

## 5) Local development setup (recommended)

## Prerequisites
- Python 3.11+
- Node.js 18+
- npm
- ffmpeg installed (required for audio workflows)

## Step-by-step

### Step 1 — Clone repository
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

### Step 3 — Configure frontend API URL
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

### Step 5 — Open app
- Frontend: `http://localhost:3000`
- Backend docs: `http://127.0.0.1:8000/docs`

---

## 6) Deployment logic (step-by-step)

Below is the practical deployment approach for this codebase.

## Option A — Deploy as a single Docker container (quickest)

This repo already includes a Dockerfile that builds frontend + backend and starts both with Supervisor.

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
- `http://localhost:3000` (frontend)
- `http://localhost:8000/docs` (backend)

### Step 4 — Persist runtime data (recommended)
Uploads, audio, and SQLite should survive container restarts:
```bash
docker run --name adobe-hackathon \
  -p 3000:3000 -p 8000:8000 \
  -v $(pwd)/backend/uploads:/app/backend/uploads \
  -v $(pwd)/backend/audio:/app/backend/audio \
  -v $(pwd)/backend/uploads.db:/app/backend/uploads.db \
  -d adobe-hackathon-2025:latest
```

---

## Option B — Production-grade split deployment (recommended for scale)

Deploy frontend and backend separately.

### Architecture logic
1. **Frontend (Next.js)** on Vercel/Netlify.
2. **Backend (FastAPI)** on Render/Railway/Fly.io/EC2.
3. **Set frontend env:** `NEXT_PUBLIC_API_BASE=https://<backend-domain>`
4. **Enable CORS** in backend for frontend domain.
5. **Use persistent storage** (block/object storage + managed DB) instead of local files/SQLite for multi-instance reliability.

### Why split is better
- independent scaling (UI vs API workloads),
- easier zero-downtime updates,
- cleaner observability and failure isolation.

---

## 7) Production hardening checklist

Before final deployment:

- [ ] Replace SQLite + local files with managed DB/storage for durability.
- [ ] Add file size/type validation and anti-malware scanning on uploads.
- [ ] Add auth (JWT/session) if data is private.
- [ ] Add request limits and timeout controls.
- [ ] Add structured logging and error monitoring.
- [ ] Add health endpoint and container health checks.
- [ ] Add CI pipeline (lint/test/build/image scan).
- [ ] Move secrets to secure env management.

---

## 8) Troubleshooting

- **Frontend can’t reach backend:** ensure `NEXT_PUBLIC_API_BASE` is set and backend is running.
- **CORS errors:** add deployed frontend URL to backend CORS `allow_origins`.
- **Audio generation fails:** confirm `ffmpeg` availability and TTS/audio dependencies.
- **Missing uploads after restart:** mount persistent volumes or use external storage.

---

## 9) Suggested next improvements

1. Fix API contract mismatch so all frontend upload-list calls align with backend endpoints.
2. Add tests for upload/snippet/audio endpoints.
3. Add role/job analytics dashboard.
4. Add background jobs for large PDF processing.
5. Add object storage support (S3/GCS/Azure Blob).

---

## License

Add your preferred license here (MIT/Apache-2.0/etc.).
