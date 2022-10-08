"""
Server part of messanger
"""

import socket
import json
from _socket import SocketType

from common import const
from common.utils import get_message, send_message
from config.config import bind_config_file


class ServerSocket:
    """
    Class represents server socket logic
    """
    def __init__(self):
        self._config = self._get_config()

    @staticmethod
    def _get_config() -> dict:
        config_file = bind_config_file()
        with open(config_file) as f:
            return json.load(f)

    def _create_server_socket(self) -> SocketType:
        """
        Creates server socket

        Returns:
            socket object with options based on config
        """

        listen_address = self._config['listen_address']
        listen_port = self._config['listen_port']
        max_connections = self._config['max_connections']

        # create socket based on tcp/ip
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # make possible to use socket on busy port
        transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to a local address
        transport.bind((listen_address, listen_port))

        # enable a server to accept connections
        transport.listen(max_connections)
        return transport

    def run(self):
        transport = self._create_server_socket()
        while True:
            client, client_address = transport.accept()
            try:
                message_from_client = get_message(client, self._config)
                print(message_from_client)
                response = self._process_client_message(message_from_client)
                send_message(client, response, self._config)
                client.close()
            except (ValueError, json.JSONDecodeError):
                print('Invalid message received from client.')
                client.close()

    @staticmethod
    def _process_client_message(message: dict) -> dict:
        """
        Client message handler

        Args:
            message: client message
        Returns:
            message for client
        """
        if const.ACTION in message and message[const.ACTION] == const.PRESENCE and const.TIME in message \
                and const.USER in message and message[const.USER][const.ACCOUNT_NAME] == 'Guest':
            return {const.RESPONSE: 200}
        return {
            const.RESPONSE: 400,
            const.ERROR: 'Bad Request'
        }


if __name__ == '__main__':
    server_socket = ServerSocket()
    server_socket.run()
