def get_best_bets(plays, limit=5):
    if not plays:
        return []

    ranked = sorted(
        plays,
        key=lambda x: (
            x.get("confidence", 0),
            x.get("edge", 0),
            x.get("ai_score", 0)
        ),
        reverse=True
    )

    return ranked[:limit]