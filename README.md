# Adobe Hackathon 2025 – PDF Insights Project

This project is built for **Adobe Hackathon 2025 (Round 3)**.  
It allows users to **upload PDFs**, process them through a **FastAPI backend**, and view **insights and analysis** on a **Next.js frontend**.

---

## 📂 Project Structure
```bash
├── backend
│ ├── app
│ │ ├── routers/ # API routes
│ │ ├── services/ # Business logic (PDF processing, insights, etc.)
│ │ ├── utils/ # Helper functions
│ │ ├── init.py
│ │ └── main.py # FastAPI entry point
│ ├── uploads/ # Uploaded PDF files
│ ├── Dockerfile
│ ├── requirements.txt # Python dependencies
│ └── uploads.db # SQLite database (if used)
│
├── frontend
│ ├── app/ # Next.js pages/components
│ ├── public/ # Static assets
│ ├── services/ # API calls to backend
│ ├── package.json # Node.js dependencies
│ └── tailwind.config.js # TailwindCSS setup
```

---

##  Tech Stack

- **Backend**: FastAPI, Python  
- **Frontend**: Next.js, React, TailwindCSS   
- **Deployment**: Docker  

---

##  Features

- ✅ Upload PDF files  
- ✅ Fetch and display uploaded documents  
- 🔜 **Generate Insights** from PDFs (summary, key points, stats)
📊 Insights Feature (Work in Progress)

```bash 
    * Extract text from PDFs pdfplumber 
    * Process text using AI/ML (e.g., OpenAI, Gemini, HuggingFace)
    * Return structured insights as JSON
    * Display in frontend with summary + charts  
```

---

##  Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/<your-username>/Adobe-Hackathon-2025.git
cd Adobe-Hackathon-2025
```


2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

