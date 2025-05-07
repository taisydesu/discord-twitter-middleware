from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route("/")
def index():
    return "Twitter to Discord Webhook Middleware is running!"

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.json
    username = data.get("UserName", "unknown_user")
    created_at = data.get("CreatedAt", "")
    tweet_id = data.get("LinkToTweet", "")

    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        formatted_time = dt.strftime("%B %d, %Y at %I:%M%p")
    except Exception:
        formatted_time = created_at

    tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
    vx_link = f"https://vxtwitter.com/{tweet_url}"

    content = f"@{username} tweeted this at {formatted_time}: {vx_link}"

    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": content})

    return jsonify({"status": "sent to discord", "discord_response": response.text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
