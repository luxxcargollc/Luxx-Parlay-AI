def score_game(team, odds):
    score = 50

    if odds < 0:
        score += 20

    if odds > 150:
        score -= 10

    if score >= 90:
        stars = "★★★★★"
    elif score >= 80:
        stars = "★★★★"
    elif score >= 70:
        stars = "★★★"
    else:
        stars = "★★"

    return score, stars