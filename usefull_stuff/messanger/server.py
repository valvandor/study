"""
Server part of messanger
"""
import logging
import select
import socket
from _socket import SocketType
from datetime import datetime, timezone
from typing import Optional, List, Dict

from common import const
from common.config_mixin import ConfigMixin
from common.exceptions import IncompleteConfig
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
        self._read_list: List[SocketType] = []
        self._write_list: List[SocketType] = []
        self._socket_to_name_mapper: Dict[str: SocketType] = {}

    def _add_to_connected_sockets(self, client_socket: SocketType) -> None:
        """
        Adds socket object to class attribute represented list of 'connected' client sockets

        Args:
            client_socket: socket file descriptor representing the connection

        """
        self._connected_sockets.append(client_socket)

    def _add_client_to_mapper(self, account: str, client_socket: SocketType) -> None:
        """
        Adds to attribute represented mapper (dict of account names to sockets) new item

        Args:
            account: account name that would be used as a key
            client_socket: socket file descriptor representing the client connection that would be used as a value
        """
        self._socket_to_name_mapper[account] = client_socket

    def _remove_from_connected_sockets(self, client_socket: SocketType) -> None:
        """
        Removes socket object from class attribute represented list of 'connected' client sockets

        Args:
            client_socket: socket file descriptor representing the connection

        """
        logger.debug("Remove from active connection %s", client_socket)
        self._connected_sockets.remove(client_socket)

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
            raise IncompleteConfig from err

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

    def _establish_client_connection(self) -> None:
        """
        Waits for an incoming connection.
        In the case of a set timeout for the socket and after it expires, does nothing.

        When established, adds to connected sockets.

        Returns:
            client socket file descriptor and client address (as a pair of host address and port)
        """
        try:
            client_socket, client_address = self._server_socket.accept()
        except OSError:
            pass  # because of the set timeout
        else:
            logger.info("Occurred connection with %s", client_address)
            self._add_to_connected_sockets(client_socket)

    def _reschedule_connected_sockets(self) -> None:
        """
        Refreshes lists of sockets that ready for some kind of I/O in dependency of connected sockets.
        """
        try:
            self._read_list, self._write_list, err_lst = select.select(self._connected_sockets,
                                                                       self._connected_sockets,
                                                                       [], 0)
        except OSError:
            pass

    def run(self):
        while True:
            self._establish_client_connection()

            if self._connected_sockets:
                self._reschedule_connected_sockets()

                for client_socket in self._read_list:
                    logger.debug("Handling a message from %s", client_socket)
                    client_message = self.get_message(client_socket)
                    action = client_message.get(const.ACTION)

                    if action == const.PRESENCE:
                        logger.debug("Greeting message is present")
                        self._process_greeting_message(client_message, client_socket)

                    if action == const.MESSAGE:
                        logger.debug("Ordinary message is present")
                        self._process_client_message(client_message)

                    if action == const.EXIT:
                        logger.debug("Exit message is present")
                        self._process_exit_message(client_message)

                    else:
                        logger.warning("Unsupported message type received from a client")
                        continue

    def _process_greeting_message(self, message: dict, client_socket: SocketType) -> None:
        """
        Represents message handler for greeting. Sends response with code 200 and close socket client

        Args:
            message: client message
            client_socket: socket file descriptor from client side
        Returns:
            message for client
        """
        if const.USER in message:
            response = {const.RESPONSE: 200}
            current_account = message[const.USER].get(const.ACCOUNT_NAME)
            logger.debug("Normal greeting with %s", current_account)

            self._add_client_to_mapper(current_account, client_socket)
            logger.debug("Mapper was updated for '%s' account", current_account)
        else:
            response = {
                const.RESPONSE: 400,
                const.ERROR: 'Bad Request'
            }
        logger.debug("Attempt to send message to client")
        self.send_message(client_socket, response)

    def _process_client_message(self, client_message) -> None:
        """
        Represents message handler for 'regular' client messages.
        After ensuring possibility of sending the message to receiver, sends message.

        Args:
            client_message: message to send

        """
        target_account_name = client_message[const.RECEIVER]
        receiver_socket = self._socket_to_name_mapper.get(target_account_name)
        if receiver_socket in self._write_list:
            logger.debug("Found active receiver %s", receiver_socket.getpeername())
            self.send_message(receiver_socket, client_message)
        else:
            logger.debug("Unable to find target socket in connected sockets")
            # todo: notify about undelivered message

    def _process_exit_message(self, client_message):
        """
        Represents message handler for 'exit' client messages.
        After ensuring possibility of sending the message to receiver, sends message.

        Args:
            client_message: message to send
        """
        account_name = client_message[const.ACCOUNT_NAME]
        socket_to_disconnect = self._socket_to_name_mapper[account_name]

        self._remove_from_connected_sockets(socket_to_disconnect)
        logger.info("Client %s was disconnected", socket_to_disconnect.getpeername())
        del self._socket_to_name_mapper[account_name]

    def _send_broadcast_message(self, message: dict) -> None:
        """
        NOT IMPLEMENTED

        Sends to all connected client sockets message.
        If unable to send message to client closes connection and removes from connected sockets.

        Args:
            message: message to send
        """
        for client_socket in self._write_list:
            try:
                self.send_message(client_socket, message)
            except Exception:
                logger.info('Client %s disconnected from server', client_socket.getpeername())
                client_socket.close()
                self._remove_from_connected_sockets(client_socket)

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
