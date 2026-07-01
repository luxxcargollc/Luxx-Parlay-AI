from models.team_stats import get_team_stats
from models.predictor import calculate_confidence
from models.pitchers import get_pitcher_advantage


def implied_probability(odds):
    if odds < 0:
        return round((-odds / (-odds + 100)) * 100, 1)
    return round((100 / (odds + 100)) * 100, 1)


def market_name(key):
    if key == "h2h":
        return "Moneyline"
    if key == "spreads":
        return "Run Line"
    if key == "totals":
        return "Over/Under"
    return key


def get_reasons(market, odds):
    reasons = []

    if odds < 0:
        reasons.append("Sportsbook has this as the favorite")
    elif odds > 120:
        reasons.append("Underdog value detected")
    else:
        reasons.append("Balanced betting line")

    if market == "Run Line":
        reasons.append("Run line market")
    if market == "Over/Under":
        reasons.append("Game total market")

    return reasons


def pick_key(play):
    return f'{play["market"]}-{play["team"]}-{play["point"]}'


def is_better_price(new_odds, old_odds):
    return new_odds > old_odds


def analyze_games(games):
    print("\n========================================")
    print("🔥 LUXX PARLAY AI VERSION 2")
    print("========================================\n")
    print(f"Games found: {len(games)}\n")

    best_plays = {}

    for game in games:
        pitcher = get_pitcher_advantage(game.get("home_team"), game.get("away_team"))

        for bookmaker in game.get("bookmakers", []):
            sportsbook = bookmaker.get("title", "Unknown Sportsbook")

            for market in bookmaker.get("markets", []):
                market_key = market.get("key")
                market_label = market_name(market_key)

                for outcome in market.get("outcomes", []):
                    team = outcome.get("name")
                    odds = outcome.get("price")
                    point = outcome.get("point", "")

                    if not team or odds is None:
                        continue

                    stats = get_team_stats(team)
                    confidence = calculate_confidence(stats, odds)
                    reasons = get_reasons(market_label, odds)

                    if pitcher["advantage"] == team:
                        confidence += pitcher["score"]
                        reasons.append("Pitcher advantage added")

                    confidence = min(confidence, 99)
                    implied = implied_probability(odds)
                    edge = round(confidence - implied, 1)

                    play = {
                        "market": market_label,
                        "team": team,
                        "point": point,
                        "odds": odds,
                        "sportsbook": sportsbook,
                        "confidence": confidence,
                        "edge": edge,
                        "implied": implied,
                        "reasons": reasons,
                        "stats": stats,
                        "stars": "★★★★★" if confidence >= 90 else "★★★★" if confidence >= 80 else "★★★"
                    }

                    key = pick_key(play)

                    if key not in best_plays:
                        best_plays[key] = play
                    elif is_better_price(play["odds"], best_plays[key]["odds"]):
                        best_plays[key] = play

    plays = list(best_plays.values())

    print(f"Unique plays found: {len(plays)}\n")

    for market in ["Moneyline", "Run Line", "Over/Under"]:
        market_plays = [p for p in plays if p["market"] == market]
        market_plays = sorted(market_plays, key=lambda x: x["confidence"], reverse=True)

        print("\n" + "=" * 40)
        print(f"🔥 TOP {market.upper()} PICKS")
        print("=" * 40)

        for index, play in enumerate(market_plays[:3], start=1):
            stats = play["stats"]

            print(f'\n{play["stars"]} #{index} {play["team"]} {play["point"]}')
            print(f'Sportsbook: {play["sportsbook"]}')
            print(f'Odds: {play["odds"]}')
            print(f'Implied Probability: {play["implied"]}%')
            print(f'Value Edge: +{play["edge"]}%')
            print(f'Record: {stats["wins"]}-{stats["losses"]}')
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

    print("\n" + "=" * 40)
    print("💰 VERSION 2 AI PARLAY")
    print("=" * 40)

    parlay = sorted(plays, key=lambda x: x["confidence"], reverse=True)[:5]

    for index, play in enumerate(parlay, start=1):
        print(f'{index}. {play["team"]} {play["point"]} | {play["market"]} | {play["odds"]}')

    avg_confidence = round(sum(p["confidence"] for p in parlay) / len(parlay), 1)
    print(f"\nAI Parlay Confidence: {avg_confidence}%")