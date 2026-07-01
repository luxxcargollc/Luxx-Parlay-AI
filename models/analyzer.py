from models.ai_engine import score_game

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

                score, stars = score_game(team, odds)

                plays.append({
                    "team": team,
                    "odds": odds,
                    "score": score,
                    "stars": stars
                })

        except:
            continue

    plays = sorted(plays, key=lambda x: x["score"], reverse=True)

    for play in plays[:5]:
        print(f'{play["stars"]} {play["team"]}')
        print(f'Odds: {play["odds"]}')
        print(f'Confidence: {play["score"]}%')
        print()