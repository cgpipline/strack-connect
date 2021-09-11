# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import os
import logging
from logging.handlers import TimedRotatingFileHandler

LOG_FORMATTER = "[%(asctime)s][%(levelname)s][%(filename)s lineno %(lineno)d]: %(message)s"


def clear_log_handler(logger, handler_types=None):
    for handler in logger.handlers:
        if handler_types is None or isinstance(handler, handler_types):
            logger.removeHandler(handler)


def set_log_file_path(logger, path):
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    clear_log_handler(logger, logging.FileHandler)
    handler = TimedRotatingFileHandler(path, 'midnight', backupCount=10)
    handler.setFormatter(logging.Formatter(LOG_FORMATTER))
    logger.addHandler(handler)


def setup_logging(logger_name):
    # set log
    logger = logging.getLogger(logger_name)

    runtime_dir = os.getenv('RUNTIME_PATH')

    # while not root_dir.endswith("Strack_Connect"):
    #     root_dir = os.path.dirname(root_dir)
    log_dir = os.path.join(runtime_dir, "log")

    # set log config
    logger.setLevel(logging.INFO)
    output_log = "{root_dir}/{log_name}.txt".format(root_dir=log_dir, log_name=logger_name)
    set_log_file_path(logger, output_log)

    # set stdout handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMATTER))
    logger.addHandler(handler)

    return logger


for logger_name in ["teamones_desktop", "api_logger"]:
    logger = setup_logging(logger_name)
    logger.info("Starting {} logging.".format(logger_name))
    logger.setLevel(logging.DEBUG)
