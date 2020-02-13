from src.api.fetch import NBAFetcher
from src.utils.config import Config

def get_nba_fetcher():
    auth_config = Config.get_auth_config()
    api_key = auth_config["api_key"]

    return NBAFetcher(api_key)
