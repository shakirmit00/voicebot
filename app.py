from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://shaileshk.app.n8n.cloud/webhook/voicebot2"
chat_history = []
listening = False

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
    return jsonify({"reply": reply})

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
