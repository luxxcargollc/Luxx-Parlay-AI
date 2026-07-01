from utils.helpers import banner
from api.odds_api import get_odds
from models.analyzer import analyze_games

banner()

print("System Status: ONLINE")
print("Welcome, Jones!")
print("Version 1.0")

games = get_odds()

analyze_games(games)