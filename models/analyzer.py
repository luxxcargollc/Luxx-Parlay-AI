from models.team_stats import get_team_stats
from models.predictor import calculate_confidence
from models.pitchers import get_pitcher_advantage


def implied_probability(odds):
    if odds < 0:
        return round((-odds / (-odds + 100)) * 100, 1)
    return round((100 / (odds + 100)) * 100, 1)


def get_reasons(odds):
    if odds < 0:
        return ["Sportsbook has this team as the favorite"]
    if odds > 120:
        return ["Underdog value detected"]
    return ["Balanced betting line"]


def analyze_games(games):
    print("\n========================================")
    print("🔥 LUX PARLAY AI TOP 5 PLAYS")
    print("========================================\n")
    print(f"Games found: {len(games)}\n")

    plays = []

    for game in games:
        pitcher = get_pitcher_advantage(game.get("home_team"), game.get("away_team"))

        try:
            bookmaker = game.get("bookmakers", [])[0]
            market = bookmaker.get("markets", [])[0]
            outcomes = market.get("outcomes", [])
        except:
            outcomes = []

        for outcome in outcomes:
            team = outcome["name"]
            odds = outcome["price"]

            stats = get_team_stats(team)
            confidence = calculate_confidence(stats, odds)
            reasons = get_reasons(odds)

            if pitcher["advantage"] == team:
                confidence += pitcher["score"]
                reasons.append("Pitcher advantage added")

            confidence = min(confidence, 99)

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
        print(f'Implied Probability: {implied_probability(play["odds"])}%')
        print(f'Record: {stats["wins"]}-{stats["losses"]}')
        print(f'Last 10: {stats["last10"]}')
        print(f'Home: {stats["home_record"]}')
        print(f'Away: {stats["away_record"]}')
        print(f'Confidence: {play["confidence"]}%')

        if play["confidence"] >= 90:
            print("Recommendation: ⭐ STRONG BET")
        elif play["confidence"] >= 80:
            print("Recommendation: ✅ LEAN")
        else:
            print("Recommendation: ⚠️ PASS")

        print("Reasons:")
        for reason in play["reasons"]:
            print(f"- {reason}")

        print()