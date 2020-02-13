###################################################################################################
# Loading games and stats
###################################################################################################

from src.data.helpers import get_nba_fetcher
import pandas as pd
import os
import json
from pathlib import Path

data_path = Path("/Users/riccardo_pizzi/Documents/project_data/ninja")
game_ids_path = Path("/Users/riccardo_pizzi/Documents/project_data/ninja/game_stats")
game_stats_path = Path("/Users/riccardo_pizzi/Documents/project_data/ninja/game_stats")


def get_game_stats_year(year, game_ids_path, game_stats_path, data_path):
    check = (game_ids_path / f'{str(year)}.json').exists()

    if check:
        game_id_path = game_ids_path / f'{str(year)}.json'
        with open(game_id_path, encoding='utf-8') as f:
            data = json.load(f)
        games = pd.DataFrame(data)
    else:
        print(f'Pulling directly from API')
        nba_fetcher = get_nba_fetcher()
        games = nba_fetcher.get_games_by_season_year(year=year)

        if not os.path.exists(game_ids_path):
            os.mkdir(game_ids_path)

        file_name = f'{year}.json'
        games.to_json(game_ids_path/file_name)

    game_stats_list = []

    for game_id in games['gameId']:

        check = (game_stats_path/f'{str(game_id)}.json').exists()

        if check:
            game_id_path = game_stats_path/f'{str(year)}.json'
            with open(game_id_path, encoding='utf-8') as f:
                data = json.load(f)
            game_stats = pd.DataFrame(data)
        else:
            print(f'Pulling directly from API')
            nba_fetcher = get_nba_fetcher()
            game_stats = nba_fetcher.get_game_stats(game_id)
            game_stats_path = data_path / 'game_stats'

            if not os.path.exists(game_stats_path):
                    os.mkdir(game_stats_path)

            game_stats_list.append(game_stats)

        file_name = f'{game_id}.json'
        with open(file_name, "w") as fp:
            json.dump(game_stats_list, fp)

        return game_stats_list


get_game_stats_year(2018, game_ids_path, game_stats_path, data_path)