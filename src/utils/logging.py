import inspect
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from src.utils.config import Config


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingleLevelFilter(logging.Filter):
    def __init__(self, passlevel, reject):
        self.passlevel = passlevel
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return record.levelno != self.passlevel
        else:
            return record.levelno == self.passlevel


class MyLogger(metaclass=Singleton):
    logger = None

    def __init__(self, env=None):
        if env is None:
            config_dict = {
                "base_path": "",
                "logging_path": "../..",
                "log_name": "tests",
            }
        else:
            config_dict = Config.get_config(env)
        today = datetime.today().strftime("%Y%m%d")
        now = datetime.today().strftime("%Y%m%d_%H%M%S")
        logger_path = "{}/{}".format(
            Path(config_dict["base_path"]) / Path(config_dict["logging_path"]), today
        )
        # TODO: change below to filesystem connector
        if not Path(logger_path).exists():
            os.makedirs(Path(logger_path), exist_ok=True)
        name = config_dict["log_name"].replace(" ", "_")
        if os.getenv("LOG_NAME"):
            name = os.getenv("LOG_NAME").replace(" ", "_")
        log_filename = "{}/{}_{}.log".format(logger_path, now, name)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_filter = SingleLevelFilter(logging.INFO, False)
        stdout_handler.addFilter(stdout_filter)

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_filter = SingleLevelFilter(logging.INFO, True)
        stderr_handler.addFilter(stderr_filter)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(threadName)s - [%(levelname)s] - %(message)s",
            handlers=[
                stdout_handler,
                stderr_handler,
                logging.FileHandler(log_filename),
            ],
        )

        self.logger_path = log_filename
        self.logger = logging.getLogger(__name__ + ".logger")

    @staticmethod
    def __get_call_info():
        try:
            stack = inspect.stack()
            # stack[1] gives previous function ('info' in our case)
            # stack[2] gives before previous function and so on

            fn = MyLogger.__prettify_name(stack[3][1])
            ln = stack[3][2]
            func = stack[3][3]
        except IndexError:
            fn = "unknown fn"
            ln = "unknown ln"
            func = "unknown func"

        return fn, func, ln

    @staticmethod
    def __prettify_name(file_name):
        return (
            os.path.splitext(os.path.basename(file_name))[0].upper().replace("_", " ")
        )

    def info(self, message, *args):
        self.logger.info(self.format_message(message), *args)

    def warning(self, message, *args):
        self.logger.warning(self.format_message(message), *args)

    def exception(self, message, *args):
        self.logger.exception(self.format_message(message), *args)

    def error(self, message, *args):
        self.logger.error(self.format_message(message), *args)

    def debug(self, message, *args):
        self.logger.debug(self.format_message(message), *args)

    def format_message(self, message):
        return "[{}] - {} at line {}: {}".format(
            *self.__get_call_info(), message
        ).encode("utf-8")
