"""
Client part of messanger
"""

import json
import socket
import time
from _socket import SocketType

from common import const
from common.utils import get_message, send_message
from config.config import bind_config_file
from exceptions import IncompleteConfigError


class ClientSocket:
    """
    Class represents client socket logic
    """
    def __init__(self):
        self._config = self._get_config()

    @staticmethod
    def _get_config() -> dict:
        config_file = bind_config_file()
        with open(config_file) as f:
            return json.load(f)

    @property
    def _connected_client_socket(self) -> SocketType:
        """
        Initializes a socket via config values

        Returns:
            connected socket
        """
        try:
            server_port = self._config['listen_port']
            server_address = self._config['listen_address']
        except KeyError as err:
            raise IncompleteConfigError from err

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((server_address, server_port))
        return tcp_socket

    def send_presence_message(self):
        """
        Sends presence message
        """
        client_socket = self._connected_client_socket
        message_to_server = self._create_presence()
        send_message(client_socket, message_to_server, self._config)
        try:
            answer = self._process_ans(get_message(client_socket, self._config))
            print(answer)
        except (ValueError, json.JSONDecodeError):
            print('Failed to decode server message.')

    @staticmethod
    def _create_presence(account_name: str = 'Guest') -> dict:
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

    @staticmethod
    def _process_ans(message):
        """
        Parses the server response
        """
        if const.RESPONSE in message:
            if message[const.RESPONSE] == 200:
                return '200 : OK'
            return f'400 : {message[const.ERROR]}'
        raise ValueError


if __name__ == '__main__':
    transport = ClientSocket()
    transport.send_presence_message()
