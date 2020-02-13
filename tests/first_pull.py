from src.data import load_data
from src.utils.logging import MyLogger

logger = MyLogger()

games = load_data.load_games(year=2019)
