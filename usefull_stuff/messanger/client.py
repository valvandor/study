"""
Client part of messanger
"""

import json
import socket
import time
from common import const
from common.utils import get_message, send_message
from config.config import bind_config_file


def create_presence(account_name: str = 'Guest') -> dict:
    """
    Generates a client presence request
    """
    out = {
        const.ACTION: const.PRESENCE,
        const.TIME: time.time(),
        const.USER: {
            const.ACCOUNT_NAME: account_name
        }
    }
    return out


def process_ans(message):
    """
    Parses the server response
    """
    if const.RESPONSE in message:
        if message[const.RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[const.ERROR]}'
    raise ValueError


def main():
    """
    Loads command line options
    """
    config_file = bind_config_file()
    with open(config_file) as f:
        config = json.load(f)

    server_port = config['listen_port']
    server_address = config['listen_address']

    # Socket initialization and exchange

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server, config)
    try:
        answer = process_ans(get_message(transport, config))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Failed to decode server message.')


if __name__ == '__main__':
    main()
