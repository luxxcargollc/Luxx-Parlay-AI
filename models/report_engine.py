import json
import os

HISTORY_FILE = "data/picks_history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def get_summary():
    history = load_history()

    total_runs = len(history)
    total_picks = 0
    wins = 0
    losses = 0
    pushes = 0
    pending = 0

    for run in history:
        for play in run.get("plays", []):
            total_picks += 1
            result = str(play.get("result", "pending")).lower()

            if result == "win":
                wins += 1
            elif result == "loss":
                losses += 1
            elif result == "push":
                pushes += 1
            else:
                pending += 1

    win_rate = round((wins / (wins + losses)) * 100, 1) if wins + losses > 0 else 0

    return {
        "total_runs": total_runs,
        "total_picks": total_picks,
        "wins": wins,
        "losses": losses,
        "pushes": pushes,
        "pending": pending,
        "win_rate": win_rate,
    }