def calculate_confidence(stats, odds):
    confidence = 50

    # Favorite
    if odds < 0:
        confidence += 10

    wins = int(stats["wins"])
    losses = int(stats["losses"])

    if wins > losses:
        confidence += 10

    last10 = stats["last10"].split("-")
    last10_wins = int(last10[0])

    if last10_wins >= 7:
        confidence += 10
    elif last10_wins >= 5:
        confidence += 5

    home = stats["home_record"].split("-")
    home_wins = int(home[0])

    if home_wins >= 30:
        confidence += 10

    return min(confidence, 99)