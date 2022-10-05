"""
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое и
выполнить обратное преобразование (используя методы encode и decode).
"""
from usefull_stuff.bytes_coding.task1 import print_type_and_content

SAMPLES = ['разработка', 'администрирование', 'protocol', 'standard']

ENCODING_TYPE = 'utf-8'

if __name__ == "__main__":
    decoded_data = []
    for sample in SAMPLES:
        decoded_sample = sample.encode(ENCODING_TYPE)
        print_type_and_content(decoded_sample)
        decoded_data.append(decoded_sample)

    encoded_samples = []
    for data in decoded_data:
        encoded_sample = data.decode(ENCODING_TYPE)
        print_type_and_content(encoded_sample)
        encoded_samples.append(encoded_sample)

    assert encoded_samples == SAMPLES
