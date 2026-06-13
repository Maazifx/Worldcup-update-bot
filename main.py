import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
API_KEY = os.environ["API_KEY"]

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(
    "https://v3.football.api-sports.io/fixtures?live=all",
    headers=headers
)

data = response.json()

message = "⚽ LIVE MATCHES\n\n"

if len(data["response"]) == 0:
    message += "No live matches currently."
else:
    for match in data["response"][:5]:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        home_score = match["goals"]["home"]
        away_score = match["goals"]["away"]

        minute = match["fixture"]["status"]["elapsed"]

        message += (
            f"{minute}'\n"
            f"{home} {home_score}-{away_score} {away}\n\n"
        )

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": "@wcupdates2026",
        "text": message
    }
)

print("Live scores posted")
