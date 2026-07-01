from models.ai_engine import score_game
from models.team_stats import get_team_stats

def get_reasons(odds):
    reasons = []

    if odds < 0:
        reasons.append("Sportsbook has this team as the favorite")
    if odds <= -200:
        reasons.append("Heavy favorite, but lower value")
    if odds > 120:
        reasons.append("Underdog value detected")
    if not reasons:
        reasons.append("Balanced betting line")

    return reasons


def analyze_games(games):
    print("\nTOP 5 PLAYS OF THE DAY\n")

    if not games:
        print("No games to analyze.")
        return

    plays = []

    for game in games:
        try:
            bookmaker = game["bookmakers"][0]
            market = bookmaker["markets"][0]
            outcomes = market["outcomes"]

            for outcome in outcomes:
                team = outcome["name"]
                odds = outcome["price"]
                stats = get_team_stats(team)

                score, stars = score_game(team, odds)
                reasons = get_reasons(odds)

                plays.append({
                    "team": team,
                    "odds": odds,
                    "score": score,
                    "stars": stars,
                    "reasons": reasons,
                    "stats": stats
                })

        except:
            continue

    plays = sorted(plays, key=lambda x: x["score"], reverse=True)

    for play in plays[:5]:
        stats = play["stats"]

        print(f'{play["stars"]} {play["team"]}')
        print(f'Odds: {play["odds"]}')
        print(f"Record: {stats['wins']}-{stats['losses']}")
        print(f"Last 10: {stats['last10']}")
        print(f"Home: {stats['home_record']}")
        print(f"Away: {stats['away_record']}")
        print(f'Confidence: {play["score"]}%')
        print("Reasons:")

        for reason in play["reasons"]:
            print(f"- {reason}")

        print()