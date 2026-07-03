def form_score(wins, losses):
    games = wins + losses

    if games == 0:
        return 50

    pct = wins / games

    if pct >= 0.800:
        return 100
    elif pct >= 0.700:
        return 95
    elif pct >= 0.600:
        return 90
    elif pct >= 0.500:
        return 80
    elif pct >= 0.400:
        return 70
    else:
        return 60