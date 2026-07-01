import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_odds():
    print("\nFetching real MLB odds...")

    api_key = os.getenv("ODDS_API_KEY")

    if not api_key:
        print("Missing API key. Check your .env file.")
        return

    url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"

    params = {
        "apiKey": api_key,
        "regions": "us",
        "markets": "h2h,totals",
        "oddsFormat": "american"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Odds API Error")
        print(response.text)
        return

    games = response.json()

    print("\nToday's MLB Odds:\n")

    for game in games[:5]:
        print(game["away_team"], "@", game["home_team"])