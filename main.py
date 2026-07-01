from utils.helpers import banner
from models.predictor import predict
from api.sports_api import get_games
from api.odds_api import get_odds
from models.analyzer import analyze_games
banner()

print("System Status: ONLINE")
print("Welcome, Jones!")
print("Version 1.0")

predict()

get_games()

games = get_odds()

analyze_games(games)