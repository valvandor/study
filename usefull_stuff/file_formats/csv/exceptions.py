"""
Module with custom exceptions
"""


class EmptyFileError(Exception):
    """
    Class of the exception that may be raised when file is empty
    """

    def __init__(self, file_name):
        super().__init__()
        self._file = file_name

    def __str__(self):
        return "The file {} is empty".format(self._file)
