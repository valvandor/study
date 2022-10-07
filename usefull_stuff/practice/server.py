"""
Server part of messanger
"""

import socket
import sys
import json
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message


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

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('The -\'p\' parameter must be followed by the port number.')
        sys.exit(1)
    except ValueError:
        print('The port number can only be specified between 1024 and 65535.')
        sys.exit(1)

    # load which address to listen to
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print(
            'The -\'a\' parameter must be followed by the address the server should listen on..')
        sys.exit(1)

    # create socket

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))

    # listen a port
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Invalid message received from client.')
            client.close()


if __name__ == '__main__':
    main()
