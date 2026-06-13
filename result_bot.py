import requests
import os
import json

BOT_TOKEN = os.environ["BOT_TOKEN"]
API_KEY = os.environ["API_KEY"]

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(
    "https://v3.football.api-sports.io/fixtures?status=FT",
    headers=headers
)

data = response.json()
print("Finished matches found:", len(data["response"]))

for match in data["response"][:5]:
    print(match["league"]["name"])

try:
    with open("posted_results.json", "r") as f:
        posted_results = json.load(f)
except:
        posted_results = {}

allowed_leagues = [
    "World Cup",
    "World Cup - Qualification",
    "Friendlies"
]

for match in data["response"]:

    fixture_id = str(match["fixture"]["id"])

    if fixture_id in posted_results:
        continue

    league_name = match["league"]["name"]

    if not any(x in league_name for x in allowed_leagues):
        continue

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    home_score = match["goals"]["home"]
    away_score = match["goals"]["away"]

    message = (
        f"🏁 FULL TIME\n\n"
        f"{league_name}\n\n"
        f"{home} {home_score}-{away_score} {away}"
    )

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": "@wcupdates2026",
            "text": message
        }
    )

    posted_results[fixture_id] = True

with open("posted_results.json", "w") as f:
    json.dump(posted_results, f)
