"""
Module with constants
"""
from typing import List

SAMPLE_FILES_DIR = 'sample_files'

FILE_FORMAT = '.csv'

ENCODING = 'utf-8'


class DataToSearch:
    """
    Enumerates for strings that should be searched
    """
    SystemManufacturer = 'Изготовитель системы'
    OSName = 'Название ОС'
    ProductCode = 'Код продукта'
    SystemType = 'Тип системы'

    def get_full_list(self) -> List[str]:
        """
        Returns list with strings to search
        """
        return [
            self.SystemManufacturer,
            self.OSName,
            self.ProductCode,
            self.SystemType
        ]
