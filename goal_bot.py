import requests
import os
import json

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
    with open("posted_goals.json", "r") as f:
        posted_goals = json.load(f)
except:
    posted_goals = {}

for match in data["response"]:

    fixture_id = match["fixture"]["id"]

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    score_home = match["goals"]["home"]
    score_away = match["goals"]["away"]

    events_response = requests.get(
        f"https://v3.football.api-sports.io/fixtures/events?fixture={fixture_id}",
        headers=headers
    )

    events = events_response.json()["response"]

    for event in events:

        if event.get("type") != "Goal":
            continue

        event_id = str(event.get("time", {}).get("elapsed", "")) + "_" + str(fixture_id)

        if event_id in posted_goals:
            continue

        scorer = event.get("player", {}).get("name", "Unknown")
        minute = event.get("time", {}).get("elapsed", "?")
        detail = event.get("detail", "")

        message = (
            f"⚽ GOAL\n\n"
            f"{home} {score_home}-{score_away} {away}\n\n"
            f"Scorer: {scorer}\n"
            f"Minute: {minute}'\n"
            f"{detail}"
        )

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": "@wcupdates2026",
                "text": message
            }
        )

        posted_goals[event_id] = True

with open("posted_goals.json", "w") as f:
    json.dump(posted_goals, f)
