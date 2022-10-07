"""
Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными.
Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item),
количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;

Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""
import json

from usefull_stuff.file_formats.json import const
from usefull_stuff.file_formats.json.helpers import get_json_file_path


def write_order_to_json(item: str,
                        quantity: int,
                        price: int or float,
                        buyer: str,
                        date: str) -> None:
    """
    Creates a dictionary from the given values and writes it to a file (orders.json) by key ('orders')
    """
    file_path = get_json_file_path(file_name=const.ORDERS)

    with open(file_path, 'r', encoding=const.ENCODING) as f:
        content = json.load(f)

    content[const.ORDERS].append({
        const.ITEM: item,
        const.QUANTITY: quantity,
        const.PRICE: price,
        const.BUYER: buyer,
        const.DATE: date,
    })

    with open(file_path, 'w', encoding=const.ENCODING) as f:
        json.dump(content, f, indent=4)


if __name__ == "__main__":

    write_order_to_json(item='sheet',
                        quantity=2,
                        price=123.45,
                        buyer='Pupkin',
                        date='today')
