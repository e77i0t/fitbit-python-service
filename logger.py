import logging
from colorlog import ColoredFormatter

def setup_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s %(asctime)s: %(message)s (%(filename)s:%(lineno)d)"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger