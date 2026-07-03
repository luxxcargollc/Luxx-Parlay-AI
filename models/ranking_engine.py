def play_id(play):
    return f'{play.get("market")}-{play.get("team")}-{play.get("point")}'


def game_id(play):
    return f'{play.get("home_team")}-{play.get("away_team")}'


def clean_score(play):
    return play.get("ai_score", play.get("confidence", 0))


def rank_plays(plays):
    return sorted(
        plays,
        key=lambda x: (
            clean_score(x),
            x.get("confidence", 0),
            x.get("edge", 0)
        ),
        reverse=True
    )


def best_unique_plays(plays, limit=10):
    ranked = rank_plays(plays)
    seen = set()
    final = []

    for play in ranked:
        pid = play_id(play)

        if pid in seen:
            continue

        seen.add(pid)
        final.append(play)

        if len(final) == limit:
            break

    return final


def best_one_per_game(plays, limit=10):
    ranked = rank_plays(plays)
    used_games = set()
    final = []

    for play in ranked:
        gid = game_id(play)

        if gid in used_games:
            continue

        used_games.add(gid)
        final.append(play)

        if len(final) == limit:
            break

    return final


def best_by_market(plays, market, limit=5):
    market_plays = [p for p in plays if p.get("market") == market]
    return best_unique_plays(market_plays, limit)


def best_underdogs(plays, limit=5):
    dogs = [p for p in plays if p.get("odds", 0) > 100]
    return best_unique_plays(dogs, limit)


def hidden_gems(plays, limit=5):
    gems = [
        p for p in plays
        if p.get("odds", 0) > 100
        and p.get("edge", 0) >= 8
        and clean_score(p) >= 75
    ]

    return best_unique_plays(gems, limit)


def parlay_builder(plays, legs=5):
    ranked = rank_plays(plays)
    used_games = set()
    parlay = []

    for play in ranked:
        gid = game_id(play)

        if gid in used_games:
            continue

        if clean_score(play) < 70:
            continue

        if play.get("edge", 0) < 0:
            continue

        used_games.add(gid)
        parlay.append(play)

        if len(parlay) == legs:
            break

    return parlay