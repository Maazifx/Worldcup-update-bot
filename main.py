import requests
import json
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

try:
    with open("last_scores.json", "r") as f:
        old_scores = json.load(f)
except:
    old_scores = {}

new_scores = {}

for match in data["response"]:

    fixture_id = str(match["fixture"]["id"])

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    home_score = match["goals"]["home"]
    away_score = match["goals"]["away"]

    score = f"{home_score}-{away_score}"

    new_scores[fixture_id] = score

    if old_scores.get(fixture_id) != score:

        message = (
            f"⚽ SCORE UPDATE\n\n"
            f"{home} {score} {away}"
        )

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": "@wcupdates2026",
                "text": message
            }
        )

with open("last_scores.json", "w") as f:
    json.dump(new_scores, f)
