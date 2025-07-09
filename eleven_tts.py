# eleven_tts.py
import requests, threading, io, pygame, os
from dotenv import load_dotenv

load_dotenv()
pygame.mixer.init()

API_KEY = os.getenv("ELEVEN_API_KEY") or "sk_7df99d5b0c6e4e151d08344a36cb1ecf4e0136e236f92c44"
VOICE_ID = "P7vsEyTOpZ6YUTulin8m"  # Change to your voice ID

def stop_tts():
    pygame.mixer.stop()

def _play_audio(audio_stream):
    stop_tts()
    audio = io.BytesIO(audio_stream)
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def speak_text(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": { "stability": 0.5, "similarity_boost": 0.75 }
    }
    try:
        res = requests.post(url, headers=headers, json=payload, stream=True)
        res.raise_for_status()
        threading.Thread(target=_play_audio, args=(res.content,), daemon=True).start()
    except Exception as e:
        print("❌ TTS Error:", e)
