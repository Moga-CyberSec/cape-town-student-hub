from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERIFY_TOKEN = "studenthub123"
PHONE_NUMBER_ID = "1471409749382189"
ACCESS_TOKEN = "EAAQJYNSf5OUBS72GhLuMM4FeYJFZA8Y6HhAPh8b878X8e0wOHADGmpRRp1MXRzGoqafevjcZCpZAYeATzaxww1QSFZA3Hrg8xZApIIRywZAsp7Esn2mZBnZCp3KKk2IR1NIyOjtkZA5rApeojQL2hh5DzXelP6SZCijlNZCc4zHeAykxJ2KqaPZAWKNaQZCsPxStghL0Wf8DZA8nwCCqePmWc74j2gddG7mCmTjVTbj7oxXOY63QnglwrX6gZBCvIjndmHRRACUBrWqt0EJZASn3ySzBGY5MNvBV"

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified successfully!")
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    try:
        if data.get("entry") and data["entry"][0].get("changes") and data["entry"][0]["changes"][0]["value"].get("messages"):
            message_obj = data["entry"][0]["changes"][0]["value"]["messages"][0]
            from_number = message_obj["from"]
            user_text = message_obj.get("text", {}).get("body", "").strip()

            reply_text = f"Welcome to Cape Town Student Hub! You said: '{user_text}'"
            send_whatsapp_message(from_number, reply_text)
    except Exception as e:
        print(f"Error handling message: {e}")

    return jsonify({"status": "received"}), 200

def send_whatsapp_message(recipient, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    app.run(port=5000)