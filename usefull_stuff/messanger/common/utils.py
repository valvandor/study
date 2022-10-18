"""
Helpfully utils
"""
import logging
import sys


def get_common_logger() -> logging.Logger:
    """
    Resolves which logger should be for common logic of sockets

    Returns:
        logger that should be used
    """
    logger_name = 'server' if 'server.py' in sys.argv[0] else 'client'
    return logging.getLogger(logger_name)
