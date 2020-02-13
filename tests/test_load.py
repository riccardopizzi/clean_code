import unittest
import pandas as pd
from src.data.load_data import load_games
from src.data.processing import (
    expand_team_column,
    stats_to_game_level,
    aggregate_team_level_stats,
)


class TestLoad(unittest.TestCase):
    def test_load_games(self):
        games = load_games(year=2019 )
        self.assertIsInstance(games, pd.DataFrame)

    def test_expand(self):
        games = load_games(year=2019)
        games = expand_team_column(games, "vTeam", "visiting")
        games = expand_team_column(games, "hTeam", "home")
        self.assertIsInstance(games, pd.DataFrame)

    def test_aggregate_team(self):
        games = load_games(year=2019)
        team_level_stats = aggregate_team_level_stats(games.iloc[0:10])
        self.assertIsInstance(team_level_stats, pd.DataFrame)

    def test_stats_team_level(self):
        games = load_games(year=2019)
        team_level_stats = aggregate_team_level_stats(games.iloc[0:10])
        game_level_stats = stats_to_game_level(games, team_level_stats)
        self.assertIsInstance(game_level_stats, pd.DataFrame)
