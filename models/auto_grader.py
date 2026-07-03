import json
import os

HISTORY_FILE = "data/picks_history.json"


def auto_grade_picks():
    print("\n" + "=" * 45)
    print("🧠 VERSION 4.6 AUTO GRADER")
    print("=" * 45)

    if not os.path.exists(HISTORY_FILE):
        print("No history file found.")
        return

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = json.load(file)

    updated = 0
    pending = 0

    for run in history:
        for play in run.get("plays", []):
            if "result" not in play:
                play["result"] = "pending"
                pending += 1
                updated += 1

            if "graded" not in play:
                play["graded"] = False
                updated += 1

            if "profit_units" not in play:
                play["profit_units"] = 0
                updated += 1

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

    print(f"Updated Picks: {updated}")
    print(f"Pending Picks: {pending}")
    print("Status: Ready for real win/loss grading")
    print("=" * 45)