"""
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.
"""

SAMPLES = ['attribute', 'класс', 'функция', 'type']


if __name__ == "__main__":
    unable_write_as_bytes_words = []

    for sample in SAMPLES:
        try:
            eval(f'b"{sample}"')
        except SyntaxError:
            unable_write_as_bytes_words.append(sample)
    print(f'Невозможно "записать в байтовом типе": {unable_write_as_bytes_words}')
