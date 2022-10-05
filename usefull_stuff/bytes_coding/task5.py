"""
Написать код, который выполняет пинг веб-ресурсов yandex.ru, youtube.com и
преобразовывает результат из байтовового типа данных в строковый без ошибок для любой кодировки операционной системы.
"""
import os
from pathlib import Path

import chardet
import subprocess
import platform

ENCODING_TYPE = 'utf-8'


def get_path_file_in_cur_dir(file_name: str) -> str:
    """
    Resolve path for intended file in current directory

    Args:
        file_name: name of the intended file

    Returns:
        absolute path for file
    """
    destination_dir = str(Path(__file__).parent.resolve())
    return os.path.join(destination_dir, file_name)


if __name__ == "__main__":
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '1', 'yandex.ru']
    process = subprocess.Popen(args, stdout=subprocess.PIPE)

    output_lines = []
    for line in process.stdout:
        encoding_info = chardet.detect(line)
        intended_encoding = encoding_info['encoding']

        decoded_data = line.decode(intended_encoding)
        line = decoded_data.encode(ENCODING_TYPE)

        output_lines.append(line.decode(ENCODING_TYPE))

    ping_file = get_path_file_in_cur_dir('ping_result.txt')

    with open(ping_file, 'w', encoding=ENCODING_TYPE) as f:
        f.writelines(output_lines)
