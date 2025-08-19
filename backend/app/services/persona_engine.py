import os
import fitz
import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for i in range(len(doc)):
        text = doc[i].get_text()
        if text.strip():
            pages.append({"page_number": i + 1, "text": text.strip()})
    return pages

def chunk_and_rank(pages, doc_name, query, top_k=5):
    query_vec = model.encode([query])[0]
    scored_chunks = []

    for page in pages:
        for chunk in page["text"].split("\n\n"):
            clean_chunk = chunk.strip()
            if len(clean_chunk) < 50:
                continue
            chunk_vec = model.encode([clean_chunk])[0]
            score = cosine_similarity([query_vec], [chunk_vec])[0][0]
            scored_chunks.append({
                "document": doc_name,
                "page_number": page["page_number"],
                "text": clean_chunk,
                "score": float(score)
            })

    top_chunks = sorted(scored_chunks, key=lambda x: x["score"], reverse=True)[:top_k]
    return top_chunks

def persona_analysis(input_docs, persona, job):
    query = f"{persona} | {job}"
    all_chunks = []

    for doc in input_docs:
        filename = doc["filename"]
        pdf_path = os.path.join("input", filename)

        if not os.path.exists(pdf_path):
            continue

        pages = extract_text_by_page(pdf_path)
        top_chunks = chunk_and_rank(pages, filename, query, top_k=2)
        all_chunks.extend(top_chunks)

    # Now pick top 5 across all docs
    all_chunks = sorted(all_chunks, key=lambda x: x["score"], reverse=True)[:5]

    extracted_sections = []
    for idx, chunk in enumerate(all_chunks):
        extracted_sections.append({
            "document": chunk["document"],
            "section_title": chunk["text"].split("\n")[0][:100],
            "importance_rank": idx + 1,
            "page_number": chunk["page_number"]
        })

    return {
        "persona": persona,
        "job_to_be_done": job,
        "extracted_sections": extracted_sections,
        "timestamp": datetime.datetime.now().isoformat()
    }
