def safe_int(value):
    try:
        return int(value)
    except:
        return 0


def parse_record(record):
    try:
        wins, losses = record.split("-")
        return int(wins), int(losses)
    except:
        return 0, 0


def win_pct_score(wins, losses):
    games = wins + losses

    if games == 0:
        return 50

    pct = wins / games

    if pct >= 0.700:
        return 95
    if pct >= 0.620:
        return 88
    if pct >= 0.550:
        return 80
    if pct >= 0.500:
        return 72
    if pct >= 0.450:
        return 64
    if pct >= 0.400:
        return 55
    return 45


def record_score(stats):
    wins = safe_int(stats.get("wins", 0))
    losses = safe_int(stats.get("losses", 0))
    return win_pct_score(wins, losses)


def last10_score(stats):
    wins, losses = parse_record(stats.get("last10", "?"))
    return win_pct_score(wins, losses)


def home_away_score(stats, is_home):
    if is_home:
        wins, losses = parse_record(stats.get("home_record", "?"))
    else:
        wins, losses = parse_record(stats.get("away_record", "?"))

    return win_pct_score(wins, losses)


def team_power_rating(stats, is_home=False):
    overall = record_score(stats)
    recent = last10_score(stats)
    location = home_away_score(stats, is_home)

    power = round(
        (overall * 0.45) +
        (recent * 0.35) +
        (location * 0.20),
        1
    )

    return {
        "overall": overall,
        "recent": recent,
        "location": location,
        "power": power
    }


def power_boost(power_rating, reasons):
    power = power_rating.get("power", 50)

    if power >= 88:
        reasons.append("Elite team power rating")
        return 6

    if power >= 80:
        reasons.append("Strong team power rating")
        return 4

    if power >= 72:
        reasons.append("Solid team power rating")
        return 2

    if power <= 55:
        reasons.append("Weak team power rating")
        return -4

    return 0