import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "studenthub123"
ACCESS_TOKEN = "EAAQJYNSf5OUBS4MTZBE5yFgP3jAfLWiJwuzhOZCahkipIc4lkFv20pP1nZAZBnaOWiQ6OZCpn51FshEX4pMUZAQBx05NgvlolMZCRZCHddKVAIBbiZBPTOg1iIXgiWg4j3C3sQYvpeafQsPHUgqKZAxYXSRNYYPGDNpGa70cs0paU4lZAlLPQACqqpQWfkabfLUlL2UrA5sFsS1YBHuBxkgPNwZCKQpdiusRrH7KWf88QuSJ88O0kT69BveBiVi0wHGjt4oEPhMIwFVpyZBepxQ70vBXqlaQ1"
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
    elif msg.startswith("ride"):
        route = msg.replace("ride", "").strip()
        if not route:
            return (
                "🚗 *Bolt / Uber Ride Share & Safety*\n\n"
                "Split fares with fellow students and travel safer in groups.\n\n"
                "Reply with your pickup & destination to match:\n"
                "Example: *RIDE Cape Station to Bellville*\n"
                "Example: *RIDE D6 to V&A Waterfront*"
            )
        return (
            f"🚗 *Ride Request Logged!*\n\n"
            f"📍 *Route:* {route.title()}\n"
            "🔍 Searching for students traveling this route...\n\n"
            "We will notify you on WhatsApp as soon as a match is found to split the fare!"
        )

    # Option 3: Local Merchants
    elif msg == "3":
        return (
            "🛒 *Local Student Services & Deals*\n\n"
            "• 🧺 *PM Laundromat CPT:* Drop-off wash, dry & fold.\n"
            "• 💻 *Tech & Phone Repair:* Student rates on screen fixes.\n"
            "• 🛍️ *Local
