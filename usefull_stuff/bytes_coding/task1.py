"""
Каждое из слов «разработка», «сокет», «декоратор» представить в
строковом формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и
также проверить тип и содержимое переменных.
"""
from typing import Any


def print_type_and_content(var: Any) -> None:
    """
    Prints type of var asd its content

    Args:
        var: object reference
    """
    print(type(var))
    print(var)


SAMPLES = [
    ['разработка', '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'],
    ['сокет', '\u0441\u043e\u043a\u0435\u0442'],
    ['декоратор', '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']
]

if __name__ == "__main__":
    for sample in SAMPLES:
        unicode_test_sample = sample[1]
        print_type_and_content(unicode_test_sample)
        print(end=f'\n{"-" * 20}\n\n')
