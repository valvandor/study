"""
Module with custom exceptions
"""


class IncompleteConfig(Exception):
    """
    Exception that may be raised in the course of getting config values
    """

    def __str__(self):
        return 'Unable to get config value'


class BadRequest(Exception):
    """
    class of exception that occurs on a server side when response is 400
    """

    def __str__(self):
        return "Incorrect sent data"


class GreetingError(Exception):
    """
    Class of exception that occurs during first communication with a server
    """

    def __str__(self):
        return "Incorrect greetings with a server"


class IncorrectDataReceived(Exception):
    """
    Class of exception that may be raised when invalid data is received from the socket
    """

    def __str__(self):
        return 'Incorrect message received'
