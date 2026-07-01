import requests

TEAM_IDS = {
    "Arizona Diamondbacks": 109,
    "Atlanta Braves": 144,
    "Baltimore Orioles": 110,
    "Boston Red Sox": 111,
    "Chicago Cubs": 112,
    "Chicago White Sox": 145,
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
    "New York Mets": 121,
    "New York Yankees": 147,
    "Oakland Athletics": 133,
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
        response = requests.get(url)
        data = response.json()

        for record in data["records"]:
            for t in record["teamRecords"]:
                return {
                    "team": team,
                    "wins": t["wins"],
                    "losses": t["losses"],
                    "last10": f'{t["records"]["splitRecords"][8]["wins"]}-{t["records"]["splitRecords"][8]["losses"]}',
                    "home_record": f'{t["records"]["splitRecords"][0]["wins"]}-{t["records"]["splitRecords"][0]["losses"]}',
                    "away_record": f'{t["records"]["splitRecords"][1]["wins"]}-{t["records"]["splitRecords"][1]["losses"]}',
                }

    except Exception as e:
        print(e)

    return {
        "team": team,
        "wins": "?",
        "losses": "?",
        "last10": "?",
        "home_record": "?",
        "away_record": "?"
    }