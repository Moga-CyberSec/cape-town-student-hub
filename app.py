from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERIFY_TOKEN = "studenthub123"
PHONE_NUMBER_ID = "1471409749382189"
ACCESS_TOKEN = "EAAQJYNSf5OUBS6vdMnt2ILaOGA6Ij43LHFuye6WgzkEIVZALHZBEZBdDdgDqoLQQ1fCmMzQopSkOqM0lUZCE27bqbzGxbV3sPxqQ5ceXBdLz8FF3z1r7Ja6N00EeZBepd2pzEWReQQ4gJhaNoJ6e4EeMJrm1qmwT24HNEHP4bxuZA7vhhzK4ud2lcaA2bZBfZANuS2igH2EwkP5GwdrEZBZC7w6ZCCld043Lv9bzFpyZCqSkNL1aQC1Gg8LwhXjAvT6K7mT2pFQvDHHQs1DJV8jCQfGTIs540gZDZD"

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
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if messages:
            msg = messages[0]
            from_number = msg.get("from")
            text = msg.get("text", {}).get("body", "")

            # Send response back to WhatsApp
            url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": from_number,
                "text": {"body": f"Welcome to Cape Town Student Hub! You said: '{text}'"}
            }
            res = requests.post(url, headers=headers, json=payload)
            print("Response status code:", res.status_code)
            print("Response body:", res.text)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("Error processing webhook:", e)
        return jsonify({"status": "error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

