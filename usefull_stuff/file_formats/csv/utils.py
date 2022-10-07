"""
Module with helpful functions
"""
from chardet import detect

from usefull_stuff.file_formats.csv.exceptions import EmptyFileError


def detect_encoding(file: str) -> str:
    """
    Detects encoding for file

    Args:
        file: filename (should be valid path)

    Returns:
        encoding for file
    Raises:
        FileNotFoundError: if unable to find file
        EmptyFileError: if file is empty
    """
    with open(file, 'rb') as f:
        content = f.read()
    if not content:
        raise EmptyFileError(file)
    return detect(content)['encoding']
