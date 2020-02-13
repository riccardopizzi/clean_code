import os
from pathlib import Path

from src.utils.config import Config, get_config_value


def get_path(key):
    config = Config.get_config()
    data_path = Path(config["base_path"]) / config[key]

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    return data_path


def get_base_path():
    base_path = Path(get_config_value("base_path"))

    if not os.path.exists(base_path):
        os.mkdir(base_path)

    return base_path


def get_data_path():
    return get_path("data_path")


def get_game_ids_path():
    data_path = get_data_path()
    game_ids_path = data_path / "game_ids"

    if not os.path.exists(game_ids_path):
        os.mkdir(game_ids_path)

    return game_ids_path


def get_game_stats_path():
    data_path = get_data_path()
    game_stats_path = data_path / "game_stats"

    if not os.path.exists(game_stats_path):
        os.mkdir(game_stats_path)

    return game_stats_path


def get_reports_path():
    return get_path("reports_path")
