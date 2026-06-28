import json
import os

import requests

api_key = os.environ["ITCH_API_KEY"]

response = requests.get(f"https://itch.io/api/1/{api_key}/my-games")
response.raise_for_status()

game = response.json()["games"][0]

stats = {
    "views": game["views_count"],
    "downloads": game["downloads_count"]
}

path = "api/stats.json"
if os.path.exists(path):
    with open(path, "r") as f:
        old_stats = json.load(f)

    if old_stats == stats:
        print("Statistics unchanged.")
        exit(0)

with open(path, "w") as f:
    json.dump(stats, f, indent=2)

print(stats)