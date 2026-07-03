def clamp(value, low=40, high=99):
    return max(low, min(high, round(value, 1)))


def ai_score(play):
    confidence = play.get("confidence", 60)
    edge = play.get("edge", 0)
    odds = play.get("odds", 0)
    market = play.get("market", "")
    power = play.get("power") or {}

    power_score = power.get("power", 60)

    score = 0

    score += confidence * 0.30
    score += power_score * 0.25

    if edge >= 30:
        score += 22
    elif edge >= 20:
        score += 18
    elif edge >= 12:
        score += 14
    elif edge >= 6:
        score += 9
    elif edge >= 0:
        score += 4
    else:
        score -= 8

    if market == "Moneyline":
        score += 6
    elif market == "Run Line":
        score += 3
    elif market == "Over/Under":
        score -= 2

    if -160 <= odds <= 140:
        score += 5
    elif odds < -220:
        score -= 5
    elif odds > 200:
        score -= 6

    return clamp(score)


def ai_grade(score):
    if score >= 94:
        return "A+"
    if score >= 88:
        return "A"
    if score >= 82:
        return "B+"
    if score >= 75:
        return "B"
    if score >= 68:
        return "C"
    return "D"


def ai_label(score):
    if score >= 94:
        return "ELITE PLAY"
    if score >= 88:
        return "STRONG PLAY"
    if score >= 82:
        return "GOOD LEAN"
    if score >= 75:
        return "WATCH LIST"
    return "PASS"