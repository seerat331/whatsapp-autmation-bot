from flask import Flask, request
import requests

ACCESS_TOKEN = "EAAQtHJzcLnsBQKtMuub6mgZA7aFLLsckLddTZBsPHtMGC0spRCpFsJnSIFMkb0HZAESARO7ZCHGYzFrkCxXCZBmt3SThGYNUZAoqMHUWTJleFrAjgByfhxStXLh5KxTeaB7vxcI03ZAlygv4o4cZApXdI3jvU46QpdCnrSDfzCKyyB11xFZB5s5crUTgNVAS2zZAjx0Pjggf6tGUXyJL6Q7DFhT97Ei4NeAhK3v2IuGwQ4zhynbJWKZBxq50sHVSAViI9uDu4tYpWe5fPGbI8c1oXJj"
PHONE_NUMBER_ID = "878453785359822"

app = Flask(__name__)

def send_whatsapp_msg(to, message):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=body)
    print(response.status_code, response.text)


# 🔐 WEBHOOK VERIFICATION (REQUIRED)
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    VERIFY_TOKEN = "my_verify_token"
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403


# 📩 RECEIVE MESSAGES
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = msg["from"]
        text = msg["text"]["body"].lower()

        if "hi" in text:
            send_whatsapp_msg(sender, "Hello! How can I help you?")
        else:
            send_whatsapp_msg(sender, "Message received 👍")

    except Exception as e:
        print("Error:", e)

    return "ok", 200


@app.route("/")
def home():
    return "Bot is running"


if __name__ == "__main__":
    app.run(port=5000)
