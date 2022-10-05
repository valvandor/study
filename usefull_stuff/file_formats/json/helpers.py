"""
Helpfully functions
"""
from os import path
from pathlib import Path

from usefull_stuff.file_formats.json import const


def get_json_file_path(file_name) -> str:
    """
    Resolve path for directory with sample files and gets paths of all files in this directory

    Args:
        file_name: file name without file extension

    Returns:
        path of a file
    """
    root_dir = str(Path(__file__).parent.resolve())
    return path.join(root_dir, file_name + const.FILE_FORMAT)
