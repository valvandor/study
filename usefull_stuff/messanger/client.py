"""
Client part of messanger
"""

import logging
import socket
from _socket import SocketType
from datetime import timezone, datetime
from typing import Optional

from common import const
from common.config_mixin import ConfigMixin
from common.exceptions import IncompleteConfig, BadRequest, GreetingError
from common.abstract_socket import AbstractSocket

logger = logging.getLogger('client')


class ClientSocket(ConfigMixin, AbstractSocket):
    """
    Class represents client socket logic
    """

    def __init__(self):
        super().__init__()
        self._client_name = None
        self._client_socket: Optional[SocketType] = None

    def _create_connected_client_socket(self) -> None:
        """
        Initializes a socket via config values and sets it to class attribute

        Returns:
            connected socket
        """
        try:
            server_port = self._config['listen_port']
            server_address = self._config['listen_address']
        except KeyError as err:
            logger.exception("Unable to get options from config")
            raise IncompleteConfig from err

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((server_address, server_port))
        logger.info("Create client socket [server address %s:%s]", server_address, server_port)
        self._client_socket = tcp_socket

    def _make_greeting_with_server(self):
        """
        Initiates greetings with a server by sending presence message and checking server response

        Raises:
            GreetingError: if was mistake during communication with a server
        """
        transport = self._client_socket
        presence_message = self._create_presence()

        self.send_message(transport, presence_message)

        try:
            answer = self.get_message(transport)
            result = self._check_server_response(answer)
        except BadRequest as err:
            raise GreetingError from err
        logger.debug("Got answer from a server [%s]", result)

    @staticmethod
    def _check_server_response(message) -> str:
        """
        Checks the server response

        Returns:
            string with ok message and 200 code
        Raises:
            BadRequest: when got 400 in a response
        """
        if message[const.RESPONSE] == 200:
            return '200 : OK'
        if message[const.RESPONSE] == 400:
            raise BadRequest

    def _create_presence(self) -> dict:
        """
        Generates a client presence request
        """
        if not self._client_name:
            self._set_client_name()
        out = {
            const.ACTION: const.PRESENCE,
            const.TIME: str(datetime.now(timezone.utc)),
            const.USER: {
                const.ACCOUNT_NAME: self._client_name
            }
        }
        logger.debug("Create presence message from [%s] account", self._client_name)
        return out

    def _set_client_name(self) -> None:
        """
        Interactively asks client name and sets it to class attribute
        """
        client_name = input('Enter your username: ')
        self._client_name = client_name

    def start(self):
        """
        Entry point for client
        """
        self._create_connected_client_socket()
        self._set_client_name()
        try:
            self._make_greeting_with_server()
        except GreetingError:
            logger.exception("Failed to establish connection with a server message")


if __name__ == '__main__':
    client_transport = ClientSocket()
    client_transport.setup_log_config(in_project_dir=True)
    client_transport.start()
