"""
Module with AbstractSocket class
"""
import json
import os
import sys
from _socket import SocketType


sys.path.append(os.path.join(os.getcwd(), '..'))
from common.exceptions import IncorrectDataReceived
from common.utils import get_common_logger, logged

logger = get_common_logger()


class AbstractSocket:
    """
    Abstract class containing common logic for SocketType objects
    """
    def __init__(self):
        self._config = self.get_config()

    @logged(logger)
    def get_message(self, client: SocketType) -> dict:
        """
        Receives and decodes messages

        Args:
            client: socket file descriptor representing the connection

        Raises:
            ValueError: if was mistake during conversion
        """

        encoding = self._config.get('encoding', 'utf-8')
        max_msg_length = self._config.get('max_bytes_for_msg', '1024')

        encoded_response = client.recv(max_msg_length)
        if isinstance(encoded_response, bytes):
            json_response = encoded_response.decode(encoding)
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            else:
                raise IncorrectDataReceived
        else:
            raise IncorrectDataReceived

    @logged(logger)
    def send_message(self, sock: SocketType, message: dict) -> None:
        """
        Encodes and sends a message

        Args:
            sock:
            message:
        Raises:
            TypeError: if got wrong message
        """
        encoding = self._config.get('encoding', 'utf-8')

        if not isinstance(message, dict):
            raise TypeError
        js_message = json.dumps(message)
        encoded_message = js_message.encode(encoding)
        sock.send(encoded_message)

    def get_config(self) -> dict:
        """
        Should return config as a dict with all necessary options

        Raises:
            NotImplementedError: when method is not redefined
        """
        raise NotImplementedError
