def to_number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0


def adjust_confidence(confidence, stats, odds):
    confidence = to_number(confidence)
    odds = to_number(odds)

    wins = to_number(stats.get("wins", 0))
    losses = to_number(stats.get("losses", 0))

    total_games = wins + losses

    if total_games > 0:
        win_rate = wins / total_games

        if win_rate >= 0.65:
            confidence += 8
        elif win_rate >= 0.58:
            confidence += 5
        elif win_rate >= 0.52:
            confidence += 2
        elif win_rate < 0.45:
            confidence -= 5

    if odds < -200:
        confidence -= 4
    elif -160 <= odds <= 120:
        confidence += 3
    elif odds > 180:
        confidence -= 3

    return max(40, min(99, round(confidence, 1)))