import json
import os
from datetime import datetime


HISTORY_FILE = "data/picks_history.json"


def save_pick_history(plays, parlay):
    os.makedirs("data", exist_ok=True)

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_plays": len(plays),
        "parlay_count": len(parlay),
        "plays": plays,
        "parlay": parlay,
    }

    history = []

    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                history = json.load(file)
        except Exception:
            history = []

    history.append(entry)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

    print("\n" + "=" * 45)
    print("📁 VERSION 4.3 HISTORY SAVED")
    print("=" * 45)
    print(f"Saved {len(plays)} plays")
    print(f"Saved {len(parlay)} parlay picks")
    print(f"File: {HISTORY_FILE}")