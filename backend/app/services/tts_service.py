import os
from openai import AzureOpenAI

def text_to_speech(text: str, filename="output.mp3"):
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-02-01",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    deployment = os.getenv("AZURE_TTS_DEPLOYMENT", "tts")  # default: 'tts'

    result = client.audio.speech.create(
        model=deployment,
        voice="alloy",  # configurable voice
        input=text
    )

    with open(filename, "wb") as f:
        f.write(result.read())

    return filename
