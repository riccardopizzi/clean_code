import pandas as pd

from src.data.load_data import load_game_stats
from src.utils.logging import MyLogger

logger = MyLogger()


def expand_team_column(games, team_column, suffix, remove_previous=True):
    new_columns = pd.DataFrame(games[team_column].tolist())
    new_columns.columns = [column + "_" + suffix for column in new_columns.columns]
    games.reset_index(drop=True, inplace=True)
    new_columns.reset_index(drop=True, inplace=True)
    if remove_previous:
        games = games.drop(team_column, axis=1)
    return pd.concat([games, new_columns], axis=1)


def correct_dtypes_in_game_stats(team_level_stats):
    return team_level_stats[
        [col for col in team_level_stats if (col not in "teamId" or col)]
    ]


def stats_to_game_level(games: pd.DataFrame, team_level_stats: pd.DataFrame):
    game_level_stats = games.merge(
        team_level_stats,
        left_on=["gameId", "teamId_visiting"],
        right_on=["gameId", "teamId"],
    )
    game_level_stats = game_level_stats.merge(
        team_level_stats,
        left_on=["gameId", "teamId_home"],
        right_on=["gameId", "teamId"],
        suffixes=("_visiting", "_home"),
    )
    return game_level_stats


def aggregate_team_level_stats(games: pd.DataFrame):
    all_game_stats_list = []
    for game_id in games["gameId"]:
        logger.info(f"Pulling game statistics for game with id {game_id}")
        game_stats = load_game_stats(game_id=game_id)
        all_game_stats_list = all_game_stats_list + game_stats["api"]["statistics"]

    team_level_stats = pd.DataFrame.from_dict(all_game_stats_list)

    return team_level_stats


def build_game_level_table(games):
    games = expand_team_column(games, "vTeam", "visiting")
    games = expand_team_column(games, "hTeam", "home")
    team_level_stats = aggregate_team_level_stats(games)

    for col in team_level_stats.columns:
        if col != "min":
            try:
                team_level_stats[col] = team_level_stats[col].astype(float)
            except ValueError:
                logger.info(
                    f"Column {col} could not be converted to float. Try different type"
                )
        else:
            team_level_stats[col] = [
                float(i) + float(j) / 60
                for i, j in team_level_stats[col].str.split(":")
            ]

    games["gameId"] = games["gameId"].astype(float)
    games["teamId_visiting"] = games["teamId_visiting"].astype(float)
    games["teamId_home"] = games["teamId_home"].astype(float)

    game_level_stats = stats_to_game_level(games, team_level_stats)

    return game_level_stats
