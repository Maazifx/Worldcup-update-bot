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

if len(data["response"]) == 0:
    print("No live matches.")
    exit()

allowed_leagues = [
    "World Cup",
    "World Cup - Qualification",
    "Friendlies"
]

for match in data["response"]:

    league_name = match["league"]["name"]

    if not any(x in league_name for x in allowed_leagues):
        continue

    fixture_id = str(match["fixture"]["id"])

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    home_score = match["goals"]["home"]
    away_score = match["goals"]["away"]

    score = f"{home_score}-{away_score}"

    new_scores[fixture_id] = score

    if old_scores.get(fixture_id) != score:

        minute = match["fixture"]["status"]["elapsed"]

        message = (
            f"⚽ LIVE UPDATE\n\n"
            f"🏆 {league_name}\n"
            f"⏱ {minute}'\n\n"
            f"{home} {home_score}-{away_score} {away}"
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
