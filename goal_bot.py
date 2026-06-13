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

print("Live matches:", len(data["response"]))

try:
    with open("posted_goals.json", "r") as f:
        posted_goals = json.load(f)
except:
    posted_goals = {}
  
  for match in data["response"]:

    fixture_id = match["fixture"]["id"]

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    events_response = requests.get(
        f"https://v3.football.api-sports.io/fixtures/events?fixture={fixture_id}",
        headers=headers
    )

    events = events_response.json()["response"]

    print(f"{home} vs {away}")
    print("Events:", len(events))
  
