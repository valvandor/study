"""
Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.

Для этого:
Подготовить данные для записи в виде словаря,
в котором первому ключу соответствует список, второму — целое число, третьему — вложенный словарь,
где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке ASCII (например, €);

Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом: allow_unicode = True;

ВАЖНО: Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""
import yaml  # should be installed

from usefull_stuff.file_formats.yaml import const
from usefull_stuff.file_formats.yaml.helpers import get_yaml_file_path
from usefull_stuff.file_formats.yaml.samples import DATA

if __name__ == "__main__":

    file = get_yaml_file_path(file_name='file')

    with open(file, 'w', encoding=const.ENCODING) as f:
        yaml.dump(DATA, f, default_flow_style=False, allow_unicode=True)

    with open(file, 'r', encoding=const.ENCODING) as f:
        file_content = yaml.load(f, Loader=yaml.FullLoader)

    assert file_content == DATA
