from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
import uuid
from eleven_tts import generate_tts_audio

app = Flask(__name__)

WEBHOOK_URL = "https://shaileshk.app.n8n.cloud/webhook/voicebot2"
chat_history = []
listening = False
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/voice", methods=["POST"])
def voice():
    global chat_history
    data = request.get_json()
    text = data.get("text", "")
    chat_history.append({"role": "user", "content": text})
    try:
        res = requests.post(WEBHOOK_URL, json={"history": chat_history}, timeout=15)
        res.raise_for_status()
        reply = res.json().get("response", "No reply received")
    except Exception as e:
        print("❌ Error contacting webhook:", e)
        reply = "Sorry, I couldn't reach the server."
    chat_history.append({"role": "assistant", "content": reply})
    # Generate TTS audio and save to file
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)
    try:
        generate_tts_audio(reply, audio_path)
        audio_url = f"/audio/{audio_filename}"
    except Exception as e:
        print("❌ TTS audio generation failed:", e)
        audio_url = None
    return jsonify({"reply": reply, "audio_url": audio_url})

@app.route("/audio/<filename>")
def audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

@app.route("/history")
def history():
    return jsonify(chat_history)

@app.route("/start", methods=["POST"])
def start_chat():
    global listening
    listening = True
    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop_chat():
    global listening
    listening = False
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
