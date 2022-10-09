"""
Server part of messanger
"""

import socket
import json
from _socket import SocketType

from common import const
from common.exceptions import IncompleteConfigError
from common.abstract_socket import AbstractSocket


class ServerSocket(AbstractSocket):
    """
    Class represents server socket logic
    """

    @property
    def _server_socket(self) -> SocketType:
        """
        Creates server socket

        Returns:
            socket object with options based on config
        """

        try:
            listen_address = self._config['listen_address']
            listen_port = self._config['listen_port']
            max_connections = self._config['max_connections']
        except KeyError as err:
            raise IncompleteConfigError from err

        # create socket based on tcp/ip
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # make possible to use socket on busy port
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to a local address
        tcp_socket.bind((listen_address, listen_port))

        # enable a server to accept connections
        tcp_socket.listen(max_connections)
        return tcp_socket

    def run(self):
        while True:
            client, client_address = self._server_socket.accept()
            try:
                message_from_client = self.get_message(client)
                print(message_from_client)
                response = self._process_client_message(message_from_client)
                self.send_message(client, response)
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
