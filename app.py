from flask import Flask, render_template, request, jsonify
import threading
import time
import os
import requests
from eleven_tts import speak_text
from voice_recorder import record_voice

app = Flask(__name__)

WEBHOOK_URL = "https://shaileshk.app.n8n.cloud/webhook/voicebot2"
WAKE_WORDS = ["hi jarvis", "hey jarvis", "ok jarvis"]
STOP_WORDS = ["stop", "stop jarvis", "cancel"]

chat_history = []
listening = False
wake_detected = False


def voice_loop():
    global listening, wake_detected, chat_history
    print("🔴 Waiting for wake word...")

    while True:
        text = record_voice()
        if not text:
            continue

        print("👂 You said:", text)

        if not wake_detected and any(w in text.lower() for w in WAKE_WORDS):
            speak_text("Hello, I am Jarvis. How can I help you?")
            wake_detected = True
            listening = True
            continue

        if not wake_detected:
            print("❌ Wake word not detected. Ignoring...")
            continue

        if any(w in text.lower() for w in STOP_WORDS):
            speak_text("Okay, stopping now.")
            listening = False
            wake_detected = False
            chat_history = []
            break

        chat_history.append({"role": "user", "content": text})
        try:
            res = requests.post(WEBHOOK_URL, json={"history": chat_history}, timeout=15)
            res.raise_for_status()
            reply = res.json().get("response", "No reply received")
        except Exception as e:
            print("❌ Error:", e)
            reply = "Sorry, I couldn't reach the server."

        print("🤖 Jarvis replied:", reply)
        chat_history.append({"role": "assistant", "content": reply})
        speak_text(reply)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_chat():
    threading.Thread(target=voice_loop, daemon=True).start()
    return jsonify({"status": "started"})


@app.route("/history")
def history():
    return jsonify(chat_history)


if __name__ == "__main__":
#    app.run(debug=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
