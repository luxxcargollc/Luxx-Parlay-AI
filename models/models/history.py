import csv
from datetime import datetime
from pathlib import Path

def save_picks(parlay):
    Path("data").mkdir(exist_ok=True)
    file_path = "data/picks_history.csv"

    file_exists = Path(file_path).exists()

    with open(file_path, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["date", "team", "market", "point", "odds", "confidence"])

        for pick in parlay:
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d"),
                pick["team"],
                pick["market"],
                pick["point"],
                pick["odds"],
                pick["confidence"]
            ])