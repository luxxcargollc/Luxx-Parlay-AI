import json
import os
from datetime import datetime

from ai_engine import score_game

HISTORY_FILE = "data/picks_history.json"

TODAY_GAMES = [
    {"team": "Philadelphia Phillies", "market": "Moneyline", "odds": -120},
    {"team": "Atlanta Braves", "market": "Moneyline", "odds": -106},
    {"team": "Cleveland Guardians", "market": "Moneyline", "odds": -105},
    {"team": "Texas Rangers", "market": "Moneyline", "odds": -110},
    {"team": "Colorado Rockies", "market": "Run Line", "odds": -120},
]


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    os.makedirs("data", exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


def generate_picks():
    plays = []

    for game in TODAY_GAMES:
        score, stars = score_game(game["team"], game["odds"])

        plays.append({
            "team": game["team"],
            "market": game["market"],
            "odds": game["odds"],
            "confidence": 99,
            "edge": round(score - 50, 1),
            "ai_score": score,
            "stars": stars,
            "result": "pending"
        })

    history = load_history()

    history.append({
        "generated_at": datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
        "plays": plays
    })

    save_history(history)

    print(f"Saved {len(plays)} new picks.")


if __name__ == "__main__":
    generate_picks()