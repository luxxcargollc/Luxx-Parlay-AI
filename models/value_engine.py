def expected_value(play):
    confidence = float(play.get("confidence", 0))
    odds = int(play.get("odds", -110))

    if odds < 0:
        payout = 100 / abs(odds)
    else:
        payout = odds / 100

    probability = confidence / 100
    ev = (probability * payout) - (1 - probability)

    return round(ev * 100, 2)


def value_label(play):
    ev = expected_value(play)

    if ev >= 20:
        return "🔥 Elite Value"
    elif ev >= 10:
        return "✅ Strong Value"
    elif ev >= 0:
        return "➕ Positive Value"
    else:
        return "⚠️ Negative Value"