"""
Server part of messanger
"""
import logging
import socket
import json
from _socket import SocketType
from typing import Optional

from common import const
from common.config_mixin import ConfigMixin
from common.exceptions import IncompleteConfigError
from common.abstract_socket import AbstractSocket

logger = logging.getLogger('server')


class ServerSocket(ConfigMixin, AbstractSocket):
    """
    Class represents server socket logic

    Params:
        - reusable: a boolean value to indicate whether the port should be used when it is busy, by default is False
    """
    def __init__(self):
        super().__init__()
        self._server_socket: Optional[SocketType] = None

    def create_server_socket(self, reusable: bool = False) -> None:
        """
        Creates server socket and sets it to class attribute

        Returns:
            socket object with options based on config
        Raises:
            IncompleteConfigError: when wrong config
        """

        try:
            listen_address = self._config['listen_address']
            listen_port = self._config['listen_port']
            max_connections = self._config['max_connections']
        except KeyError as err:
            logger.exception("Unable to get options from config")
            raise IncompleteConfigError from err

        logger.info("Create socket based on tcp/ip")
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if reusable:
            logger.warning("Possible use of a socket on a busy port")
            tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        logger.info("Bind the socket to a local address (%s:%s)", listen_address, listen_port)
        tcp_socket.bind((listen_address, listen_port))

        logger.info("Enable a server to accept connections")
        tcp_socket.listen(max_connections)
        self._server_socket = tcp_socket

    def run(self):
        while True:
            logger.debug("Await for a client connection")
            client, client_address = self._server_socket.accept()
            logger.info("Occurred connection with %s", client_address)
            try:
                message_from_client = self.get_message(client)
                logger.debug("Got message from client: %s", message_from_client)
                response = self._process_client_message(message_from_client)
                logger.debug("Attempt to send message to client")
                self.send_message(client, response)
                logger.debug("Close connection with client %s", client_address)
                client.close()
            except (ValueError, json.JSONDecodeError):
                logger.exception("Invalid message received from client")
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

    def close(self):
        """
        Closes server socket
        """
        self._server_socket.close()


if __name__ == '__main__':
    server_transport = ServerSocket()
    server_transport.setup_log_config(in_project_dir=True)
    server_transport.create_server_socket(reusable=True)
    server_transport.run()
