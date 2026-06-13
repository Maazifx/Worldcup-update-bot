import requests
import os
import json

BOT_TOKEN = os.environ["BOT_TOKEN"]
API_KEY = os.environ["API_KEY"]

headers = {
    "x-apisports-key": API_KEY
}

response = requests.get(
    "https://v3.football.api-sports.io/fixtures?date=2026-06-13",
    headers=headers
)

data = response.json()

print("Matches found:", len(data["response"]))

for match in data["response"][:10]:
    print(
        match["league"]["name"],
        "-",
        match["teams"]["home"]["name"],
        "vs",
        match["teams"]["away"]["name"]
    )

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

    print(f"{home} vs {away}")
    print("Events:", len(events))

    for event in events[:5]:
        print(event)

    for event in events:

        if event.get("type") != "Goal":
            continue

        scorer = event.get("player", {}).get("name", "Unknown")
        minute = event.get("time", {}).get("elapsed", "?")
        detail = event.get("detail", "")

        event_id = f"{fixture_id}_{minute}_{scorer}_{detail}"

        if event_id in posted_goals:
            continue

        message = (
            f"⚽ GOAL ALERT\n\n"
            f"{home} {score_home}-{score_away} {away}\n\n"
            f"⚽ Scorer: {scorer}\n"
            f"⏱ Minute: {minute}'\n"
            f"📋 {detail}"
        )

        telegram_response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": "@wcupdates2026",
                "text": message
            }
        )

        print("Telegram:", telegram_response.status_code)

        posted_goals[event_id] = True

with open("posted_goals.json", "w") as f:
    json.dump(posted_goals, f)
