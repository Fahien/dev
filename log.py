import logging
from enum import Enum


class Color(Enum):
    WHITE = "\x1b[38;5;7m"
    GREY = "\x1b[38;5;8m"
    BLUE = "\x1b[38;5;39m"
    YELLOW = "\x1b[38;5;226m"
    RED = "\x1b[38;5;196m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    def __str__(self):
        return self.value


class CustomFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.head = "[%(levelname)s]"
        self.message = "%(message)s"
        self.FORMATS = {
            logging.DEBUG: f"{Color.GREY}{self.head}{Color.GREY} {self.message}{Color.RESET}",
            logging.INFO: f"{Color.BLUE}{self.head}{Color.GREY} {self.message}{Color.RESET}",
            logging.WARNING: f"{Color.YELLOW}{self.head}{Color.GREY} {self.message}{Color.RESET}",
            logging.ERROR: f"{Color.RED}{self.head}{Color.RESET} {Color.GREY}{self.message}{Color.RESET}",
            logging.CRITICAL: f"{Color.BOLD_RED}{self.head}{Color.GREY} {self.message}{Color.RESET}",
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def init():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(CustomFormatter())
    logger.addHandler(sh)
