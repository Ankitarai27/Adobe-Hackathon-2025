import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_insights(context: str):
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Context: {context}

    Generate three sections in JSON format:
    {{
        "insights": ["..."],
        "contradictions": ["..."],
        "inspirations": ["..."]
    }}
    """

    response = model.generate_content(prompt)

    try:
        import json
        data = json.loads(response.text)
    except Exception:
        data = {"insights": [response.text], "contradictions": [], "inspirations": []}

    return data
