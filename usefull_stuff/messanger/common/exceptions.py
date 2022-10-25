"""
Module with custom exceptions
"""


class IncompleteConfig(Exception):
    """
    Exception that may be raised in the course of getting config values
    """

    def __str__(self):
        return 'Unable to get config value'
