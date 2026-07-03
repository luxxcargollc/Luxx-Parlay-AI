import json
import os

HISTORY_FILE = "data/picks_history.json"


def show_performance_tracker():
    print("\n" + "=" * 45)
    print("📈 VERSION 4.5 PERFORMANCE TRACKER")
    print("=" * 45)

    if not os.path.exists(HISTORY_FILE):
        print("No pick history found yet.")
        return

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = json.load(file)

    total_picks = 0
    graded_picks = 0
    wins = 0
    losses = 0
    pushes = 0

    market_stats = {}

    for run in history:
        for play in run.get("plays", []):
            total_picks += 1

            result = play.get("result", "pending")
            market = play.get("market", "Unknown")

            if market not in market_stats:
                market_stats[market] = {
                    "wins": 0,
                    "losses": 0,
                    "pushes": 0,
                    "pending": 0,
                    "total": 0,
                }

            market_stats[market]["total"] += 1

            if result == "win":
                wins += 1
                graded_picks += 1
                market_stats[market]["wins"] += 1
            elif result == "loss":
                losses += 1
                graded_picks += 1
                market_stats[market]["losses"] += 1
            elif result == "push":
                pushes += 1
                graded_picks += 1
                market_stats[market]["pushes"] += 1
            else:
                market_stats[market]["pending"] += 1

    win_rate = round((wins / graded_picks) * 100, 1) if graded_picks else 0

    print(f"Total Picks: {total_picks}")
    print(f"Graded Picks: {graded_picks}")
    print(f"Pending Picks: {total_picks - graded_picks}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Pushes: {pushes}")
    print(f"Win Rate: {win_rate}%")

    print("\nMarket Breakdown")
    print("-" * 25)

    for market, stats in market_stats.items():
        graded = stats["wins"] + stats["losses"] + stats["pushes"]
        market_win_rate = round((stats["wins"] / graded) * 100, 1) if graded else 0

        print(f"\n{market}")
        print(f"Total: {stats['total']}")
        print(f"W-L-P: {stats['wins']}-{stats['losses']}-{stats['pushes']}")
        print(f"Pending: {stats['pending']}")
        print(f"Win Rate: {market_win_rate}%")

    print("=" * 45)