def score_game(team, odds):
    score = 50

    if odds < 0:
        score += 20
    elif odds <= 120:
        score += 10
    elif odds >= 200:
        score -= 15
    elif odds >= 150:
        score -= 10

    score = max(0, min(score, 100))

    if score >= 95:
        stars = "★★★★★"
    elif score >= 85:
        stars = "★★★★☆"
    elif score >= 75:
        stars = "★★★★"
    elif score >= 65:
        stars = "★★★"
    elif score >= 50:
        stars = "★★"
    else:
        stars = "★"

    return score, stars