from src.utils import paths


def check_game_ids_exist_locally(year):
    game_ids_path = paths.get_game_ids_path()
    return (game_ids_path / f"{str(year)}.json").exists()


def check_game_stats_exist_locally(game_id):
    game_stats_path = paths.get_game_stats_path()
    return (game_stats_path / f"{str(game_id)}.json").exists()
