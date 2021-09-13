# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import os
import sys
import time
import logging.handlers
import logging
import tempfile
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


def set_loggers(logger_names=None):
    """ init strack loggers"""
    if logger_names is None:
        logger_names = ["connect_runtime", "api"]

    for logger_name in logger_names:
        logger = setup_logging(logger_name)
        logger.info("Starting {} logging.".format(logger_name))
        logger.setLevel(logging.DEBUG)


def get_logger(logger_name=None, level=logging.DEBUG,
               log_format='%(asctime)s - STRACK API - %(filename)s:%(lineno)s - %(message)s'):
    time_code = time.time()
    # LOG_FILE = os.path.join(os.environ.get("TMP"), 'STRACK_API_%s.log' % time_code)
    log_file = os.path.join(tempfile.gettempdir(), 'STRACK_API_%s.log' % time_code)

    if not logger_name:
        logger_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler

    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger


if __name__ == '__main__':
    from strack_connect.config.env import Env

    Env()
    set_loggers(["connect_runtime", "api"])
