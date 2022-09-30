"""
Каждое из слов «class», «function», «method» записать в байтовом типе.
Сделать это необходимо в автоматическом, а не ручном режиме, с помощью добавления литеры b к текстовому значению,
(т.е. ни в коем случае не используя методы encode, decode или функцию bytes) и
определить тип, содержимое и длину соответствующих переменных.
"""
from usefull_stuff.bytes_coding.task1 import print_type_and_content

SAMPLES = ['class', 'function', 'method']

if __name__ == "__main__":
    for sample in SAMPLES:
        byte_sample = eval(f'b"{sample}"')
        assert isinstance(byte_sample, bytes) is True, "the converted objects must belong to the class 'bytes'"

        print_type_and_content(byte_sample)
        print(len(byte_sample))
        print(end=f'\n{"-" * 20}\n\n')
