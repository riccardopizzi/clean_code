import os
from src.utils import json_utils


class Config:
    @staticmethod
    def get_config():
        if os.environ("ENV"):
            env = os.environ("ENV")
            config_path = os.path.join(
                Config.get_config_dir(), f"config_{env}.json"
            )
        else:
            config_path = os.path.join(Config.get_config_dir(), f"config.json")
        return json_utils.read_json(config_path)

    @staticmethod
    def get_auth_config():
        config_path = os.path.join(Config.get_auth_dir(), f"auth.json")
        return json_utils.read_json(config_path)

    @staticmethod
    def get_config_dir():
        config_dir = "src/config"
        return config_dir

    @staticmethod
    def get_auth_dir():
        auth_dir = "auth"
        return auth_dir


def get_config_value(key):
    config = Config.get_config()
    return config[key]
