# Ninja project

## Modules
- api: code to pull data from api
- utils: utilities library
- more to come...

## Auth credentials
Save credentials for the NBA fetched as a json file under the auth directory in the root (auth/auth.json).
Note that git will ignore this (check .gitignore)

e.g. {"api_key": "..."}

## Environment variables in Visual Studio Code
To set environment variables, create a file `.env` in the root directory that contains:
```
ENV=env_name
CONFIG_DIR=path/to/auth/directory
AUTH_CONFIG_DIR=path/to/config/directory
```
Notice that there must be a file `config_$ENV.json` in `CONFIG_DIR` and a file `auth_$ENV.json` in `AUTH_CONFIG_DIR`

## Environment vaariables in a jupyter notebook
To set environment variables, run the following magic commands in in the first cell of the notebook
```
%env ENV=env_name
%env CONFIG_DIR=path/to/auth/directory
%env AUTH_CONFIG_DIR=path/to/config/directory
```
Notice that there must be a file `config_$ENV.json` in `CONFIG_DIR` and a file `auth_$ENV.json` in `AUTH_CONFIG_DIR`

## How to pull data
Data is pulled using the _api_ module. This will return raw data

Instantiate a new data fetcher object:
```python
from src.api.fetch import NBAFetcher

api_key = "MY_API_KEY"
nba_fetcher = NBAFetcher(api_key)
```

Get stats of a player
```python
player_id = 1
player_stats = nba_fetcher.get_player_stats(player_id)
```


To stats of players of a game
```python
game_id = 35
player_stats = nba_fetcher.get_player_stats_by_gane(game_id)
```