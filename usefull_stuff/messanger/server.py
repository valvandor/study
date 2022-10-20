"""
Server part of messanger
"""
import json
import logging
import select
import socket
from _socket import SocketType
from typing import Optional, Tuple, List

from common import const
from common.config_mixin import ConfigMixin
from common.exceptions import IncompleteConfigError
from common.abstract_socket import AbstractSocket

logger = logging.getLogger('server')


class ServerSocket(ConfigMixin, AbstractSocket):
    """
    Class represents server socket logic
    """

    def __init__(self):
        super().__init__()
        self._server_socket: Optional[SocketType] = None
        self._connected_sockets: List[SocketType] = []
        self._messages_as_db: list = []  # temporary solution
        self._read_list: List[SocketType] = []
        self._write_list: List[SocketType] = []

    def _add_to_connected_sockets(self, client_socket: SocketType) -> None:
        """
        Adds socket to class attribute represented list of 'connected' client sockets

        Args:
            client_socket: socket file descriptor representing the connection

        """
        self._connected_sockets.append(client_socket)

    def create_server_socket(self, reusable: bool = False) -> None:
        """
        Creates server socket and sets it to class attribute

        Args:
            reusable: a boolean value to indicate whether the port should be used when it is busy, by default is False
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

        refresh_timeout = self._config.get('socket_operation_timeout', 0.1)
        logger.info("Set timeout to refresh connections to a server socket [%s ms]", refresh_timeout * 1000)
        tcp_socket.settimeout(refresh_timeout)

        logger.info("Enable a server to accept connections (%s max)", max_connections)
        tcp_socket.listen(max_connections)
        self._server_socket = tcp_socket

    def _establish_client_connection(self) -> Tuple[SocketType, tuple]:
        """
        Waits for an incoming connection.
        In the case of a set timeout for the socket and after it expires, does nothing.

        When established, adds to connected sockets.

        Returns:
            client socket file descriptor and client address (as a pair of host address and port)
        """
        logger.debug("Await for a client connection")
        try:
            client_socket, client_address = self._server_socket.accept()
        except OSError:
            pass  # because of the set timeout
        else:
            logger.info("Occurred connection with %s", client_address)
            self._add_to_connected_sockets(client_socket)
            return client_socket, client_address

    def _reschedule_connected_sockets(self) -> None:
        """
        TODO
        """
        try:
            self._read_list, self._write_list, err_lst = select.select(__rlist=self._connected_sockets,
                                                                       __wlist=self._connected_sockets,
                                                                       __xlist=[],
                                                                       __timeout=0)
        except OSError:
            pass

    def run(self):
        while True:
            client_socket, client_address = self._establish_client_connection()

            if self._connected_sockets:
                self._reschedule_connected_sockets()

            for client_socket in self._read_list:
                client_message = self.get_message(client_socket)
                try:
                    if client_message[const.ACTION] == const.PRESENCE:
                        logger.debug("Test message is present")
                        response = self._process_test_message(client_message)
                        logger.debug("Attempt to send message to client")
                        self.send_message(client_socket, response)
                        logger.debug("Close connection with client %s", client_address)
                        client_socket.close()
                    else:
                        self.add_message(client_message)
                except ValueError:
                    logger.exception("Invalid message received from client")
                    client_socket.close()

    @staticmethod
    def _process_test_message(message: dict) -> dict:
        """
        Client message handler

        Args:
            message: client message
        Returns:
            message for client
        """
        if const.ACTION in message and const.TIME in message and const.USER in message \
                and message[const.USER][const.ACCOUNT_NAME] == 'Guest':
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
