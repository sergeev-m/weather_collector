import logging
import os

from logging import Logger, handlers

from src.core.conf import LogPath, settings


def get_log() -> Logger:
    if not os.path.exists(LogPath):
        os.mkdir(LogPath)

    log_file = os.path.join(LogPath, settings.LOG_FILENAME)

    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s'
    )
    file_handler = handlers.RotatingFileHandler(
        log_file, maxBytes=50000000, backupCount=5
    )
    file_handler.setLevel(logging.WARN)
    file_handler.setFormatter(file_formatter)

    console_formatter = logging.Formatter(
        '%(levelname)s -- %(filename)s -- %(message)s'
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    return logger


log = get_log()
