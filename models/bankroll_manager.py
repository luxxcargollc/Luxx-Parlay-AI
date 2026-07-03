def recommend_units(play):
    confidence = float(play.get("confidence", 0))
    edge = float(play.get("edge", 0))
    ai_score = float(play.get("ai_score", 0))

    score = (confidence * 0.5) + (ai_score * 0.3) + (edge * 0.2)

    if score >= 90:
        return 5, "Aggressive"
    elif score >= 80:
        return 4, "Strong"
    elif score >= 70:
        return 3, "Standard"
    elif score >= 60:
        return 2, "Small"
    else:
        return 1, "Watch Only"