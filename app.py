import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "studenthub123"
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

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "messages" in value:
            message = value["messages"][0]
            from_number = message["from"]
            
            if message.get("type") == "text":
                user_msg = message["text"]["body"].strip().lower()
                reply_text = process_user_message(user_msg)
                send_whatsapp_message(from_number, reply_text)

    except Exception as e:
        print("Error parsing webhook:", e)

    return jsonify({"status": "success"}), 200

def process_user_message(msg):
    # Main Menu
    if msg in ["hi", "hello", "menu", "hub", "0"]:
        return (
            "🇿🇦 *Welcome to Cape Town Student Hub!*\n\n"
            "Select an option by replying with the number:\n\n"
            "1️⃣ *Safe Accommodation & Scam Check*\n"
            "   └ Verify listings, safety tips, avoid deposit scams.\n\n"
            "2️⃣ *Bolt / Uber Fare Split & Ride Safety*\n"
            "   └ Find students heading your way to split rides safely.\n\n"
            "3️⃣ *Local Student Services & Merchants*\n"
            "   └ Laundromats, tech repair, and local student deals.\n\n"
            "4️⃣ *Past Papers, Study Notes & Test Prep*\n"
            "   └ Past exam papers, summarized class notes, scope sheets.\n\n"
            "Reply *1*, *2*, *3*, or *4* to choose!"
        )

    # Option 1: Accommodation
    elif msg == "1":
        return (
            "🏠 *Safe Accommodation & Scam Prevention*\n\n"
            "⚠️ *Red Flags for Deposit Scams:*\n"
            "• Landlord refuses an in-person or live video walkthrough.\n"
            "• Pressuring you to pay deposit via cash/e-wallet before viewing.\n"
            "• Listing price is way below average for Cape Town / CPT Central.\n\n"
            "Reply *VERIFY* to submit a property listing or agent contact for a quick safety check!"
        )

    # Option 2: Ride Share
    elif msg == "2":
        return (
            "🚗 *Bolt / Uber Ride Share & Safety*\n\n"
            "Split fares with fellow students and travel safer in groups.\n\n"
            "Reply with your route to match:\n"
            "Example: *RIDE Cape Station to Bellville Campus*"
        )

    # Option 3: Local Merchants
    elif msg == "3":
        return (
            "🛒 *Local Student Services & Deals*\n\n"
            "• 🧺 *PM Laundromat CPT:* Drop-off wash, dry & fold.\n"
            "• 💻 *Tech & Phone Repair:* Student rates on screen fixes.\n"
            "• 🛍️ *Local Merchants:* WhatsApp digital ledger for local shops.\n\n"
            "Reply *MENU* to return to the main hub."
        )

    # Option 4: Papers & Notes
    elif msg == "4":
        return (
            "📚 *Past Papers, Study Notes & Test Prep*\n\n"
            "Get instant access to study resources uploaded by fellow students:\n\n"
            "• Reply *JAVA* for Java Programming notes & scopes\n"
            "• Reply *PYTHON* for Python Essentials study material\n"
            "• Reply *NETWORKS* for Communications Networks past papers\n"
            "• Reply *UPLOAD* to share your own notes with the hub!\n\n"
            "Or reply *MENU* to return to the main options."
        )

    # Specific Subject Triggers
    elif msg == "java":
        return (
            "☕ *Java Programming Study Hub*\n\n"
            "• Past Test Papers & Solutions: [Drive Link]\n"
            "• Variable Scope & Methods Cheat Sheet\n"
            "• NetBeans Setup & Debugging Guide\n\n"
            "Reply *MENU* to return to main menu."
        )

    elif msg == "python":
        return (
            "🐍 *Python Essentials Hub*\n\n"
            "• Cisco Python Essentials Course Summaries\n"
            "• Practical Coding Exercise Solutions\n"
            "• Thonny IDE Quick Reference\n\n"
            "Reply *MENU* to return to main menu."
        )

    elif msg == "networks":
        return (
            "🌐 *Communications Networks Hub*\n\n"
            "• OSI & TCP/IP Model Summary Sheets\n"
            "• Subnetting & IP Addressing Practice Questions\n"
            "• Cisco Cybersecurity Intro Notes\n\n"
            "Reply *MENU* to return to main menu."
        )

    # Fallback
    else:
        return (
            f"Received: '{msg}'\n\n"
            "Reply *MENU* to view main options (1: Accommodation, 2: Ride Share, 3: Services, 4: Notes & Papers)."
        )

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
    print("OUTBOUND REPLY RESPONSE:", response.status_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
