"""
Client part of messanger
"""
import json
import logging
import socket
import time
from _socket import SocketType
from datetime import timezone, datetime
from threading import Thread
from typing import Optional, Any, Dict

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
        else:
            self._communicate_with_server(refresh_timeout=1)

    def _communicate_with_server(self, refresh_timeout: int) -> None:
        """
        Creates two threads to communicate with the server (receiving and sending),
        makes them demons and then starts them.

        Checks that they are alive according to the timeout.

        Args:
            refresh_timeout: timeout in seconds to check that threads are alive

        """
        receiving_thread = Thread(target=self._receive_from_server)
        receiving_thread.daemon = True
        receiving_thread.start()

        sending_thread = Thread(target=self._send_through_interactive)
        sending_thread.daemon = True
        sending_thread.start()

        while True:
            time.sleep(refresh_timeout)
            if receiving_thread.is_alive() and sending_thread.is_alive():
                continue
            break

    def _receive_from_server(self) -> None:
        """
        Represents a handler for messages from other users coming from the server
        """

        while True:
            try:
                message = self.get_message(self._client_socket)
                if message.get(const.ACTION) == const.MESSAGE and message.get(const.RECEIVER) == self._client_name:
                    print(f'\n{message.get(const.SENDER)}: {message.get(const.MESSAGE_TEXT)}\n')

                else:
                    logger.error(f'Incorrect message received from server: {message}')
            except (OSError, ConnectionError, ConnectionAbortedError,
                    ConnectionResetError, json.JSONDecodeError):
                logger.critical(f'Lost connection to server')
                break

    def _send_through_interactive(self) -> None:
        """
        Represents a user interface with interactive session in an infinite loop
        """
        self._print_help()
        while True:
            command = input('Enter command: ')
            if command == 'message':
                message = self._create_message()
                self.send_message(self._client_socket, message)

            elif command == 'help':
                self._print_help()

            elif command == 'exit':
                message = self._create_exit_message()
                self.send_message(self._client_socket, message)
                print('Goodbye')
                logger.info('Expected terminating connection by client')
                # make possible for the message to have time to go
                time.sleep(0.5)
                break

            else:
                print('Unknown command, please try again ("help" command for information)')

    @staticmethod
    def _print_help():
        """
        Displays usage help
        """
        print('Supported commands:\n'
              '    message - send a message (receiver and message text will be requested separately);\n'
              '    help - show usage help'
              '    exit - exit the program')

    def _create_message(self) -> Dict[str, Any]:
        """
        Interactively asks receiver and text of a message and creates message based on this data.

        Returns:
            formed message
        """
        message_receiver = input('Enter addressee of a message : ')
        message_body = input('Enter message to send: ')
        message = {
            const.ACTION: const.MESSAGE,
            const.SENDER: self._client_name,
            const.RECEIVER: message_receiver,
            const.TIME: datetime.now().isoformat(),
            const.MESSAGE_TEXT: message_body
        }
        return message

    def _create_exit_message(self) -> Dict[str, Any]:
        """
        Creates exit message

        Returns:
            exit message
        """
        return {
            const.ACTION: const.EXIT,
            const.TIME: datetime.now().isoformat(),
            const.ACCOUNT_NAME: self._client_name
        }


if __name__ == '__main__':
    client_transport = ClientSocket()
    client_transport.setup_log_config(in_project_dir=True)
    client_transport.start()
