"""
logger.py — one shared logger configuration for the whole pipeline.
Every module imports get_logger() instead of setting up its own
handlers, so all log lines land in the same file with the same format.
"""

import logging
from logging.handlers import RotatingFileHandler
from data_pipeline.config import LOG_FILE_PATH

# Make sure the logs/ directory exists even on a fresh clone.
LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger scoped to the calling module (pass __name__).
    Rotating file handler caps pipeline.log at 5MB x 3 backups so it
    doesn't grow forever on a machine running 24/7 every 5 minutes.
    """
    logger = logging.getLogger(name)

    # Guard against duplicate handlers if get_logger() is called
    # more than once for the same module (e.g. during a scheduler reload).
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(
        LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setFormatter(logging.Formatter(_LOG_FORMAT))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(_LOG_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger