import sys
import os
import time
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")


class Logger(object):

    logger = None

    def __init__(self, logger_name, log_file):
        # Log to file - Level DEBUG
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        _file = "%s/%s" % (LOG_DIR, log_file)
        rfh = logging.handlers.RotatingFileHandler(
            _file, maxBytes=10485760, backupCount=6, mode="a"
        )
        formatter = logging.Formatter(
            fmt="%(asctime)-15s: %(name)-10s - %(levelname)-16s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        rfh.setFormatter(formatter)
        self.logger.addHandler(rfh)
        # Console log - Level INFO
        self.console_logger = logging.getLogger(logger_name)
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        self.console_logger.addHandler(console)

    @staticmethod
    def timer(log, name):
        def decorator(function):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = function(*args, **kwargs)
                end_time = time.time()
                log.debug("%s - Execution time: %f" % (name, float(end_time - start_time)))
                return result
            return wrapper
        return decorator