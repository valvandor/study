"""
 Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
 Далее забыть о том, что мы сами только что создали этот файл и исходить из того,
 что перед нами файл в неизвестной кодировке.
 Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.
"""
from typing import Iterable

from chardet import detect

from usefull_stuff.bytes_coding.task5 import get_path_file_in_cur_dir

ENCODING_TYPE = 'utf-8'


def write_content_to_file(content: Iterable, file_name) -> None:
    """
    Write content to file in current dir
    """
    file_to_test = get_path_file_in_cur_dir(file_name)
    with open(file_to_test, 'w', encoding=ENCODING_TYPE) as f:
        for sample in content:
            f.write(sample)
            f.write('\n')


SAMPLES = ['сетевое программирование', 'сокет', 'декоратор']


if __name__ == "__main__":
    sample_file = 'file_to_test.txt'

    # ARRANGE
    write_content_to_file(SAMPLES, sample_file)

    # ACT
    with open(sample_file, 'rb') as f:
        content = f.read()
    intended_encoding = detect(content)['encoding']

    with open(sample_file, encoding=intended_encoding) as f:
        content = f.read()
    print(content)
