import pandas as pd

from src.utils.io import JSONHandler
from src.api.connect import RapidApiConnector


class NBAFetcher:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._rapid_api_connector = RapidApiConnector(self._api_key)
        self._json_handler = JSONHandler(self._rapid_api_connector)

    def get_seasons(self) -> dict:
        return self._json_handler.get_json("seasons/")

    def get_leagues(self) -> dict:
        return self._json_handler.get_json("leagues/")

    def get_games_by_season_year(self, year: int) -> pd.DataFrame:
        return self._json_handler.get_table(
            f"games/seasonYear/{year}/", subset=["api", "games"]
        )

    def get_games_by_date(self, date: pd.Timestamp) -> pd.DataFrame:
        if not isinstance(date, str):
            date = date.strftime("%Y-%m-%d")
        return self._json_handler.get_table(
            f"games/date/{date}/", subset=["api", "games"]
        )

    def get_games_live(self) -> pd.DataFrame:
        return self._json_handler.get_table("games/live/", subset=["api", "games"])

    def get_game_details(self, game_id) -> dict:
        return self._json_handler.get_json(f"gameDetails/{game_id}/")

    def get_team_by_id(self, team_id) -> dict:
        return self._json_handler.get_json(f"teams/teamId/{team_id}/")

    def get_player_by_id(self, player_id) -> dict:
        return self._json_handler.get_json(f"players/playerId/{player_id}/")

    def get_game_stats(self, game_id) -> dict:
        return self._json_handler.get_json(f"statistics/games/gameId/{game_id}/")

    def get_player_stats_by_game(self, game_id) -> dict:
        return self._json_handler.get_json(f"/statistics/players/gameId/{game_id}")

    def get_player_stats(self, player_id) -> dict:
        return self._json_handler.get_json(f"/statistics/players/playerId/{player_id}")
