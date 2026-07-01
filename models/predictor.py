def calculate_confidence(stats, odds):
    confidence = 50

    if odds < 0:
        confidence += 10

    try:
        wins = int(stats["wins"])
        losses = int(stats["losses"])

        if wins > losses:
            confidence += 10

        last10 = stats["last10"].split("-")
        if int(last10[0]) >= 7:
            confidence += 10

        home = stats["home_record"].split("-")
        if int(home[0]) >= 30:
            confidence += 10

    except:
        pass

    return min(confidence, 99)