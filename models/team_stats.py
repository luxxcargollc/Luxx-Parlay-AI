import requests

TEAM_IDS = {
    "Milwaukee Brewers": 158,
    "Tampa Bay Rays": 139,
    "New York Mets": 121,
    "Pittsburgh Pirates": 134,
    "Cincinnati Reds": 113,
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
                    "last10": "Coming Soon",
                    "home_record": "Coming Soon",
                    "away_record": "Coming Soon"
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