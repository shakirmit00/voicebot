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
voice_thread_running = False


def voice_loop():
    global listening, wake_detected, chat_history, voice_thread_running
    voice_thread_running = True
    print("🔴 Waiting for wake word...")

    try:
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
                print("❌ Error contacting webhook:", e)
                reply = "Sorry, I couldn't reach the server."

            print("🤖 Jarvis replied:", reply)
            chat_history.append({"role": "assistant", "content": reply})
            speak_text(reply)

    except Exception as e:
        print("❌ Voice loop crashed:", e)

    finally:
        voice_thread_running = False
        print("🛑 Voice loop exited.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_chat():
    global voice_thread_running
    if not voice_thread_running:
        threading.Thread(target=voice_loop, daemon=True).start()
        return jsonify({"status": "started"})
    else:
        return jsonify({"status": "already running"})


@app.route("/history")
def history():
    return jsonify(chat_history)


if __name__ == "__main__":
    # Production-ready binding
    app.run(host='0.0.0.0', port=8080, debug=True)
