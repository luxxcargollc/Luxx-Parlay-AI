import requests


TEAM_IDS = {
    "Arizona Diamondbacks": 109,
    "Atlanta Braves": 144,
    "Baltimore Orioles": 110,
    "Boston Red Sox": 111,
    "Chicago White Sox": 145,
    "Chicago Cubs": 112,
    "Cincinnati Reds": 113,
    "Cleveland Guardians": 114,
    "Colorado Rockies": 115,
    "Detroit Tigers": 116,
    "Houston Astros": 117,
    "Kansas City Royals": 118,
    "Los Angeles Angels": 108,
    "Los Angeles Dodgers": 119,
    "Miami Marlins": 146,
    "Milwaukee Brewers": 158,
    "Minnesota Twins": 142,
    "New York Yankees": 147,
    "New York Mets": 121,
    "Athletics": 133,
    "Philadelphia Phillies": 143,
    "Pittsburgh Pirates": 134,
    "San Diego Padres": 135,
    "San Francisco Giants": 137,
    "Seattle Mariners": 136,
    "St. Louis Cardinals": 138,
    "Tampa Bay Rays": 139,
    "Texas Rangers": 140,
    "Toronto Blue Jays": 141,
    "Washington Nationals": 120,
}


def find_split(split_records, split_type):
    for record in split_records:
        if record.get("type") == split_type:
            return f'{record.get("wins", "?")}-{record.get("losses", "?")}'
    return "?"


def get_team_stats(team):
    team_id = TEAM_IDS.get(team)

    if not team_id:
        return {
            "team": team,
            "wins": "?",
            "losses": "?",
            "last10": "?",
            "home_record": "?",
            "away_record": "?"
        }

    url = f"https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&teamId={team_id}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        for record in data.get("records", []):
            for t in record.get("teamRecords", []):
                splits = t.get("records", {}).get("splitRecords", [])
                print(team, [s.get("type") for s in splits])

                return {
                    "team": team,
                    "wins": t.get("wins", "?"),
                    "losses": t.get("losses", "?"),
                    "last10": find_split(splits, "lastTen"),
                    "home_record": find_split(splits, "home"),
                    "away_record": find_split(splits, "away"),
                }

    except Exception as e:
        print("Team stats error:", e)

    return {
        "team": team,
        "wins": "?",
        "losses": "?",
        "last10": "?",
        "home_record": "?",
        "away_record": "?"
    }