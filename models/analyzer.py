from models.models.team_stats import get_team_stats
from models.predictor import calculate_confidence
from models.pitchers import get_pitcher_advantage
from models.history_analyzer import analyze_history
from models.auto_grader import auto_grade_picks
from models.performance_tracker import show_performance_tracker
from models.history_logger import save_pick_history
from models.value_engine import value_label
from models.report_engine import final_report
from models.confidence_engine import adjust_confidence
from models.ai_score import ai_score, ai_grade, ai_label
from models.ranking_engine import rank_picks
    best_unique_plays,
    best_by_market,
    best_underdogs,
    hidden_gems,
    parlay_builder,
)


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


def pick_key(play):
    return f'{play["market"]}-{play["team"]}-{play["point"]}'


def is_better_price(new_odds, old_odds):
    return new_odds > old_odds


def print_play(play, index=None):
    stats = play["stats"]

    title = f'{play["team"]} {play["point"]}'.strip()

    if index:
        print(f'\n#{index} {title}')
    else:
        print(f'\n{title}')

    print(f'Sportsbook: {play["sportsbook"]}')
    print(f'Market: {play["market"]}')
    print(f'Odds: {play["odds"]}')
    print(f'Implied Probability: {play["implied"]}%')
    print(f'Value Edge: +{play["edge"]}%')
    print(f'Confidence: {play["confidence"]}%')
    print(f'AI Score: {play["ai_score"]}')
    print(f'AI Grade: {play["ai_grade"]}')
    print(f'AI Label: {play["ai_label"]}')
    print(f'Record: {stats.get("wins", "?")}-{stats.get("losses", "?")}')

    print("Reasons:")
    for reason in play["reasons"]:
        print(f"- {reason}")


def print_section(title, plays):
    print("\n" + "=" * 45)
    print(title)
    print("=" * 45)

    if not plays:
        print("No plays found.")
        return

    for index, play in enumerate(plays, start=1):
        print_play(play, index)


def analyze_games(games):
    print("\n" + "=" * 45)
    print("🔥 LUXX PARLAY AI VERSION 4.1")
    print("=" * 45)

    print(f"\nGames found: {len(games)}")

    best_plays = {}

    for game in games:
        home_team = game.get("home_team")
        away_team = game.get("away_team")

        pitcher = get_pitcher_advantage(home_team, away_team)

        for bookmaker in game.get("bookmakers", []):
            sportsbook = bookmaker.get("title", "Unknown")

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
                    reasons = []

                    if odds < 0:
                        reasons.append("Sportsbook has this as the favorite")
                    elif odds > 120:
                        reasons.append("Underdog value detected")
                    else:
                        reasons.append("Balanced betting line")

                    if market_label == "Moneyline":
                        reasons.append("Moneyline market")
                    elif market_label == "Run Line":
                        reasons.append("Run line market")
                    elif market_label == "Over/Under":
                        reasons.append("Game total market")

                    if pitcher.get("advantage") == team:
                        confidence += pitcher.get("score", 0)
                        reasons.append("Pitcher advantage added")

                    confidence = adjust_confidence(confidence, stats, odds)
                    confidence = min(confidence, 99)

                    implied = implied_probability(odds)
                    edge = round(confidence - implied, 1)
                    label = value_label(edge)

                    if label in ["Elite Value", "Strong Value"]:
                        reasons.append(label)

                    play = {
                        "home_team": home_team,
                        "away_team": away_team,
                        "market": market_label,
                        "team": team,
                        "point": point,
                        "odds": odds,
                        "sportsbook": sportsbook,
                        "confidence": confidence,
                        "implied": implied,
                        "edge": edge,
                        "reasons": reasons,
                        "stats": stats,
                    }

                    play["ai_score"] = ai_score(play)
                    play["ai_grade"] = ai_grade(play["ai_score"])
                    play["ai_label"] = ai_label(play["ai_score"])

                    key = pick_key(play)

                    if key not in best_plays:
                        best_plays[key] = play
                    elif is_better_price(play["odds"], best_plays[key]["odds"]):
                        best_plays[key] = play

    plays = list(best_plays.values())

    print(f"Unique plays found: {len(plays)}")

    top_10 = best_unique_plays(plays, 10)
    moneyline = best_by_market(plays, "Moneyline", 5)
    run_line = best_by_market(plays, "Run Line", 5)
    totals = best_by_market(plays, "Over/Under", 5)
    underdogs = best_underdogs(plays, 5)
    gems = hidden_gems(plays, 5)
    parlay = parlay_builder(plays, 5)

    print_section("🏆 TOP 10 OVERALL PICKS", top_10)
    print_section("💰 TOP MONEYLINE PICKS", moneyline)
    print_section("📈 TOP RUN LINE PICKS", run_line)
    print_section("🔢 TOP OVER/UNDER PICKS", totals)
    print_section("🐶 BEST UNDERDOG PICKS", underdogs)
    print_section("💎 HIDDEN GEMS", gems)

    print("\n" + "=" * 45)
    print("🔥 VERSION 4.1 AI PARLAY")
    print("=" * 45)

    if not parlay:
        print("No strong parlay found.")
        return

    for index, play in enumerate(parlay, start=1):
        print(
            f'{index}. {play["team"]} {play["point"]} | '
            f'{play["market"]} | {play["odds"]} | '
            f'Grade {play["ai_grade"]} | Score {play["ai_score"]}'
        )

    avg_confidence = round(sum(p["confidence"] for p in parlay) / len(parlay), 1)
    avg_ai_score = round(sum(p["ai_score"] for p in parlay) / len(parlay), 1)

    print(f"\nAI Parlay Confidence: {avg_confidence}%")
    print(f"AI Parlay Score: {avg_ai_score}")

    save_pick_history(plays, parlay)
    analyze_history()
    auto_grade_picks()
    show_performance_tracker()