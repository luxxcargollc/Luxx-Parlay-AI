import json
import os

HISTORY_FILE = "data/picks_history.json"


def analyze_history():
    print("\n" + "=" * 45)
    print("📊 VERSION 4.4 HISTORY ANALYTICS")
    print("=" * 45)

    if not os.path.exists(HISTORY_FILE):
        print("No history found.")
        return

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = json.load(file)

    total_runs = len(history)
    total_plays = 0
    total_parlays = 0

    for run in history:
        total_plays += run.get("total_plays", 0)
        total_parlays += run.get("parlay_count", 0)

    latest = history[-1]

    print(f"Runs Saved: {total_runs}")
    print(f"Total Plays Saved: {total_plays}")
    print(f"Total Parlays Saved: {total_parlays}")

    print("\nLatest Run")
    print("-" * 25)
    print(f"Date: {latest['date']}")
    print(f"Plays: {latest['total_plays']}")
    print(f"Parlays: {latest['parlay_count']}")

    print("=" * 45)