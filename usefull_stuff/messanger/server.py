"""
Server part of messanger
"""

import socket
import sys
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, PRESENCE, TIME, USER, ERROR
from common.utils import get_message, send_message
from config.config import bind_config_file


def process_client_message(message: dict) -> dict:
    """
    Client message handler

    Args:
        message: client message
    Returns:
        message for client
    """
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    """
    Loads command line options, if unable to find values, uses default values:
        server.py -p 8888 -a 127.0.0.1

    Raises:
        ValueError: if port number is invalid
    """
    config_file = bind_config_file()
    with open(config_file) as f:
        config = json.load(f)

    listen_port = config.get('listen_port')
    if listen_port < 1024 or listen_port > 65535:
        print('The port number can only be specified between 1024 and 65535.')
        sys.exit(1)

    default_listen_address = ''  # allow any
    listen_address = config.get('listen_address', default_listen_address)

    # create socket
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))

    # listen a port
    max_connections = config.get('max_connections', 3)
    transport.listen(max_connections)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client, config)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response, config)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Invalid message received from client.')
            client.close()


if __name__ == '__main__':
    main()
