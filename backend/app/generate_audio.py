import os
import requests

AZURE_TTS_KEY = os.getenv("AZURE_TTS_KEY")
AZURE_TTS_ENDPOINT = os.getenv("AZURE_TTS_ENDPOINT")
AZURE_TTS_DEPLOYMENT = os.getenv("AZURE_TTS_DEPLOYMENT", "tts")

def generate_audio(text: str, output_path: str):
    if not AZURE_TTS_KEY or not AZURE_TTS_ENDPOINT:
        #  Mock Mode: create dummy MP3 content
        print("⚠️ Azure TTS credentials not found — running in MOCK mode")
        with open(output_path, "wb") as f:
            f.write(b"FAKE_MP3_AUDIO_CONTENT")  # Just a placeholder
        return

    url = f"{AZURE_TTS_ENDPOINT}/openai/deployments/{AZURE_TTS_DEPLOYMENT}/audio/speech?api-version=2024-02-15-preview"
    headers = {
        "api-key": AZURE_TTS_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "input": text,
        "voice": "en-US-JennyMultilingualNeural",
        "response_format": "mp3"
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception(f"Audio generation failed: {response.status_code} {response.text}")

    with open(output_path, "wb") as f:
        f.write(response.content)
