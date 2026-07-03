def rate_pick(play):
    confidence = play.get("confidence", 0)
    ai_score = play.get("ai_score", 0)
    edge = play.get("edge", 0)

    total_score = (confidence * 0.5) + (ai_score * 0.3) + (edge * 0.2)

    if total_score >= 90:
        return "★★★★★ Elite", "LOW"
    elif total_score >= 80:
        return "★★★★ Strong", "MEDIUM"
    elif total_score >= 70:
        return "★★★ Solid", "MEDIUM"
    elif total_score >= 60:
        return "★★ Risky", "HIGH"
    else:
        return "★ Avoid", "HIGH"