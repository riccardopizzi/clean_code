import pandas as pd

from src.data import checks
from src.data.helpers import get_nba_fetcher
from src.utils.logging import MyLogger
from src.utils import paths, json_utils

logger = MyLogger()


def load_all_game_stats_in_year(year):
    games = load_games(year)
    game_stats_list = []
    for game_id in games["gameId"]:
        game_stats_list.append(load_game_stats(game_id))
    return game_stats_list


def load_games(year: int):
    if checks.check_game_ids_exist_locally(year):
        return load_games_from_local(year)
    else:
        logger.info(
            f"Game IDs for year {str(year)} are not saved locally. Pulling directly from API"
        )
        return load_games_from_api(year)


def load_game_stats(game_id: int):
    if checks.check_game_stats_exist_locally(game_id):
        return load_game_stats_from_local(game_id)
    else:
        logger.info(
            f"Game stats for game_id {str(game_id)} are not saved locally. Pulling directly from "
            f"API"
        )
        return load_game_stats_from_api(game_id)


def load_games_from_local(year: int):
    game_ids_path = paths.get_game_ids_path()
    games = pd.DataFrame(json_utils.read_json(game_ids_path / f"{str(year)}.json"))
    return games


def load_games_from_api(year: int):
    nba_fetcher = get_nba_fetcher()
    games = nba_fetcher.get_games_by_season_year(year=year)
    game_ids_path = paths.get_game_ids_path()
    file_name = f"{year}.json"
    games.to_json(game_ids_path / file_name)
    return games


def load_game_stats_from_local(game_id):
    game_stats_path = paths.get_game_stats_path()
    return json_utils.read_json(game_stats_path / f"{str(game_id)}.json")


def load_game_stats_from_api(game_id: int):
    nba_fetcher = get_nba_fetcher()
    game_stats = nba_fetcher.get_game_stats(game_id)
    game_stats_path = paths.get_game_stats_path()
    file_name = f"{game_id}.json"
    json_utils.save_json(game_stats, game_stats_path / file_name)
    return game_stats
