# eleven_tts.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVEN_API_KEY") or "sk_7df99d5b0c6e4e151d08344a36cb1ecf4e0136e236f92c44"
VOICE_ID = "P7vsEyTOpZ6YUTulin8m"  # Replace with your actual voice ID

def generate_tts_audio(text, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    res = requests.post(url, headers=headers, json=payload, stream=True)
    res.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in res.iter_content(chunk_size=4096):
            if chunk:
                f.write(chunk)
