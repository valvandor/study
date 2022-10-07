"""
Module with helpfully functions and methods for task about 'csv'
"""
import os
from os import path
import re
from pathlib import Path
from typing import List, Dict

from usefull_stuff.file_formats.csv import const


def get_sample_file_paths() -> List[str]:
    """
    Resolve path for directory with sample files and gets paths of all files in this directory

    Returns:
        list with paths of sample files
    """
    root_dir = str(Path(__file__).parent.resolve())
    dir_with_samples = path.join(root_dir, const.SAMPLE_FILES_DIR)

    return [path.join(dir_with_samples, f) for f in os.listdir(dir_with_samples)
            if path.isfile(path.join(dir_with_samples, f))]


def get_csv_file_path(file_name) -> str:
    """
    Resolve path for directory with sample files and gets paths of all files in this directory

    Args:
        file_name: file name without file extension

    Returns:
        path of a file
    """
    root_dir = str(Path(__file__).parent.resolve())
    return path.join(root_dir, file_name + const.FILE_FORMAT)


class Parser:
    """
    Class with parsing logic
    """

    def __init__(self, lookup_fields: List[str]):
        self._lookup_fields = lookup_fields

    def get_searched_data(self, file, encoding) -> dict:
        """
        Gets data from a file

        Args:
            file: file to be open and parse
            encoding: encoding for correctly opening file

        """
        selected_rows = []

        with open(file, encoding=encoding) as f:
            for row in f:
                if self._is_need_to_choose(researched_string=row):
                    selected_rows.append(row)

        return self._split_content_to_dict(selected_rows)

    def _is_need_to_choose(self, researched_string: str) -> bool:
        """
        Checks for the presence of lookup fields in the search string

        Args:
            researched_string: string to check

        Returns:
            True if contain else False
        """
        flag = False
        for search_stm in self._lookup_fields:
            regex = fr'^{search_stm}'
            if bool(re.search(regex, researched_string)):
                flag = True
        return flag

    @staticmethod
    def _split_content_to_dict(content: List[str]) -> Dict[str, str]:
        """
        Splits list elements and transforms gotten items to a dict with a normalizable values

        Args:
            content: list with elements contains colon

        Returns:
            dict with items where lookup fields are keys
        Raises:
            ValueError: if unable to split list elements with a colon
        """
        data_dict = {}
        for data in content:
            key, value = data.split(':', maxsplit=1)
            value = value.replace('\n', '')
            data_dict[key] = value.strip()
        return data_dict
