from models.team_stats import get_team_stats
from models.predictor import calculate_confidence


def get_reasons(odds):
    reasons = []

    if odds < 0:
        reasons.append("Sportsbook has this team as the favorite")
    elif odds > 120:
        reasons.append("Underdog value detected")
    else:
        reasons.append("Balanced betting line")

    return reasons


def analyze_games(games):
    print("\n========================================")
    print("🔥 LUX PARLAY AI TOP 5 PLAYS")
    print("========================================\n")

    print(f"Games found: {len(games)}\n")

    plays = []

    for game in games:
        teams = []

        try:
            bookmaker = game.get("bookmakers", [])[0]
            market = bookmaker.get("markets", [])[0]
            outcomes = market.get("outcomes", [])

            for outcome in outcomes:
                teams.append({
                    "team": outcome["name"],
                    "odds": outcome["price"]
                })

        except:
            teams.append({"team": game.get("home_team"), "odds": 0})
            teams.append({"team": game.get("away_team"), "odds": 0})

        for item in teams:
            team = item["team"]
            odds = item["odds"]

            if not team:
                continue

            stats = get_team_stats(team)
            confidence = calculate_confidence(stats, odds)
            reasons = get_reasons(odds)

            plays.append({
                "team": team,
                "odds": odds,
                "confidence": confidence,
                "reasons": reasons,
                "stats": stats,
                "stars": "★★★★★" if confidence >= 90 else "★★★★" if confidence >= 80 else "★★★"
            })

    print(f"Plays found: {len(plays)}\n")

    plays = sorted(plays, key=lambda x: x["confidence"], reverse=True)

    for index, play in enumerate(plays[:5], start=1):
        stats = play["stats"]

        print("=" * 40)
        print(f'{play["stars"]} #{index} {play["team"]}')
        print("=" * 40)
        print(f'Odds: {play["odds"]}')
        print(f'Record: {stats["wins"]}-{stats["losses"]}')
        print(f'Last 10: {stats["last10"]}')
        print(f'Home: {stats["home_record"]}')
        print(f'Away: {stats["away_record"]}')
        print(f'Confidence: {play["confidence"]}%')
        print("Reasons:")

        for reason in play["reasons"]:
            print(f"- {reason}")

        print()