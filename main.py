import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]

message = """
⚽ Football Bot Online

GitHub Actions is working.
Telegram connection successful.
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": "@wcupdates2026",
        "text": message
    }
)

print("Message sent")
