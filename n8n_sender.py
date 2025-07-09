import requests

def send_to_n8n(text):
    webhook_url = "https://shaileshk.app.n8n.cloud/webhook/voicebot2"

    try:
        response = requests.post(webhook_url, json={"command": text, "mcp": True})
        response.raise_for_status()
        response_json = response.json()

        # ✅ Extract only the message
        reply = response_json.get("response", "No response received")
        #print(f"🤖 n8n replied: {reply}")
        return reply

    except Exception as e:
        print("Error sending to n8n:", e)
        return "Sorry, there was an error."
