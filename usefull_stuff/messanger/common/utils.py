"""
Helpfully utils
"""
import logging
import sys
from datetime import datetime
from functools import wraps


def get_common_logger() -> logging.Logger:
    """
    Resolves which logger should be for common logic of sockets

    Returns:
        logger that should be used
    """
    logger_name = 'server' if 'server.py' in sys.argv[0] else 'client'
    return logging.getLogger(logger_name)


def logged(logger):
    """
    Decorator for wrapping methods with logging

    Args:
        logger: logger to use

    Returns:
        decorated function
    """
    def wrap_method(func_to_log):

        @wraps(func_to_log)
        def wrapped(*args, **kwargs):
            start_time = datetime.now()
            func_name = func_to_log.__name__
            logger.debug(f'Enter {func_name} method (args={args}, kwargs={kwargs})')

            result = func_to_log(*args, **kwargs)

            spent_time = round((datetime.now() - start_time).total_seconds() * 1000)
            logger.debug(f'Result {func_name} return: {result}, {spent_time} ms')
            return result
        return wrapped
    return wrap_method
