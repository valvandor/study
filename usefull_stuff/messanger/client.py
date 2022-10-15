"""
Client part of messanger
"""

import json
import socket
from _socket import SocketType
from datetime import timezone, datetime
from typing import Optional

from common import const
from common.config_mixin import ConfigMixin
from common.exceptions import IncompleteConfigError
from common.abstract_socket import AbstractSocket


class ClientSocket(ConfigMixin, AbstractSocket):
    """
    Class represents client socket logic
    """

    def __init__(self):
        super().__init__()
        self._client_socket: Optional[SocketType] = None

    def create_connected_client_socket(self) -> None:
        """
        Initializes a socket via config values and sets it to class attribute

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
        self._client_socket = tcp_socket

    def send_presence_message(self):
        """
        Sends presence message
        """
        client_socket = self._client_socket
        message_to_server = self._create_presence()

        self.send_message(client_socket, message_to_server)
        try:
            answer = self._process_ans(self.get_message(client_socket))
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
            const.TIME: str(datetime.now(timezone.utc)),
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
    client_transport = ClientSocket()
    client_transport.create_connected_client_socket()
    client_transport.send_presence_message()
