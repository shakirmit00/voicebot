from voice_recorder import record_voice
from eleven_tts import speak_text
import requests

chat_history = []
WEBHOOK_URL = "https://chlearx.app.n8n.cloud/webhook-test/voicebot2"
WAKE_WORDS = ["hi jarvis", "hey jarvis", "hello jarvis"]

print("🔴 Waiting for wake word... (say 'Hi Jarvis')")

while True:
    command = record_voice(timeout=5, phrase_time_limit=6)

    if not command:
        continue

    print(f"👂 You said: {command.lower()}")

    if any(wake_word in command.lower() for wake_word in WAKE_WORDS):
        print("🟢 Wake word detected. Assistant activated!")
        speak_text("Hi, I'm Jarvis. How can I help you?")

        while True:
            command = record_voice(timeout=5, phrase_time_limit=10)

            if not command:
                continue

            print(f"👂 You said: {command}")

            if command.lower() in ["exit", "quit", "stop", "cancel"]:
                speak_text("Goodbye!")
                break

            chat_history.append({"role": "user", "content": command})

            try:
                res = requests.post(WEBHOOK_URL, json={"history": chat_history}, timeout=12)
                res.raise_for_status()
                reply = res.json().get("response", "No response received")
            except Exception as e:
                print("❌ Error in response:", e)
                reply = "Sorry, I couldn't reach the server."

            print("🤖 Jarvis replied:", reply)
            speak_text(reply)
            chat_history.append({"role": "assistant", "content": reply})

        print("🔴 Waiting for wake word again...")
