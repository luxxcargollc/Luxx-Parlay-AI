def analyze_pick(play):
    confidence = play.get("confidence", 0)
    ai_score = play.get("ai_score", 0)
    edge = play.get("edge", 0)

    reasons = []

    if confidence >= 90:
        reasons.append("🔥 Very High AI Confidence")

    if ai_score >= 70:
        reasons.append("🧠 AI Model Strongly Agrees")

    if edge >= 5:
        reasons.append("📈 Positive Betting Edge")

    if not reasons:
        reasons.append("⚠️ Limited Supporting Data")

    return reasons