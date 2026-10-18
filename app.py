import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Verification token for Meta setup
VERIFY_TOKEN = "studenthub123"

# Active credentials from Meta
ACCESS_TOKEN = "EAAQJYNSf5OUBSzioIkvmPf3cZCLtDVM9Nzg9MUsMno0ZBspOSLiEkpepkF8PA8wqywFdf8e7jAsA6UTDJRPjqKgw9xCTxUWijWshSOylAnj1BZCG9oGMy4XR8bPaRe4ju8dXjVMqAUzRvbCSRE6rSThaZAy58saWcx3vBgaFAx4vq3fpwDMe3MWmwb19hQ5yoxET7c4XBBUZBPcuq4Jpsn86XJ3TwFUTl2TTNPAZDZD"
PHONE_NUMBER_ID = "1471409749382189"

@app.route("/", methods=["GET"])
def home():
    return "Cape Town Student Hub Bot is Running!", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED SUCCESSFULLY")
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("INCOMING WEBHOOK PAYLOAD:", data)

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        # Process incoming text messages
        if "messages" in value:
            message = value["messages"][0]
            from_number = message["from"]
            
            # Check if text exists
            if message.get("type") == "text":
                text_body = message["text"]["body"]
                send_whatsapp_message(from_number, f"Welcome to Cape Town Student Hub! You said: '{text_body}'")

    except Exception as e:
        print("Error parsing webhook:", e)

    return jsonify({"status": "success"}), 200

def send_whatsapp_message(to_number, text):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, json=payload, headers=headers)
    print("OUTBOUND REPLY RESPONSE:", response.status_code, response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
