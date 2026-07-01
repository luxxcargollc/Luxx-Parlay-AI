import requests

def get_games():
    print("Fetching today's games...")

    url = "https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d=2026-07-01&s=Soccer"

    response = requests.get(url)

    if response.status_code != 200:
        print("API Error")
        return

    data = response.json()

    events = data.get("events")

    if not events:
        print("No games found.")
        return

    print("\nToday's Games:\n")

    for game in events[:10]:
        home = game["strHomeTeam"]
        away = game["strAwayTeam"]

        print(f"{away} @ {home}")