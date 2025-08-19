import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

NEGATIVE_KEYWORDS = [
    "rsvp", "www", "http", "address", "page", "form", "block", "fare",
    "parkway", "s.no", "name", "age", "single", "application", "grant"
]

def clean_text(text):
    text = text.strip()
    if not text or len(text) < 3:
        return ""
    return text

def is_heading_candidate(text):
    text_lower = text.lower()

    if any(neg in text_lower for neg in NEGATIVE_KEYWORDS):
        return False
    if text.endswith("."):
        return False
    if re.search(r"\d", text) and not re.match(r"^\d+(\.\d+)*", text):
        return False
    if "," in text:
        return False
    words = text.split()
    if len(words) == 1 and len(words[0]) < 4:
        return False
    if len(words) > 12:
        return False
    if text.startswith("•") or text.startswith("-"):
        return False
    return True

def determine_heading_level(text, size, h1_threshold, h2_threshold, h3_threshold):
    if re.match(r"^\d+\.\d+\.\d+", text):
        return "H3"
    elif re.match(r"^\d+\.\d+", text):
        return "H2"
    elif re.match(r"^\d+\.", text):
        return "H1"

    if size >= h1_threshold:
        return "H1"
    elif size >= h2_threshold:
        return "H2"
    elif size >= h3_threshold:
        return "H3"
    return None

def extract_headings_from_pdf(pdf_path: str):
    candidates = []
    title_candidates = []

    for page_num, page_layout in enumerate(extract_pages(pdf_path), start=0):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if hasattr(text_line, "get_text"):
                        text = clean_text(text_line.get_text())
                        if not text:
                            continue

                        font_size = 0
                        count = 0
                        for char in text_line:
                            if isinstance(char, LTChar):
                                font_size += char.size
                                count += 1
                        avg_font = font_size / count if count > 0 else 0

                        if avg_font > 10:
                            if page_num == 0:
                                title_candidates.append((text, avg_font))
                            if is_heading_candidate(text):
                                candidates.append((text, avg_font, page_num))

    # Detect title
    title = ""
    if title_candidates:
        title_candidates.sort(key=lambda x: x[1], reverse=True)
        title = title_candidates[0][0]

    if not candidates:
        return {"title": title, "outline": []}

    max_size = max(size for _, size, _ in candidates)
    h1_threshold = max_size * 0.8
    h2_threshold = max_size * 0.6
    h3_threshold = max_size * 0.4

    outline = []
    added = set()

    for text, size, page in candidates:
        if text in added:
            continue
        level = determine_heading_level(text, size, h1_threshold, h2_threshold, h3_threshold)
        if level:
            outline.append({"level": level, "text": text, "page": page})
            added.add(text)

    return {"title": title, "outline": outline}
