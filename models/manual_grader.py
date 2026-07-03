import json
import os

HISTORY_FILE = "data/picks_history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        print("No history file found.")
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def manual_grade_latest_run():
    print("\n" + "=" * 45)
    print("📝 VERSION 4.7 MANUAL RESULT GRADER")
    print("=" * 45)

    history = load_history()

    if not history:
        return

    latest_run = history[-1]
    plays = latest_run.get("plays", [])

    if not plays:
        print("No plays found in latest run.")
        return

    print(f"Latest Run Date: {latest_run.get('date', 'Unknown')}")
    print(f"Total Plays: {len(plays)}")
    print("\nType: win, loss, push, skip, or stop\n")

    for index, play in enumerate(plays, start=1):
        current_result = play.get("result", "pending")

        if current_result != "pending":
            continue

        team = play.get("team", "Unknown")
        market = play.get("market", "Unknown")
        odds = play.get("odds", "Unknown")
        point = play.get("point", "")

        print("-" * 45)
        print(f"{index}. {team} {point}")
        print(f"Market: {market}")
        print(f"Odds: {odds}")

        result = input("Result: ").strip().lower()

        if result == "stop":
            break

        if result == "skip":
            continue

        if result not in ["win", "loss", "push"]:
            print("Invalid result. Skipped.")
            continue

        play["result"] = result
        play["graded"] = True

        if result == "win":
            play["profit_units"] = 1
        elif result == "loss":
            play["profit_units"] = -1
        else:
            play["profit_units"] = 0

        print(f"Saved result: {result}")

    save_history(history)

    print("\n" + "=" * 45)
    print("✅ MANUAL GRADING SAVED")
    print("=" * 45)