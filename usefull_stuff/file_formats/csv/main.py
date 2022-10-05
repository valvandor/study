"""
Задание на закрепление знаний по модулю CSV.
Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и
формирующий новый «отчетный» файл в формате CSV.

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в него названия
столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Проверить работу программы через вызов функции write_to_csv().
"""
import csv
from typing import List

from usefull_stuff.file_formats.csv import const
from usefull_stuff.file_formats.csv.helpers import get_sample_file_paths, Parser, get_csv_file_path
from usefull_stuff.file_formats.csv.utils import detect_encoding


def write_to_csv(csv_file: str, csv_data: List[dict], headers: List[str]) -> None:
    """
    Writes to a file data

    Args:
        csv_file: file with a '.csv' extension
        csv_data: data to save as a list with dicts, e.g.
            [
                {
                    'some_name_1': 'value_1',
                    'some_name_2': '00971-OEM-1982661-00231',
                },
                {
                    'some_name_1': 'value_2',
                    'some_name_2': 'anything else',
                },
            ]
        headers: list of a headers for a csv file, e.g.
            ['some_name_1', 'some_name_2']

    """
    with open(csv_file, 'w', encoding=const.ENCODING) as f:
        csv_writer = csv.DictWriter(f, fieldnames=headers)
        csv_writer.writeheader()
        for item in csv_data:
            csv_writer.writerow(item)


if __name__ == "__main__":

    main_data = const.DataToSearch().get_full_list()
    parser = Parser(lookup_fields=main_data)

    csv_data = []
    files_to_parse = get_sample_file_paths()
    for file in files_to_parse:
        encoding = detect_encoding(file)
        file_data = parser.get_searched_data(file, encoding)
        csv_data.append(file_data)

    file_name = 'test_file'
    csv_file = get_csv_file_path(file_name)
    write_to_csv(csv_file, csv_data, headers=main_data)
