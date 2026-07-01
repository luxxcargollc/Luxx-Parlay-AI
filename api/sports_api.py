import requests

def get_games():
    print("Fetching MLB games...")

    url = "https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d=2026-07-01&s=Baseball"

    response = requests.get(url)

    if response.status_code != 200:
        print("API Error")
        return

    data = response.json()
    events = data.get("events")

    if not events:
        print("No MLB games found.")
        return

    print("\nToday's MLB Games:\n")

    for game in events[:10]:
        home = game.get("strHomeTeam")
        away = game.get("strAwayTeam")
        print(f"{away} @ {home}")